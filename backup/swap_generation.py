import os
import datetime
import time
from django.db.utils import InterfaceError
from django import db as post_db

from campaign.models import TradeOperator
from core.models.base_models import Operator
from engine.swap.swap_helper import get_active_cmt_trade_list, get_trade_option_segment_list, get_option_type_dict, get_trade_advertiser_level_map, create_dir, map_segment_to_stb_id, copy_slave_files_to_master, update_processed_trades_state
from engine.swap.intersection_helper import generate_intersection, split_segment_intersection, get_segment_round_robin_map, get_segment_dataset_map, get_segment_list
from engine.constants import *
from core.constants import OPERATOR_NAME, MASTER_TAGS
from core.helper.common_helper import get_master_db_connection
from collections import OrderedDict
from engine.configurations import *
from engine.helper.generic import get_directory_name_from_date_str, get_collection_name_for_processing_date, get_directory_path_for_processing_date, get_slave_info_dict
from bitarray import bitarray
from engine.helper.shell_command import ShellUtils
from engine.helper.database_snapshot import convert_camel_case_to_snake_case
from functools import reduce
from core.models.trade import CustomizedMessagingTrade, MessagingGroup, OrderSegmentTagFileMap, OrderFiles
from adcuratio.settings import BASE_DIR
from engine.helper.sentry_helper import sentry_capture_message

# Add Logs

# Do not create tag files if household count is less than THRESHOLD_VALUE
THRESHOLD_VALUE = int(TAG_THRESHOLD * DEMOGRAPHICS_DB_SIZE)

def update_trade_tracker(processing_date_str):
    '''
        seeds into mongo tracker for unprocessed trade
    '''
    collection_name = get_collection_name_for_processing_date(DATABASE_SNAPSHOT, processing_date_str)
    master_db = get_master_db_connection()
    processing_date = datetime.datetime.strptime(processing_date_str, DATE_FORMAT_Y_M_D)

    if SERVER_NAME == MASTER.lower():
        active_trade_list = get_active_cmt_trade_list(master_db, processing_date, collection_name)      #   gets list of active trade from snapshot
        option_type_dict = get_option_type_dict(master_db, processing_date, collection_name)      #         gets dict for wanted and unwanted CMOptions
        trade_meta_list = get_trade_meta_map(master_db, active_trade_list, processing_date, collection_name, option_type_dict)      #       gets list of campagins which are not processed yet
        seed_trade_tracker(master_db, trade_meta_list, processing_date, processing_date_str)      #     updates mongo tracker
        return True
    return False

def generate_swap(processing_date_str):

    '''
        create slave swaps for processing_date and copy back to master
    '''

    master_db = get_master_db_connection()
    processing_date = datetime.datetime.strptime(processing_date_str, DATE_FORMAT_Y_M_D)

    # Create Intersection Files for Slaves
    active_trade_for_swap_generation = get_active_trade_for_processing_date(master_db, processing_date)     #       gets list of active trade from snapshot
    initialiaze_trade_process(active_trade_for_swap_generation, processing_date, processing_date_str)       #       initializes the swap generation

    # Map intersection files created to stb id and move to master server
    processed_active_trade = get_active_trade_for_processing_date(master_db, processing_date)     #       gets list of active trade from snapshot

    map_start_time = time.time()
    map_segment_to_stb_id(processing_date_str, processing_date, processed_active_trade, master_db)     #       gets epsilon_ids using household ids from binary file index to
    print (f'time taken to map adcuratio internal id to epsilon adcuratio id {time.time() - map_start_time}')

    copy_start_time = time.time()
    copy_slave_files_to_master(processing_date_str, processed_active_trade, processing_date)     #       gets scp the files from slaves to master
    print (f'time taken to copy files from worker to master server {time.time() - copy_start_time}')


def initialiaze_trade_process(active_trade_for_processing_date, processing_date, processing_date_str):
    '''
        Create swap generation process for individual trades
    '''
    # For test
    # for active_trade in active_trade_for_processing_date:
    # 	if active_trade['trade_id'] == 59:

    # 		initialize_swap_generation({'trade_meta': active_trade, 'processing_date': processing_date, 'processing_date_str': processing_date_str})
    # 		return
    processing_date_str_dir = get_directory_name_from_date_str(processing_date_str)
    processing_date_order_path = SWAP_SEGMENT_INTERSECTION_DIR_PATH
    create_dir(processing_date_order_path)

    from billiard import Pool
    pools = Pool(SWAP_GENERATION_POOL_SIZE)
    pools.map(initialize_swap_generation, [{'trade_meta': active_trade, 'processing_date': processing_date, 'processing_date_str': processing_date_str}
                                            for active_trade in active_trade_for_processing_date])
    pools.close()
    pools.terminate()


def initialize_swap_generation(trade_meta):

    '''
        trade_meta_dict = {
                            'wanted_option_dict': OrderedDict([(4, [5]), (5, [11])]),
                            'trade_id': 55,
                            'meta': {
                                'bit_vector_id': 'bv_segment_23',
                                'segment_id': '23',
                                'level': 'brand',
                                'campaign_id': 2,
                                'company_id': '1',
                                'brand_id': '1',
                                'trade_id': '55',
                                'sub_brand_id': None,
                                'data_provider_type': 'acxiom',
                                'adspots': [{
                                    'adspot_id': 173,
                                    'channel_id': '1',
                                    'adspot_timestamp': None
                                }],
                                'oldest_adspot_date': None,
                                'original_adid': 2
                            },
                            'type': u 'refine',
                            'unwanted_option_dict': OrderedDict()
                        }
    '''
    trade_meta_dict = trade_meta['trade_meta']
    processing_date = trade_meta['processing_date']
    processing_date_str = trade_meta['processing_date_str']

    master_db = get_master_db_connection()

    trade_id = trade_meta_dict['trade_id']
    segment_id = trade_meta_dict['meta']['segment_id']
    processing_date_str_dir = get_directory_name_from_date_str(processing_date_str)
    processing_date_order_path = SWAP_SEGMENT_INTERSECTION_DIR_PATH
    trade_path = os.path.join(processing_date_order_path, str(trade_id))
    create_dir(trade_path)

    wanted_option_dict = {int(key): value for key, value in list(trade_meta_dict['wanted_option_dict'].items())}
    unwanted_option_dict = {int(key): value for key, value in list(trade_meta_dict['unwanted_option_dict'].items())}

    sorted_wanted_option_dict = OrderedDict(sorted(wanted_option_dict.items()))
    sorted_unwanted_option_dict = OrderedDict(sorted(unwanted_option_dict.items()))

    # Wanted Options
    if sorted_wanted_option_dict:
        create_swap_files(master_db, sorted_wanted_option_dict, trade_path, trade_id, processing_date, segment_id, wanted=True)     #       swap files are created for unwanted option

    # Unwanted Options
    if sorted_unwanted_option_dict:
        create_swap_files(master_db, sorted_unwanted_option_dict, trade_path, trade_id, processing_date, segment_id, wanted=False)      #       swap files are created for wanted option


def create_swap_files(master_db, option_dict, trade_path, trade_id, processing_date, segment_id, wanted=True):
    '''
        create segment intersection for wanted and unwanted cm options
    '''
    giver_and_taker_map = load_giver_and_taker_bit(option_dict, segment_id, processing_date, wanted)    # loads bit vectors from bin files of mgs {"giver": c, "taker": ["b1", "b2", "b3", "b4"]}
    updated_frequency_intersection_map = generate_intersection(giver_and_taker_map)     # does intersections among mgs
    for key, level_dict in updated_frequency_intersection_map.items():
        if key == 'taker':
            for level, segment_bit_dict in level_dict.items():
                for operator_name in list(TradeOperator.objects.filter(trade_id = trade_id).values_list('operator__name', flat = True)) + [MASTER_TAGS]:
                    op_fp_bin_path = os.path.join(OPERATOR_BIN_FILE_DIR_PATH, operator_name + FILE_FORMAT.BIN)
                    if not os.path.isfile(op_fp_bin_path):
                        error_mess = f' {operator_name} bit vector file is not generated considering total Target'
                        sentry_capture_message(message=error_mess)
                        print ('error_mess = ', error_mess)
                        op_bv = bitarray([1] * DEMOGRAPHICS_DB_SIZE)
                    else:
                        op_bv = bitarray()
                        op_bv.fromfile(open(op_fp_bin_path,'rb'))

                    for segment_id_hash, bit_list in segment_bit_dict.items():
                        op_seg_bv = bit_list & op_bv
                        bin_path = os.path.join(trade_path, operator_name + '__' + segment_id_hash)
                        with open(bin_path + FILE_FORMAT.BIN, 'wb') as swap_segment_file:
                            op_seg_bv.tofile(swap_segment_file)

                        update_key = '.'.join([SERVER_NAME, 'bin_files', operator_name, segment_id_hash])
                        processing_data = dict()
                        processing_data['file_path'] = bin_path + FILE_FORMAT.BIN
                        processing_data['count'] = bitarray.count(op_seg_bv)
                        master_db[TRADE_TRACKER].update({'trade_id': trade_id, 'processing_date': processing_date},
                            {'$set': {update_key: processing_data}})


def load_giver_and_taker_bit(option_dict, giver_segment_id, processing_date, wanted):
    giver_reciever_dict = {}
    giver_bit_vector = load_segment_bit_vector(processing_date, str(giver_segment_id))      #   loads mg bit vectors from binary files

    if wanted:
        giver = giver_bit_vector
    else:
        # Inplace Update
        bitarray.invert(giver_bit_vector)       #       if unwanted targets are required than bit vector inverion is done to avail all unwanted targets
        giver = giver_bit_vector

    giver_reciever_dict['giver'] = giver
    giver_reciever_dict['taker'] = dict()

    for cm_option, reciever_segment_id_list in list(option_dict.items()):
        for reciever_segment_id in reciever_segment_id_list:
            giver_reciever_dict['taker'][str(reciever_segment_id)] = load_segment_bit_vector(processing_date, str(reciever_segment_id))     #   reads binary file and convert it into bit vector

    return giver_reciever_dict


def load_segment_bit_vector(processing_date, bit_vector_id):
    segment_bit_vector_dict = dict()
    date_directory = processing_date.strftime('%Y-%m-%d').replace('-', '_')

    # This can be made dynamic in future where calculations can be done on household vs individual files for propagation
    bv_household_file_name = MG_HOUSEHOLD_KEY_PREFIX + str(bit_vector_id)

    # TODO Change SEGMENT_BIT_VECTOR_PATH to MG_BIT_VECTOR_PATH
    bit_vector_bin_file = os.path.join(SEGMENT_BIT_VECTOR_PATH,  date_directory, bv_household_file_name + '.bin')
    if not os.path.exists(bit_vector_bin_file):
        print('path for segment does not exist', bit_vector_bin_file)
        return None
    tmp_bitarray = bitarray()
    with open(bit_vector_bin_file, 'rb') as binary_file:
        tmp_bitarray.fromfile(binary_file)
    # tmp_bitarray = tmp_bitarray[1: DEMOGRAPHICS_DB_SIZE + 1]
    return tmp_bitarray


def get_trade_meta_map(master_db, active_trade_list, processing_date, collection_name, option_type_dict):
    '''
    This function returns trade meta data.

    :param active_cmt_trade_list: active trade list.
    :param processing_date: processing date.
    :param custom_messaging_option_map: custom messaging option dictioary.
    :returns: [{
                'wanted_option_dict': OrderedDict([(4, [5]), (5, [11])]),
                'trade_id': 55,
                'meta': {
                    'bit_vector_id': 'bv_segment_23',
                    'level': 'brand',
                    'segment_id': '23',
                    'company_id': '1',
                    'campaign_id': 2,
                    'brand_id': '1',
                    'trade_id': '55',
                    'sub_brand_id': None,
                    'adspots': [{
                        'adspot_id': 173,
                        'channel_id': '1',
                        'adspot_timestamp': None
                    }],
                    'data_provider_type': 'acxiom',
                    'oldest_adspot_date': None,
                    'original_adid': 2
                },
                'type': u 'refine',
                'unwanted_option_dict': OrderedDict()
            }, {
                'wanted_option_dict': OrderedDict(),
                'trade_id': 58,
                'meta': {
                    'bit_vector_id': 'bv_segment_26',
                    'level': 'brand',
                    'segment_id': '26',
                    'company_id': '1',
                    'campaign_id': 2,
                    'brand_id': '1',
                    'trade_id': '58',
                    'sub_brand_id': None,
                    'adspots': [{
                        'adspot_id': 173,
                        'channel_id': '1',
                        'adspot_timestamp': None
                    }],
                    'data_provider_type': 'acxiom',
                    'oldest_adspot_date': None,
                    'original_adid': 2
                },
                'type': u 'normal',
                'unwanted_option_dict': OrderedDict([(6, [2, 3, 6]), (14, [1])])
            }, {
                'wanted_option_dict': OrderedDict([(4, [5]), (5, [11])]),
                'trade_id': 59,
                'meta': {
                    'bit_vector_id': 'bv_segment_27',
                    'level': 'brand',
                    'segment_id': '27',
                    'company_id': '1',
                    'campaign_id': 2,
                    'brand_id': '1',
                    'trade_id': '59',
                    'sub_brand_id': None,
                    'adspots': [{
                        'adspot_id': 173,
                        'channel_id': '1',
                        'adspot_timestamp': None
                    }],
                    'data_provider_type': 'acxiom',
                    'oldest_adspot_date': None,
                    'original_adid': 2
                },
                'type': u 'mixed',
                'unwanted_option_dict': OrderedDict([(6, [2, 3, 6]), (14, [1])])
            }]
    '''

    trade_meta_data_list, ad_spot_id_list = list(), list()

    for cmt_trade in active_trade_list:
        trade_id = cmt_trade['id']
        trade_option_segment_dict = get_trade_option_segment_list(master_db, processing_date, collection_name,
                                                                option_type_dict, trade_id)     # categorizes mgs according to wanted or unwanted option

        wanted_option_dict = trade_option_segment_dict['wanted']
        unwanted_option_dict = trade_option_segment_dict['unwanted']

        # Check if adspot validation is required on daily basis

        trade_meta_data_map = dict()
        trade_meta_data_map['trade_id'] = trade_id
        trade_meta_info = get_trade_advertiser_level_map(cmt_trade)
        trade_meta_data_map['meta'] = trade_meta_info.copy()
        trade_meta_data_map['wanted_option_dict'] = wanted_option_dict
        trade_meta_data_map['unwanted_option_dict'] = unwanted_option_dict
        trade_meta_data_map['type'] = cmt_trade['type']
        trade_meta_data_map['name'] = cmt_trade['name']
        trade_meta_data_map['id'] = cmt_trade['id']

        trade_meta_data_list.append(trade_meta_data_map)        # generates meta data for each trade

    return trade_meta_data_list


def seed_trade_tracker(master_db, trade_meta_data_list, processing_date, processing_date_str):
    """
    Creates an initial entry in mongo with meta info for the trade
    """

    master_segment_intersection_path = COPY_ORDER_SEGMENT_DIR_PATH
    processing_date_str_dir = get_directory_name_from_date_str(processing_date_str)
    order_segment_process_date_path = get_directory_path_for_processing_date(master_segment_intersection_path, processing_date_str_dir)

    slave_info_dict = get_slave_info_dict()
    for trade_meta_dict in trade_meta_data_list:
        trade_id = trade_meta_dict['trade_id']
        trade_meta = trade_meta_dict['meta']
        trade_info_dict = slave_info_dict.copy()
        trade_info_dict['processing_date'] = processing_date
        trade_info_dict['trade_id'] = trade_id
        trade_info_dict['wanted_option_dict'] = trade_meta_dict['wanted_option_dict']
        trade_info_dict['unwanted_option_dict'] = trade_meta_dict['unwanted_option_dict']
        trade_info_dict['meta'] = trade_meta
        trade_info_dict['type'] = trade_meta_dict['type']
        trade_info_dict['name'] = trade_meta_dict['name']
        tags = dict()
        for operator_name in list(TradeOperator.objects.filter(trade_id = trade_id).values_list('operator__name',flat = True)) + [MASTER_TAGS]:
            tags[operator_name] = dict()
            tags[operator_name]['checks'] = dict()
            tags[operator_name]['checks'][CampaignStage.PROCESSED] = False
            tags[operator_name]['checks'][CampaignStage.FILE_UPLOADED_TO_S3] = False
            tags[operator_name]['checks'][CampaignStage.ICDX_CREATED] = False
            tags[operator_name]['tag_files'] = list()

        trade_info_dict['tags'] = tags
        trade_info_dict[CampaignStage.FILE_MERGED] = False
        trade_info_dict[CampaignStage.FILE_SPLIT] = False

        # Set this flag true when all processing is done in slaves and master
        # this flag is set when FILE_MERGED, FILE_SPLIT and FILE_UPLOADED_TO_S3 are True
        trade_info_dict[CampaignStage.PROCESSED] = False

        key = {'trade_id': trade_id, 'processing_date': processing_date}
        master_db[TRADE_TRACKER].update(key, trade_info_dict, upsert=True)      #   updates trade_tracker for the unprocessed trade

        order_segment_intersection_path = os.path.join(order_segment_process_date_path, str(trade_id))
        create_dir(order_segment_intersection_path)


def get_active_trade_for_processing_date(master_db, processing_date, data_distributor = None):
    ''' For a given processing date check if there are some trades that need to execute
        Derivative is not in this logic (Dont know why it is removed i added this long back)
    '''
    if data_distributor:
        return list(master_db[TRADE_TRACKER].find({'processing_date': processing_date, '.'.join(['tags', data_distributor, 'checks', CampaignStage.PROCESSED]): False}, {'_id': 0}))
    return list(master_db[TRADE_TRACKER].find({'processing_date': processing_date, 'processed': False}, {'_id': 0}))


def validate_trade_tracker():

    '''
    ToDo This implementation will change when daily processing is done for campaigns.
    eg: check what trades were needed to process with (processed flag and processing date)
    Right now only check is on processed state as processing date remains constant for testing (In Redis)

    Before doing any processing in master server eg, merge,  split etc verify all the trades are correctly processed
    Set this flag true when all processing is done my master server
    '''

    # run from master
    master_db = get_master_db_connection()
    if master_db[TRADE_TRACKER].find({'processed': False}).count():
        return False, list(master_db[TRADE_TRACKER].find({'processed': False}, {'trade_id': 1}))
    return True, None


def check_trades_processed_by_all_slaves():
    """
    Checks if all slaves have processed the trade and binary files are created. Execution does not proceed further if this returns false.
    """
    master_db = get_master_db_connection()

    unprocessed_trades = master_db[TRADE_TRACKER].find({'processed': False})
    slave_list = ['SLAVE' + str(num) for num in range(1, TOTAL_NUMBER_OF_SLAVES + 1)]

    all_trade_processed_by_slaves = False

    for trade in unprocessed_trades:
        all_trade_processed_by_slaves = all([trade[slave]['processed'] for slave in slave_list])
    return all_trade_processed_by_slaves


def split_segment_tag_files(processing_date_str):

    '''
        split merged files
    '''
    processing_date_dir = get_directory_name_from_date_str(processing_date_str)

    master_db = get_master_db_connection()

    processing_date = datetime.datetime.strptime(processing_date_str, DATE_FORMAT_Y_M_D)

    active_trade_list = get_active_trade_for_processing_date(master_db, processing_date)

    processing_date_merged_path = get_directory_path_for_processing_date(MERGED_ORDER_SEGMENT_DIR_PATH, processing_date_dir)
    segment_split_dir_path = os.path.join(SEGMENT_INTERSECTION_SPLIT_PATH, processing_date_dir)
    create_dir(segment_split_dir_path)

    for trade_obj in active_trade_list:
        trade_segment_dict = dict()
        trade_id = trade_obj['trade_id']

        if not trade_obj['file_merged']:
            print(f'trade id {trade_id} on split process')
            continue

        # This line is risky add this check somewhere else
        # will take it after code is working
        # for test it is ok
        # trade_segment_split_path = os.path.join(segment_split_dir_path, str(trade_id))
        # create_dir(trade_segment_split_path)


        order_split_file_list = list()
        for operator in trade_obj['tags'].keys():

            merged_trade_path = os.path.join(processing_date_merged_path, str(trade_id), operator)
            trade_segment_split_path = os.path.join(segment_split_dir_path, str(trade_id), operator)
            create_dir(trade_segment_split_path)

            for file_name in os.listdir(merged_trade_path):
                combination_id_hash = file_name.split('.')[0]
                segment_list = get_segment_list(combination_id_hash)
                split_len = len(segment_list) if len(segment_list) == 1 else SEGMENT_SPLIT_LENGTH
                combination_file_path = os.path.join(merged_trade_path, file_name)

                split_info_dict = {
                        'trade_segment_split_path': trade_segment_split_path,
                        'combination_file_path': combination_file_path,
                        'split_len': split_len,
                        'combination_id_hash': combination_id_hash

                }

                order_split_file_list.append(split_info_dict)

        initiate_split_process(order_split_file_list)       #   uses shell command to split files
        update_processed_trades_state(trade_id, CampaignStage.FILE_SPLIT)   # updates mongo tracker for the trade


def initiate_split_process(order_split_file_list):
    '''
        split files for order in parallel
    '''
    from billiard import Pool
    pools = Pool(SWAP_GENERATION_POOL_SIZE)
    pools.map(split_file, [split_file_info for split_file_info in order_split_file_list])
    pools.close()
    pools.terminate()


def split_file(split_dict):
    """
    Uses shell commands to split the file according to split length
    """

    trade_segment_split_path = split_dict['trade_segment_split_path']
    combination_file_path = split_dict['combination_file_path']
    split_len = split_dict['split_len']
    combination_id_hash = split_dict['combination_id_hash']

    prefix_for_split_command = os.path.join(trade_segment_split_path, combination_id_hash + '_')
    file_split_args = (split_len, combination_file_path, prefix_for_split_command)
    is_success, output, error_mess = ShellUtils.split_file(*file_split_args)
    if not is_success:
        sentry_capture_message(message=error_mess)
        print ('error_mess = ', error_mess)
        # Send email
        return


def create_icdx_files(processing_date_str):
    '''
    The function creates OrderSegmentTagFiles and updates the postgres db.
    '''

    processing_date_dir = get_directory_name_from_date_str(processing_date_str)

    master_db = get_master_db_connection()

    processing_date = datetime.datetime.strptime(processing_date_str, DATE_FORMAT_Y_M_D)

    active_trade_list = get_active_trade_for_processing_date(master_db, processing_date, OPERATOR_NAME.DISH)

    segment_split_dir_path = os.path.join(SEGMENT_INTERSECTION_SPLIT_PATH, processing_date_dir)
    split_file_prefix = DISH_FILE_PREFIX

    for trade_obj in active_trade_list:
        trade_id = trade_obj['trade_id']

        if not trade_obj['file_split']:
            print(f'skipped for trade id {trade_id} on create icdx for dish,as split is not completed')
            continue

        if OPERATOR_NAME.DISH not in trade_obj['tags'].keys():
            continue

        order_icdx_path = os.path.join(ICDX_DIR_PATH, str(trade_id), OPERATOR_NAME.DISH)
        create_dir(order_icdx_path)
        # This line is risky add this check somewhere else
        # will take it after code is working
        # for test it is ok
        try:
            post_db.connection.close()
            trade = CustomizedMessagingTrade.objects.filter(id=trade_id).first()
            if trade:
                trade.ordersegmenttagfilemap_set.all().delete()

        except:
            import traceback
            print(traceback.format_exc())
        trade_segment_split_path = os.path.join(segment_split_dir_path, str(trade_id), OPERATOR_NAME.DISH)

        order_tag_file = list()
        for file_name in os.listdir(trade_segment_split_path):

            split_len = len(file_name.split('_'))
            icdx_order_data = dict()
            combination_file_path = os.path.join(trade_segment_split_path, file_name)
            header_file_path = os.path.join(BASE_DIR, 'engine/swap/icdx_headers')
            print ('file_name = ', combination_file_path)

            row_count_args = (combination_file_path, )
            is_success, output, error_mess = ShellUtils.get_file_row_count(*row_count_args)
            if not is_success:
                print(error_mess)
                sentry_capture_message(message=error_message)
                # Send email
                return

            row_count = int(output)
            dish_file_name = '_'.join([DISH_FILE_PREFIX + file_name, str(trade_id)])

            file_list = [header_file_path, combination_file_path]
            order_tag_icdx_path = os.path.join(order_icdx_path, dish_file_name + FILE_FORMAT.CSV)
            merge_args = (file_list, order_tag_icdx_path)


            concatenate_start_time = time.time()
            is_success, error_message = ShellUtils.add_header(*merge_args)
            print (f'time taken to concatenate file is {time.time() - concatenate_start_time}')

            # Add Exception Handler
            if not is_success:
                print('error merging file = ', error_message)
                sentry_capture_message(message=error_message)
                return

            icdx_order_data['row_count'] = row_count
            icdx_order_data['file_path'] = order_tag_icdx_path
            order_tag_file.append(icdx_order_data)

            segment_files_map_dict = dict()
            trade = CustomizedMessagingTrade.objects.get(id=trade_id)
            segment_files_map_dict["adcuratio_filename"] = file_name + FILE_FORMAT.CSV
            segment_files_map_dict["level"] = split_len

            # Not populating segment_files_map_dict["ad_id"] field as currently this is not required
            segment_files_map_dict["dish_filename"] = dish_file_name + FILE_FORMAT.CSV
            segment_files_map_dict["row_count"] = row_count
            o_s_t, o_created = OrderSegmentTagFileMap.objects.get_or_create(**segment_files_map_dict)
            o_s_t.trades.add(trade)
            o_s_t.threshold_value = DISH_TAG_THRESHOLD if os.environ.get('SERVER_DESC') == 'production' else THRESHOLD_VALUE
            o_s_t.local_file_path = order_tag_icdx_path
            if row_count < o_s_t.threshold_value:
                o_s_t.declined_by_adcuratio = True

            # sent_to_operator is set to True to visible in dish portal for testing instances
            if not o_s_t.declined_by_adcuratio:
                o_s_t.sent_to_operator = check_env_variable()

            # else:
            #     #----------scp order_tag_icdx_path -> /home/dishuser/data/to_dish
            #     if SERVER_DESC == 'test':
            #         Ftp_Hostname = 'ubuntu@'+str(FTP_HOSTNAME)
            #         args = [ENGINE_PEM_FILE, order_tag_icdx_path, Ftp_Hostname, '/mnt2/mnt2/test_icdx']
            #         is_success, error_message = ShellUtils.scp_local_to_remote(*args)
            #         if not is_success:
            #             print('error merging file = ', error_message)
            #             sentry_capture_message(message=error_message)
            #             return

            o_s_t.save()

        key = {'trade_id': trade_id, 'processing_date': processing_date}
        file_projection = '.'.join(['tags', OPERATOR_NAME.DISH, 'tag_files'])
        flag_projection = '.'.join(['tags', OPERATOR_NAME.DISH, 'checks', CampaignStage.ICDX_CREATED])
        master_db[TRADE_TRACKER].update(key, {'$set': {file_projection: order_tag_file, flag_projection:True}})

def check_env_variable():
    '''
        checks MOCK_SENT_TO_OPERATOR env varibale
        NOTE:- MOCK_SENT_TO_OPERATOR should be 1 for prod instances
    '''
    try:
        if int(os.environ.get('MOCK_SENT_TO_OPERATOR')):
            return False
        else:
            return True
    except:
        return True


def generate_trade_meta_map():

    for split_file in os.listdir(trade_segment_split_path):
        file_path = os.path.join(trade_segment_split_path, split_file)

        row_count_args = (file_path, )
        is_success, output, error_mess = ShellUtils.get_file_row_count(*row_count_args)
        if not is_success:
            print(error_mess)
            # Send email
            return


def get_segment_id_name_map(collection_name, master_db):
    segment_collection_name = convert_camel_case_to_snake_case(MessagingGroup.__name__)
    query = {"model_name": segment_collection_name}
    projection = {"name": 1, "_id": 0, "id": 1}
    segment_list = list(master_db[collection_name].find(query, projection))
    return {segment["id"]: segment["name"] for segment in segment_list}


# Make this code parallel if large time is taken to concatenate files
def merge_order_segment_files(command_processing_date_str):
    """
    Merge common intersection segment files for order on master server copied from slaves
    :return:
    """



    master_db = get_master_db_connection()
    processing_date_dir = get_directory_name_from_date_str(command_processing_date_str)
    # order_list = get_active_trade_meta()
    collection_name = get_collection_name_for_processing_date(DATABASE_SNAPSHOT, str(command_processing_date_str))
    processing_date = datetime.datetime.strptime(command_processing_date_str, DATE_FORMAT_Y_M_D)
    # order_list = get_active_trade_meta()

    # Get Active orders to process for processing date
    order_list = get_active_trade_for_processing_date(master_db, processing_date)


    segment_name_dict = get_segment_id_name_map(collection_name, master_db)

    print (f'command processing date = {command_processing_date_str}')
    # master/swap/order_segment/processing_date/
    # Path in master machine where intersection files are copied from worker machines
    master_swap_path = get_directory_path_for_processing_date(COPY_ORDER_SEGMENT_DIR_PATH, processing_date_dir)

    # Path where copied files will be merged for orders
    # master/swap/merged_order_segment/processing_date/
    processing_date_merged_path = get_directory_path_for_processing_date(MERGED_ORDER_SEGMENT_DIR_PATH, processing_date_dir)

    operator_segment_path = SEGMENT_DISH_DIR_PATH

    create_dir(processing_date_merged_path)
    create_dir(operator_segment_path)

    file_prefix_dict = dict()
    for order_meta_dict in order_list:
        order_id = str(order_meta_dict['trade_id'])
        master_order_segment_path = os.path.join(master_swap_path, order_id)

        all_files = os.listdir(master_order_segment_path)

        op_info_dict = {i.split('__')[0]:{j.split('__')[1]:[os.path.join(master_order_segment_path, k) for k in all_files if i.split('__')[0]+ '__' + j.split('__')[1] in k] for j
            in all_files if i.split('__')[0] ==  j.split('__')[0]} for i in all_files}
        file_prefix_dict[order_id] = op_info_dict

    # file_prefix_dict =
    # {
    #     1: {
    #         "dish": {
    #             "5_6": [
    #                 "/master/swap/order_segment/2020_12_13/dish__5_6___slave2.csv",
    #                 "/master/swap/order_segment/2020_12_13/dish__5_6___slave1.csv",
    #             ]
    #         },
    #         "xandr": {
    #             "5_6": ["/master/swap/order_segment/2020_12_13/xandr__5_6___slave2.csv"],
    #             "5": [
    #                 "/master/swap/order_segment/2020_12_13/xandr__5_6___slave2.csv",
    #                 "/master/swap/order_segment/2020_12_13/xandr__5___slave1.csv",
    #             ],
    #         },
    #     }
    # }


    merge_start_time = time.time()
    number_of_files_to_merge = 0


    for order_id, meta_info in file_prefix_dict.items():
        for operator, order_segment_prefix_dict in meta_info.items():
            merged_order_path = os.path.join(processing_date_merged_path, str(order_id), operator)
            operator_order_segment_path = os.path.join(operator_segment_path, str(order_id), operator)
            create_dir(merged_order_path)
            create_dir(operator_order_segment_path)

            order_concatenate_arg_list = list()

            for segment_prefix, file_list in order_segment_prefix_dict.items():
                merge_path = os.path.join(merged_order_path, segment_prefix + FILE_FORMAT.CSV)
                # check if all the slaves file doesn't have any entry
                total_entries_for_all_slaves = reduce(lambda x, y: x + y,
                                                    [os.stat(slave_file).st_size for slave_file in file_list])
                if total_entries_for_all_slaves == 0:
                    continue

                # Bench mark this for 250 Million else add multiprocess to this logic
                merge_args = (file_list, merge_path)
                order_concatenate_arg_list.append(merge_args)
                number_of_files_to_merge += 1

            initiate_concatenate_process(order_concatenate_arg_list)        # shell command to concatenate the files from slaves into one

            update_merged_file_to_trade_tracker(merged_order_path)          # no funtionalty as of now

            update_processed_trades_state(order_id, CampaignStage.FILE_MERGED)      # updates mongo tracker

    merge_time = time.time() - merge_start_time
    print (f'file concatenation number = {number_of_files_to_merge}')
    print (f'Total time taken to concatenate files = {merge_time}')


def update_merged_file_to_trade_tracker(merged_order_path):
    '''
        Walk all files in directory and update trade tracker master key 'merged file'
        Not adding now can be added in future
    '''
    pass

def initiate_concatenate_process(files_concate_args_list):

    from billiard import Pool
    pools = Pool(SWAP_GENERATION_POOL_SIZE)
    pools.map(start_concatenate_process, [merge_args for merge_args in files_concate_args_list])
    pools.close()
    pools.terminate()


def start_concatenate_process(merge_args):

    '''
        ['/master/swap/order_segment/2020_12_13/39/77__slave2.csv',
        '/master/swap/order_segment/2020_12_13/39/77__slave1.csv']

        Concatenate same prefix files to one file

    '''

    concatenate_start_time = time.time()
    is_success, error_message = ShellUtils.concatenate_file_list(*merge_args)
    print (f'time taken to concatenate file is {time.time() - concatenate_start_time}')

    # Add Exception Handler
    if not is_success:
        sentry_capture_message(message=error_message)
        print('error merging file = ', error_message)

def update_order_file(order_id, file_paths):
    '''
        updates or refresh the OrderFile records for input order id
    '''
    order_tag_file = list()
    OrderFiles.objects.filter(trade_id = order_id).delete()
    for merged_file_path in file_paths:
        icdx_order_data = dict()
        new_file_loc = os.path.join(ICDX_DIR_PATH, str(order_id), MASTER_TAGS, merged_file_path.split('/')[-1])
        if not os.path.exists(os.path.dirname(new_file_loc)):
            create_dir(os.path.dirname(new_file_loc))

        records_to_update = {
            'filename' : new_file_loc.split('/')[-1],
            's3_file_path' : '',
            'directory_path' : new_file_loc,
            'trade_id' : order_id
        }
        ShellUtils.copy(merged_file_path, new_file_loc)
        order_obj ,success = OrderFiles.objects.get_or_create(**records_to_update)

        if not success:
            message = 'could not create order file for ' + str(order_obj.id) + merged_file_path
            print(message)
            sentry_capture_message(message=message)
            continue

        if AWS_UPLOAD: is_success, message, s3_path = upload_order_file_to_s3(merged_file_path, order_obj)

        row_count_args = (merged_file_path, )
        _, output, _ = ShellUtils.get_file_row_count(*row_count_args)
        row_count = int(output)
        icdx_order_data['row_count'] = row_count
        icdx_order_data['file_path'] = new_file_loc
        order_tag_file.append(icdx_order_data)

    if AWS_UPLOAD: update_processed_trades_state(order_id,  '.'.join(['tags', MASTER_TAGS, 'checks', CampaignStage.FILE_UPLOADED_TO_S3]))
    return order_tag_file


def upload_order_file_to_s3(merged_file_path, order_obj):
    '''
    uploads order file to s3
    '''
    import uuid
    from django.conf import settings
    from core.helper.common_helper import get_hash_key_by_filename, upload_file

    directory_path = os.path.join(settings.GROUP_FILE_PATH,'OrderFiles')
    dest_file_name = merged_file_path.split('/')[-1]
    hash_key = get_hash_key_by_filename(os.path.join(merged_file_path, dest_file_name))
    s3_path = os.path.join(os.path.join(directory_path,str(order_obj.trade_id)), hash_key, '.'.join([uuid.uuid5(uuid.uuid4(), dest_file_name.replace('.csv','')).hex, 'csv']))

    s3_file_obj = upload_file(file_path=order_obj.directory_path,
            s3_file_path=order_obj.s3_file_path,
            bucket_name=settings.S3_ADCURATIO_ACXIOM,
            app_name=order_obj._meta.app_label,
            model_name=order_obj.__class__.__name__,
            column_name="s3_file_path",
            model_id=order_obj.id)

    if s3_file_obj['success']:
        message = 'could not upload file to s3'
        sentry_capture_message(message=message)
        return False, message, s3_path

    order_obj.s3_file_path = s3_path
    order_obj.save()

    return True, None, s3_path

def mongo_update_cmt(command_processing_date_str):
    """
    final update on mongo tracker and CMT obj
    """

    master_db = get_master_db_connection()
    processing_date = datetime.datetime.strptime(command_processing_date_str, DATE_FORMAT_Y_M_D)
    order_list = get_active_trade_for_processing_date(master_db, processing_date)

    for order_obj in order_list:
        if all([op['checks'][CampaignStage.PROCESSED] for op in order_obj['tags'].values()]):
            update_processed_trades_state(order_obj['trade_id'], CampaignStage.PROCESSED)

def create_order_files(processing_date_str):

    master_db = get_master_db_connection()
    processing_date_dir = get_directory_name_from_date_str(processing_date_str)
    processing_date = datetime.datetime.strptime(processing_date_str, DATE_FORMAT_Y_M_D)
    active_trade_list = get_active_trade_for_processing_date(master_db, processing_date, MASTER_TAGS)
    processing_date_merged_path = get_directory_path_for_processing_date(MERGED_ORDER_SEGMENT_DIR_PATH, processing_date_dir)

    for order_obj in active_trade_list:
        order_id = order_obj['trade_id']
        merged_order_path = os.path.join(processing_date_merged_path, str(order_id), MASTER_TAGS)
        file_paths = [os.path.join(merged_order_path, filename) for filename in os.listdir(merged_order_path)]
        files_row_count = update_order_file(order_id, file_paths)
        key = {'trade_id': order_id, 'processing_date': processing_date}
        file_projection = '.'.join(['tags', MASTER_TAGS, 'tag_files'])
        icdx_flag_projection = '.'.join(['tags', MASTER_TAGS, 'checks', CampaignStage.ICDX_CREATED])
        processed_flag_projection = '.'.join(['tags', MASTER_TAGS, 'checks', CampaignStage.PROCESSED])
        master_db[TRADE_TRACKER].update(key, {'$set': {file_projection: files_row_count, icdx_flag_projection: True, processed_flag_projection: True}})


def is_distributor_processed(master_db, processing_date, data_distributor):
    ''' checks if tags are processed for data distributor
    '''
    key = {'processing_date': processing_date}
    processed = '.'.join(['tags', data_distributor, 'checks', CampaignStage.PROCESSED])
    return not all(master_db[TRADE_TRACKER].find(key).distinct(processed))

def create_distributor_tags(command_processing_date_str):
    '''
        method to create icdx for trade operators
    '''

    master_db = get_master_db_connection()
    processing_date = datetime.datetime.strptime(command_processing_date_str, DATE_FORMAT_Y_M_D)

    # This queue command will be operator specific.
    if is_distributor_processed(master_db, processing_date, MASTER_TAGS):
        print("Processing for Master Tags")
        create_order_files(command_processing_date_str)

    if is_distributor_processed(master_db, processing_date, OPERATOR_NAME.DISH):
        print("Processing for Dish")
        # create icdx files
        create_icdx_files_start_time = time.time()
        create_icdx_files(command_processing_date_str)
        print (f'create_icdx_files creation time  = {time.time() - create_icdx_files_start_time}')

        from engine.helper.campaign import sync_campaign
        sync_campaign_start_time = time.time()
        # sync files generated to s3 bucket
        sync_campaign(command_processing_date_str)
        print (f'sync_campaign time  = {time.time() - sync_campaign_start_time}')

    if is_distributor_processed(master_db, processing_date, OPERATOR_NAME.XANDR):
        print("Processing for Xandr")
        from xandr.helper import create_icdx_for_directtv
        create_icdx_for_directtv(command_processing_date_str)

    if is_distributor_processed(master_db, processing_date, OPERATOR_NAME.VIZIO):
        print("Processing for Vizio")
        from audience.helpers.trade_helper import create_icdx_for_vizio
        create_icdx_for_vizio(command_processing_date_str)

    mongo_update_cmt(command_processing_date_str)

