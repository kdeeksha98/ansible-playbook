import redis
import os
from core.constants import DISH_LOG_FILE_PATH, XANDR_LOG_FILE_PATH, VIZIO_LOG_FILE_PATH

SERVER_DESC = "LOCAL"
MASTER_IP = "xxx.xxx.xxx.xxx"

MILLION = 1000000
THOUSAND = 1000
##########################
# DB Settings
##########################
# AUTH
MONGO_ADMIN_PASSWORD = "test"
MONGO_ADMIN_USERNAME = "test"
MONGO_AUTHENTICATION_DATABASE = "admin"
REDIS_PASSWORD = "Adcuratio123"
REDIS_PASSWORD_MASTER = "Adcuratio123"

# URLS
MONGO_HOST_NAME = "localhost"
MONGO_HOST = 'mongodb://' + MONGO_ADMIN_USERNAME + ':' + MONGO_ADMIN_PASSWORD + '@localhost:27017/'
MONGO_HOST_MASTER = 'mongodb://' + MONGO_ADMIN_USERNAME + ':' + MONGO_ADMIN_PASSWORD + '@localhost:27017/'
REDIS_DB = 'localhost'
REDIS_DB_MASTER = 'localhost'
MONGO_EXPORT_HOST = "localhost"
REPORTING_HOST = 'mongodb://localhost:27018/'
VIEWERSHIP_HOST = 'mongodb://' + MONGO_ADMIN_USERNAME + ':' + MONGO_ADMIN_PASSWORD + '@54.86.125.43:27017'
VIEWERSHIP_HOST_BACKUP = "54.86.125.43:27017"
MONGO_HOST_SLAVES = {
    "1": 'mongodb://' + MONGO_ADMIN_USERNAME + ':' + MONGO_ADMIN_PASSWORD + '@localhost:27017/',
    "2": 'mongodb://' + MONGO_ADMIN_USERNAME + ':' + MONGO_ADMIN_PASSWORD + '@localhost:27017/'
}
# DATABASES
DB_NAME = 'demographics'  # Postgres demographicsce
MONGO_DATABASE = "adcuratio_full"
MONGO_DATABASE_MASTER = "adcuratio_full"
MONGO_DATABASE_SLAVES = {
    "1": "adcuratio_slave1",
    "2": "adcuratio_slave2"
}
VIEWERSHIP_DATABASE = "adcuratio_test"  # mongo
COMMAND_TRACKER = "command_tracker"
TRADE_TRACKER = "trade_tracker"
SHOW_TRADE_ADID_TRACKER = "show_trade_adid_tracker"

# Used for debugging purpose
TRADE_SWAP_SUMMARY_TRACKER = 'trade_swap_summary'


class REDIS_POOL():
    ''' This class contains static variable of redis pools'''
    ACXIOM_SHARD_INFO = redis.ConnectionPool(host=REDIS_DB, port=6379, db=5, max_connections=3000,
                                             password=REDIS_PASSWORD)
    EXPERIAN_SHARD_INFO = redis.ConnectionPool(host=REDIS_DB, port=6379, db=6, max_connections=3000,
                                               password=REDIS_PASSWORD)
    EPSILON_SHARD_INFO = redis.ConnectionPool(host=REDIS_DB, port=6379, db=9, max_connections=3000,
                                              password=REDIS_PASSWORD)
    STB_SHARD_INFO = redis.ConnectionPool(host=REDIS_DB, port=6379, db=7, max_connections=3000, password=REDIS_PASSWORD)
    BIT_VECTOR_DATA = redis.ConnectionPool(host=REDIS_DB, port=6379, db=8, max_connections=3000,
                                           password=REDIS_PASSWORD)
    OFFSET_DATA = redis.ConnectionPool(host=REDIS_DB, port=6379, db=1, max_connections=3000, password=REDIS_PASSWORD)


##########################
# Celery specific settings
##########################
CELERY_BROKER_URL = "redis://:" + REDIS_PASSWORD + "@localhost:6379/2"
CELERY_RESULT_BACKEND = "redis://:" + REDIS_PASSWORD + "@localhost:6379/3"
FLOWER_API_ROOT = "http://localhost:5555/api"
TOTAL_NUMBER_OF_SLAVES = 2

##########################
# MONGO COLLECTIONS
##########################
DB_TABLE = 'experian'  # Postgres demographics
# CMT
CMT_SUMMARY = "cmt_summary"
DAILY_FEEDBACK_TRACKER_COLLECTION = "daily_feedback_tracker"
FEEDBACK_TRACKER_COLLECTION = "feedback_tracker"
SEGMENT_TRACKER_COLLECTION = "segment_tracker"

# Number of successful swaps generated for a given segment on daily basis
SEGMENT_RECEIVE_COUNTER = "segment_receive_counter"

SEGMENT_REACH_COLLECTION = "segment_reach"
MG_TRACKER_COLLECTION = "mg_tracker"
SWAP_CMT = 'swap_cmt'
SWAP_CMT_YESTERDAY = 'swap_cmt_yesterday'
SWAP_CMT_OUT = "swap_cmt_out"
SWAP_INTERSECTION_COLLECTION = "swap_intersection"
SWAP_PROJECTION_COLLECTION = "swap_projection"
PREDICTION_COLLECTION = "prediction_table_yesterday"
PREDICTION_UPDATE_COLLECTION = "prediction_table"
PREDICTION_AGGREGATION_COLLECTION = "prediction_aggregation_collection"
REPORTING_DATABASE = "reporting_adcuratio"

DATA_PROVIDER_SEGMENT_TRACKER = "data_provider_segment_tracker"
CMT_PERCENTAGE = "cmt_percentage"
DATABASE_SNAPSHOT = "database_snapshot"
DATABASE_SNAPSHOT_YESTERDAY = "database_snapshot_yesterday"
DEBUG_TRACKER_COLLECTION = "debug_tracker"
SWAP_EXPORT_TRACKER = "swap_export_tracker"
ADMIN_LOG_TRACKER = "admin_log_tracker"
VEHICLE_MAKE = "vehicle_make"
VEHICLE_MODEL = "vehicle_model"


##########################
# Engine Configurations
##########################
MIN_HOUSEHOLD_MEMBERS = 1
MAX_HOUSEHOLD_MEMBERS = 9
DEMOGRAPHICS_DB_SKIP = 10 * MILLION
DEMOGRAPHICS_DB_SIZE = 100 * MILLION
BATCH_SIZE = 100 * THOUSAND
BATCH_SIZE_1M = MILLION
POOL_SIZE = 32
SWAP_GENERATION_POOL_SIZE = 1
ARCHIVE_POOL_SIZE = 5
NUM_WORKER_THREADS = 64
PREDICTION_POOL_SIZE = 32
PREDICTION_BATCH_SIZE = 5000
POLLING_FEEDBACK_BATCH_SIZE = 100000
PREDICTION_EOD_BATCH_SIZE = 1000


#40K/250M
TAG_THRESHOLD = 0.0016
THRESHOLD_VALUE = int(TAG_THRESHOLD * DEMOGRAPHICS_DB_SIZE)

#Prod threshold
DISH_TAG_THRESHOLD = 40 * THOUSAND

# Control flags
RETARGETING_ALLOWED = True
ROUND_ROBIN_ALLOWED = True
VIEWERSHIP_FILTER = True
POLLING_FILTER = False
PREDICTION_THRESHOLD = 0.2  # 1.) all stb ids 2.) greyzone stb ids 3.)
POPULATE_STB_REDIS_DATA = True
POPULATE_ACXIOM_REDIS_DATA = True
POPULATE_EXPERIAN_REDIS_DATA = True
POPULATE_EPSILON_REDIS_DATA = True
OPS_VALIDATION_REQUIRED = True
CHANNEL_ADID_APPROVAL_REQUIRED = False
IS_SWAP_INTERSECTION = True
AWS_UPLOAD = True

SWAP_START_HOUR = 6
SWAP_END_HOUR = 23
SAFE_PERIOD_FOR_SWAPS_IN_MINUTES = 120

DEBUG_DASHBOARD_RETRIES = 3

# Number of swaps queued before inserting in swap_cmt collection
SWAP_INSERTION_THRESHOLD = 1000
SEGMENT_SPLIT_LENGTH = 2

##########################
# Code logic constants
##########################
ENGINE_PEM_FILE = 'scripts/docker/docker_pem/engine.pem'

STORAGE_DIR = "/home/yashas/adcuratio/adc_storage/mnt2"
LOG_DIR = "/home/yashas/adcuratio/adc_storage/mnt2/logs"

# pem directory
PEM_DIR = "pem"
PEM_PATH = os.path.join(STORAGE_DIR, PEM_DIR)
PEM_FILE = "key.pem"

DATA_PROVIDER_LIST = ['ACXIOM', 'EXPERIAN', 'STB', 'EPSILON']

DATA_PROVIDER_HEADER_DICT = {
    'ACXIOM': ['ACXIOM_ID', 'ACXIOM_STB_ID', 'OPERATOR_ID'],
    'EXPERIAN': ['EXPERIAN_ID', 'EXPERIAN_STB_ID', 'OPERATOR_ID'],
    'STB': ['STB_ID', 'OPERATOR_ID']
}

DATA_PROVIDER_PREFIX_DICT = {
    'ACXIOM': 'acxiom_',
    'EXPERIAN': 'experian_',
    'STB': 'stb_'
}

PROCESS_VIEWERSHIP = False

DOCKER_ID = "e892a6c037c4"

SERVER_MODE = "testing"
DATA_LOAD_FOLDER_PATH = '/opt/docker_test/docker_folder/data_load'
DESTINATION_FOLDER = "/home/ubuntu/docker_test/docker_folder/data_load/"

try:
    OPERATOR_ID = os.environ["OPERATOR_ID"]
    if os.environ.get('DEPLOYMENT_MODE') == 'DOCKER':
        if os.environ["SERVER_TYPE"] == "MASTER":
            SERVER_NAME = "MASTER"
            from engine.docker_configurations import *
        if os.environ["SERVER_TYPE"] == "SLAVE":
            SERVER_NAME = "SLAVE" + os.environ["SLAVE_ID"]
            from engine.docker_configurations_slave import *
    else:
        SERVER_NAME = os.environ["SERVER_NAME"]
        if os.environ["SERVER_NAME"] == "MASTER":
            from engine.local_configurations import *
        elif os.environ["SERVER_NAME"] == "SLAVE1":
            from engine.local_configurations_slave1 import *
        elif os.environ["SERVER_NAME"] == "SLAVE2":
            from engine.local_configurations_slave2 import *
except:
    import traceback

    print(traceback.format_exc())
    pass

##########################
# File path configurations
##########################

POLLING_DIR = "polling"
EOD_DIR = "eod"
SERVER_NAME_LOWER = SERVER_NAME.lower()
SERVER_STORAGE_PATH = os.path.join(STORAGE_DIR, SERVER_NAME_LOWER)

EDI_DIR = 'edi'
CREATIVES_DIR = 'creatives'

EDI_STORAGE_PATH = os.path.join(SERVER_STORAGE_PATH, EDI_DIR)
CREATIVES_STORAGE_PATH = os.path.join(SERVER_STORAGE_PATH, CREATIVES_DIR)

S3_BACKUP_DIR = "s3_backup"
S3_BACKUP_PATH = os.path.join(SERVER_STORAGE_PATH, S3_BACKUP_DIR)

S3_FILE_BACKUP_DIR = "file_backup"
S3_FILE_BACKUP_PATH = os.path.join(S3_BACKUP_PATH, S3_FILE_BACKUP_DIR)
S3_POLLING_BACKUP_PATH = os.path.join(S3_FILE_BACKUP_PATH, POLLING_DIR)
S3_EOD_BACKUP_PATH = os.path.join(S3_FILE_BACKUP_PATH, EOD_DIR)

S3_COLLECTION_BACKUP_DIR = "collection_backup"
S3_COLLECTION_BACKUP_PATH = os.path.join(S3_BACKUP_PATH, S3_COLLECTION_BACKUP_DIR)

# A&E logs file path
# Note A&E logs file are used to create trafficking files.
ANE_LOGS_DIR = os.path.join('ftp','ane_logs')
ANE_LOGS_PATH = os.path.join(SERVER_STORAGE_PATH, ANE_LOGS_DIR)
ANE_TRAFFICKING_FILE_DIR = 'ane_trafficking_plan'
ANE_TRAFFICKING_FILE_PATH = os.path.join(SERVER_STORAGE_PATH, ANE_TRAFFICKING_FILE_DIR)

UNIVISION_LOGS_DIR = os.path.join('ftp', 'univision/data/')
UNIVISION_BASE_LOGS_PATH = os.path.join(SERVER_STORAGE_PATH, UNIVISION_LOGS_DIR)

OPERATOR_LOGS_DIR = "operator_logs"
OPERATOR_LOGS_PATH = os.path.join(STORAGE_DIR, OPERATOR_LOGS_DIR)
DISH_PATH = "dish"
XANDR_PATH = "xandr"
VIZIO_PATH = "vizio"
DISH_OPERATOR_LOGS_PATH = os.path.join(SERVER_STORAGE_PATH, OPERATOR_LOGS_DIR, DISH_PATH)
XANDR_OPERATOR_LOGS_PATH = os.path.join(SERVER_STORAGE_PATH, OPERATOR_LOGS_DIR, XANDR_PATH)
VIZIO_OPERATOR_LOGS_PATH = os.path.join(SERVER_STORAGE_PATH, OPERATOR_LOGS_DIR, VIZIO_PATH)

# Dish reports file path
REPORTS_DIR = 'reports'
REPORTS_PATH = os.path.join(SERVER_STORAGE_PATH, REPORTS_DIR)

# s3 backup key
ARCHIVE_BACKUP = "ARCHIVE_BACKUP/"

TMP_DIR_FOR_PROCESSING = os.path.join(SERVER_STORAGE_PATH, "tmp_processing")

FTP_DIR = "ftp"
FTP_PATH = os.path.join(SERVER_STORAGE_PATH, FTP_DIR)

TEMP_LOG_DIR = "temp_logs"
TEMP_LOG_PATH = os.path.join(SERVER_STORAGE_PATH, TEMP_LOG_DIR)

TEMP_POST_LOG_DIR = "temp_post_logs"
TEMP_POST_LOG_PATH = os.path.join(SERVER_STORAGE_PATH, TEMP_POST_LOG_DIR)
EOD_PATH = os.path.join(FTP_PATH, EOD_DIR)
POLLING_FEEDBACK_PATH = os.path.join(FTP_PATH, POLLING_DIR)

FTP_INTERNAL_DIR = "ftp_internal"
FTP_INTERNAL_PATH = os.path.join(SERVER_STORAGE_PATH, FTP_INTERNAL_DIR)

FTP_EOD_INTERNAL_DIR = "eod"
EOD_INTERNAL_PATH = os.path.join(FTP_INTERNAL_PATH, FTP_EOD_INTERNAL_DIR)

FTP_POLLING_INTERNAL_DIR = "polling"
POLLING_FEEDBACK_INTERNAL_PATH = os.path.join(FTP_INTERNAL_PATH, FTP_POLLING_INTERNAL_DIR)

# File based group uploads
FTP_GROUP_DIR = "group"
FTP_GROUP_PATH = os.path.join(FTP_PATH, FTP_GROUP_DIR)

# creative_file path
FTP_CREATIVE_DIR = "creatives"
FTP_CREATIVE_PATH = os.path.join(FTP_PATH, FTP_CREATIVE_DIR)

# creative_thumbnail path
THUMBNAIL_CREATIVE_DIR = "thumbnail_creative"
THUMBNAIL_CREATIVE_PATH = os.path.join(SERVER_STORAGE_PATH, THUMBNAIL_CREATIVE_DIR)

# creative location in ftp server
SFTP_CREATIVE_PATH = '/home/creatives/'

FTP_EDI_DIR = "edi"
INTERNAL_FTP_EDI_PATH = os.path.join(FTP_PATH, FTP_EDI_DIR)

# Adcuratio Asrun File Path
FTP_POST_LOG_DIR = "post_logs"
INTERNAL_FTP_POST_LOG_PATH = os.path.join(FTP_PATH, FTP_POST_LOG_DIR)

BIT_VECTOR_DIR = "bit_vector"
BIT_VECTOR_PATH = os.path.join(SERVER_STORAGE_PATH, BIT_VECTOR_DIR)
SEGMENT_BIT_VECTOR_DIR = "segment"
SEGMENT_BIT_VECTOR_PATH = os.path.join(BIT_VECTOR_PATH, SEGMENT_BIT_VECTOR_DIR)
REACH_SEGMENT_BIT_VECTOR_DIR = "reach_segment"
REACH_SEGMENT_BIT_VECTOR_PATH = os.path.join(BIT_VECTOR_PATH, REACH_SEGMENT_BIT_VECTOR_DIR)
S3_SEGMENT_BACKUP_PATH = os.path.join(S3_FILE_BACKUP_PATH, SEGMENT_BIT_VECTOR_DIR)

PROCESS_PREDICTION_FILE_DIR = "prediction"
DAY_SPLIT_FILE_DIR = "day_split"
MERGED_FILE_DIR = "merged"
SORTED_FILE_DIR = "sorted"
PROCESS_PREDICTION_FILE_PATH = os.path.join(SERVER_STORAGE_PATH, PROCESS_PREDICTION_FILE_DIR)
DAY_SPLIT_FILE_PATH = os.path.join(PROCESS_PREDICTION_FILE_PATH, DAY_SPLIT_FILE_DIR)
MERGED_FILE_PATH = os.path.join(PROCESS_PREDICTION_FILE_PATH, MERGED_FILE_DIR)
SORTED_FILE_PATH = os.path.join(PROCESS_PREDICTION_FILE_PATH, SORTED_FILE_DIR)

DATA_PROCESSING_DIR = "data_processing"
DATA_PROCESSING_PATH = os.path.join(SERVER_STORAGE_PATH, DATA_PROCESSING_DIR)
ACXIOM_DIR = "acxiom_processing"
EPSILON_DIR = "epsilon_processing"
EXPERIAN_DIR = "experian_processing"
STB_DIR = "stb_processing"
ACXIOM_FILE_PATH_FOR_GROUP = os.path.join(DATA_PROCESSING_PATH, ACXIOM_DIR)
EPSILON_FILE_PATH_FOR_SEGMENT = os.path.join(DATA_PROCESSING_PATH, EPSILON_DIR)
EXPERIAN_FILE_PATH_FOR_GROUP = os.path.join(DATA_PROCESSING_PATH, EXPERIAN_DIR)
# Group Files created from filters are stored in this location for processing
FTP_PROVIDER_SEGMENT_DIR = "provider_segment"
FTP_PROVIDER_SEGMENT_DIR_PATH = os.path.join(DATA_PROCESSING_PATH, FTP_PROVIDER_SEGMENT_DIR)
EPSILON_FILE_DIR = 'epsilon_files'
EPSILON_FILE_DIR_PATH = os.path.join(DATA_PROCESSING_PATH, EPSILON_FILE_DIR)
EXPERIAN_FILE_DIR = 'experian_files'
EXPERIAN_FILE_DIR_PATH = os.path.join(DATA_PROCESSING_PATH, EXPERIAN_FILE_DIR)
STB_FILE_PATH_FOR_GROUP = os.path.join(DATA_PROCESSING_PATH, STB_DIR)
SWAP_FILE_DIR = 'swap_files'
SWAP_FILE_PATH = os.path.join(SERVER_STORAGE_PATH, SWAP_FILE_DIR)
SWAP_WITH_FEEDBACK_FILE_DIR = 'swap_files_with_feedback'
SWAP_WITH_FEEDBACK_FILE_PATH = os.path.join(SERVER_STORAGE_PATH, SWAP_WITH_FEEDBACK_FILE_DIR)
S3_SWAP_FILE_BACKUP_PATH = os.path.join(S3_FILE_BACKUP_PATH, SWAP_FILE_DIR)
S3_SWAP_FILE_WITH_FEEDBACK_BACKUP_PATH = os.path.join(S3_FILE_BACKUP_PATH, SWAP_WITH_FEEDBACK_FILE_DIR)
CAMPAIGN_BACKUP_DIR = 'campaign'
CAMPAIGN_BACKUP_PATH = os.path.join(SERVER_STORAGE_PATH, CAMPAIGN_BACKUP_DIR)
OPERATOR_BIN_FILE_DIR = 'operator_bin_files'
OPERATOR_BIN_FILE_DIR_PATH = os.path.join(DATA_PROCESSING_PATH, OPERATOR_BIN_FILE_DIR)
OPERATOR_SEGMENT_FILE_DIR = 'operator_segment_files'
OPERATOR_SEGMENT_FILE_PATH = os.path.join(DATA_PROCESSING_PATH, OPERATOR_SEGMENT_FILE_DIR)
# Trade info sheet file path
CAMPAIGN_INFO_EXCEL_DIR = "campaign_info"
CAMPAIGN_INFO_EXCEL_PATH = os.path.join(SERVER_STORAGE_PATH, CAMPAIGN_INFO_EXCEL_DIR)


class CampaignSyncDir:
    ADSPOT_DIR = 'adspot'
    ICD_FILE_DIR = 'icd'
    CREATIVE_DIR = 'creative'


class CAMAPIGN_BACKUP_TYPE:
    ADSPOT = 'adspot'
    ICD = 'icd'
    CREATIVE = 'creative'


CAMPAIGN_SYNC_LIST = ['adspot', 'icd', 'creative']

# INFRA BACKUP PATH
#
# DB_BACKUP_DIR = "db_backup" + "_" + SERVER_NAME
# DB_BACKUP_DIR_PATH = os.path.join(STORAGE_DIR, DB_BACKUP_DIR)


INFRA_BACKUP_DIR = "backup_directory" + "_" + SERVER_NAME
INFRA_BACKUP_DIR_PATH = os.path.join(STORAGE_DIR, INFRA_BACKUP_DIR)

SERVER_INFRA_BACKUP_POST_SWAP_DIR = "post_swap"
SERVER_INFRA_BACKUP_POST_SWAP_PATH = os.path.join(INFRA_BACKUP_DIR_PATH, SERVER_INFRA_BACKUP_POST_SWAP_DIR)
SERVER_BACKUP_PRE_ETL_DIR = "pre_etl"
SERVER_BACKUP_PRE_ETL_PATH = os.path.join(INFRA_BACKUP_DIR_PATH, SERVER_BACKUP_PRE_ETL_DIR)

SERVER_RESTORE_BACKUP_DIR = "infra_restore_backup"
SERVER_RESTORE_BACKUP_PATH = os.path.join(INFRA_BACKUP_DIR_PATH, SERVER_RESTORE_BACKUP_DIR)

# AWS S3 infra folder dir
S3_INFRA_BACKUP_DIR = "infra_backup"
S3_INFRA_BACKUP_PATH = os.path.join(S3_INFRA_BACKUP_DIR, SERVER_DESC)

S3_CAMPAIGN_INFO_DIR = 'CAMPAIGN'
S3_CAMPAIGN_INFO_PATH = os.path.join(S3_CAMPAIGN_INFO_DIR, SERVER_DESC)

MONGO_BACKUP_DIR = "mongo"
MONGO_BACKUP_PATH = os.path.join(SERVER_INFRA_BACKUP_POST_SWAP_PATH, MONGO_BACKUP_DIR)
REDIS_BACKUP_DIR = "redis"
REDIS_BACKUP_PATH = os.path.join(SERVER_INFRA_BACKUP_POST_SWAP_PATH, REDIS_BACKUP_DIR)
POSTGRES_BACKUP_DIR = "postgres"
POSTGRES_BACKUP_PATH = os.path.join(SERVER_INFRA_BACKUP_POST_SWAP_PATH, POSTGRES_BACKUP_DIR)

SWAP_SEGMENT_DIR = 'swap'
SWAP_SEGMENT_DIR_PATH = os.path.join(SERVER_STORAGE_PATH, SWAP_SEGMENT_DIR)

SWAP_SEGMENT_INTERSECTION_DIR = 'order_segment_intersection'
SWAP_SEGMENT_INTERSECTION_DIR_PATH = os.path.join(SWAP_SEGMENT_DIR_PATH, SWAP_SEGMENT_INTERSECTION_DIR)

SWAP_SEGMENT_INTERSECTION_STB_DIR = 'order_stb'
SWAP_SEGMENT_INTERSECTION_STB_DIR_PATH = os.path.join(SWAP_SEGMENT_DIR_PATH, SWAP_SEGMENT_INTERSECTION_STB_DIR)

MERGED_ORDER_SEGMENT_DIR = 'merged_order_segment'
MERGED_ORDER_SEGMENT_DIR_PATH = os.path.join(SWAP_SEGMENT_DIR_PATH, MERGED_ORDER_SEGMENT_DIR)

SEGMENT_INTERSECTION_SPLIT_DIR = 'split_segment'
SEGMENT_INTERSECTION_SPLIT_PATH = os.path.join(SWAP_SEGMENT_DIR_PATH, SEGMENT_INTERSECTION_SPLIT_DIR)

ICDX_DIR = 'icdx'
ICDX_DIR_PATH = os.path.join(SWAP_SEGMENT_DIR_PATH, ICDX_DIR)

COPY_ORDER_SEGMENT_DIR = 'order_segment'
COPY_ORDER_SEGMENT_DIR_PATH = os.path.join(SWAP_SEGMENT_DIR_PATH, COPY_ORDER_SEGMENT_DIR)

OPERATOR_FILES_DIR = "operator_files"
OPERATOR_FILES_DIR_PATH = os.path.join(SWAP_SEGMENT_DIR_PATH, OPERATOR_FILES_DIR)

INVENTORY_DETAIL_DIR = "inventory_detail"
INVENTORY_DETAIL_DIR_PATH = os.path.join(OPERATOR_FILES_DIR_PATH, INVENTORY_DETAIL_DIR)

ORDER_DETAIL_DIR = "order_detail"
ORDER_DETAIL_DIR_PATH = os.path.join(OPERATOR_FILES_DIR_PATH, ORDER_DETAIL_DIR)

SEGMENT_DETAIL_DIR = "segment_detail"
SEGMENT_DETAIL_DIR_PATH = os.path.join(OPERATOR_FILES_DIR_PATH, SEGMENT_DETAIL_DIR)

SEGMENT_DISH_DIR = "segment_dish_files"
SEGMENT_DISH_DIR_PATH = os.path.join(OPERATOR_FILES_DIR_PATH, SEGMENT_DISH_DIR)

SEGMENT_ORDER_DIR_PATH = 'segment_order_files'
SEGMENT_ORDER_PATH = os.path.join(OPERATOR_FILES_DIR_PATH, SEGMENT_ORDER_DIR_PATH)

DISH_LOG_FILE_MERGED_PATH = os.path.join(DISH_LOG_FILE_PATH, MERGED_FILE_DIR)
XANDR_LOG_FILE_MERGED_PATH = os.path.join(XANDR_LOG_FILE_PATH, MERGED_FILE_DIR)
VIZIO_LOG_FILE_MERGED_PATH = os.path.join(VIZIO_LOG_FILE_PATH, MERGED_FILE_DIR)

# s3 backup folder for operator files.
S3_ORDER_DETAIL_BACKUP_PATH = os.path.join(S3_FILE_BACKUP_PATH, OPERATOR_FILES_DIR, ORDER_DETAIL_DIR)
S3_INVENTORY_DETAIL_BACKUP_PATH = os.path.join(S3_FILE_BACKUP_PATH, OPERATOR_FILES_DIR, INVENTORY_DETAIL_DIR)
S3_SEGMENT_DETAIL_BACKUP_PATH = os.path.join(S3_FILE_BACKUP_PATH, OPERATOR_FILES_DIR, SEGMENT_DETAIL_DIR)

# INFRA TRACKER COLLECTIONS
POST_SWAP_INFRA_TRACKER = 'post_swap_infra_tracker'
PRE_ETL_INFRA_TRACKER = 'pre_etl_infra_tracker'
INFRA_TRACKER_COLLECTION = 'infra_backup_tracker'

EOD_FIELDFILE = "engine/eod_simulation_fieldfile.txt"
SWAP_FIELDFILE = "engine/swap_fieldfile.txt"

# Deal created from test_deal.py are stored in this location for testing
DEAL_FILE_DIR = 'test_deals'
DEAL_FILE_DIR_PATH = os.path.join(STORAGE_DIR, DEAL_FILE_DIR)

# Deal created from test_deal.py are stored in this location for testing
ANELOG_FILE_DIR = 'test_logs'
ANELOG_FILE_DIR_PATH = os.path.join(STORAGE_DIR, ANELOG_FILE_DIR)

##########################
# Prediction Files
##########################

MERGED_PREDICTION_FILE = "merged.xlsx"
SORTED_PREDICTION_FILE = "sorted.xlsx"

##########################
# Code logic constants
##########################

# Fields Meta
SWAP_CMT_FIELDS = ['adspot_timestamp', 'trade_id', 'channel_id', 'company_id', 'campaign_id', 'cm_option',
                   'original_adid', 'swapped_adid', 'adspot_id', 'from_advertiser', 'from_brand',
                   'from_subbrand', 'from_segment', 'to_advertiser', 'to_brand', 'to_subbrand', 'to_segment',
                   'data_provider_type']

META_DATA_FIELDS = ["trade_name", "channel_name", "show_name", "company_name", "campaign_name",
                    "option_description", "original_adid_name", "swapped_adid_name", "adspot_name",
                    "from_advertiser_name", "from_brand_name", "from_subbrand_name", "to_advertiser_name",
                    "to_brand_name", "to_subbrand_name", "from_segment_name", "from_segment_type",
                    "to_segment_name", "to_segment_type"]

SEGMENT_REACH_FIELDS = ["date", "brand_id", "percentage_reached", "impression_reach", "segment_wanted_count",
                        "segment_type",
                        "avg_frequency", "segment_id", "company_id", "reached_count", "sub_brand_id", "segment_level"]

SEGMENT_META_DATA_FIELDS = ["company_name", "brand_name", "subbrand_name", "segment_name"]

SWAP_CMT_OUT_FIELDS = ["adspot_timestamp", "channel_id", "from_advertiser", "campaign_id", "adspot_id", "trade_id",
                       "from_subbrand",
                       "data_provider_type", "from_brand", "to_segment", "to_advertiser", "cm_option", "swapped_adid",
                       "to_subbrand",
                       "company_id", "original_adid", "from_segment", "to_brand", "count"]

CMT_SUMMARY_FIELDS = ["cm_option", "wanted_count", "trade_id", "unwanted_count", "date"]

SEGMENT_RECEIVE_FIELDS = ["date", "segment_receive", "segment_id"]

SLAVE_ARCHIVE_COLLECTIONS = [SWAP_CMT]
VIEWERSHIP_ARCHIVE_COLLECTIONS = [PREDICTION_UPDATE_COLLECTION]
MASTER_ARCHIVE_COLLECTIONS = [DATABASE_SNAPSHOT]

# Master Configuration dirs
MASTER_CONF_DIRS = [SERVER_STORAGE_PATH, S3_BACKUP_PATH, S3_FILE_BACKUP_PATH,
                    S3_POLLING_BACKUP_PATH, S3_EOD_BACKUP_PATH, S3_COLLECTION_BACKUP_PATH,
                    FTP_PATH, EOD_PATH, POLLING_FEEDBACK_PATH, FTP_INTERNAL_PATH, EOD_INTERNAL_PATH, FTP_GROUP_PATH,
                    POLLING_FEEDBACK_INTERNAL_PATH, PROCESS_PREDICTION_FILE_PATH, DAY_SPLIT_FILE_PATH,
                    MERGED_FILE_PATH, SORTED_FILE_PATH, SWAP_FILE_PATH, S3_SWAP_FILE_BACKUP_PATH,
                    S3_SWAP_FILE_WITH_FEEDBACK_BACKUP_PATH, TMP_DIR_FOR_PROCESSING, SWAP_SEGMENT_DIR_PATH,
                    COPY_ORDER_SEGMENT_DIR_PATH, MERGED_ORDER_SEGMENT_DIR_PATH, S3_SEGMENT_DETAIL_BACKUP_PATH,
                    S3_INVENTORY_DETAIL_BACKUP_PATH, S3_ORDER_DETAIL_BACKUP_PATH, ANE_LOGS_PATH, UNIVISION_BASE_LOGS_PATH,
                    ANE_TRAFFICKING_FILE_PATH, SEGMENT_DISH_DIR_PATH, REPORTS_PATH, OPERATOR_LOGS_PATH,
                    INTERNAL_FTP_EDI_PATH, FTP_CREATIVE_PATH, CAMPAIGN_INFO_EXCEL_PATH, INTERNAL_FTP_POST_LOG_PATH,
                    DISH_OPERATOR_LOGS_PATH, XANDR_OPERATOR_LOGS_PATH, VIZIO_OPERATOR_LOGS_PATH,
                    DISH_LOG_FILE_MERGED_PATH, XANDR_LOG_FILE_MERGED_PATH, VIZIO_LOG_FILE_MERGED_PATH]

# Slave Configuration dirs
SLAVE_CONF_DIRS = [SERVER_STORAGE_PATH, S3_BACKUP_PATH, S3_BACKUP_PATH, S3_FILE_BACKUP_PATH,
                   S3_POLLING_BACKUP_PATH, S3_EOD_BACKUP_PATH, S3_COLLECTION_BACKUP_PATH, FTP_GROUP_PATH,
                   FTP_PATH, EOD_PATH, POLLING_FEEDBACK_PATH, FTP_INTERNAL_PATH, EOD_INTERNAL_PATH,
                   POLLING_FEEDBACK_INTERNAL_PATH, BIT_VECTOR_PATH, SEGMENT_BIT_VECTOR_PATH,
                   REACH_SEGMENT_BIT_VECTOR_PATH, PROCESS_PREDICTION_FILE_PATH, DAY_SPLIT_FILE_PATH,
                   MERGED_FILE_PATH, SORTED_FILE_PATH, DATA_PROCESSING_PATH, ACXIOM_FILE_PATH_FOR_GROUP,
                   EXPERIAN_FILE_PATH_FOR_GROUP, EPSILON_FILE_PATH_FOR_SEGMENT, STB_FILE_PATH_FOR_GROUP, SWAP_FILE_PATH,
                   S3_SEGMENT_BACKUP_PATH,
                   S3_SWAP_FILE_BACKUP_PATH, SWAP_WITH_FEEDBACK_FILE_PATH,
                   S3_SWAP_FILE_WITH_FEEDBACK_BACKUP_PATH, TMP_DIR_FOR_PROCESSING, SWAP_SEGMENT_DIR_PATH,
                   SWAP_SEGMENT_INTERSECTION_DIR_PATH, SWAP_SEGMENT_INTERSECTION_STB_DIR_PATH, OPERATOR_SEGMENT_FILE_PATH]

# CELERY BEAT_SCHEDULE CONFIGURATIONS (UTC + 5:30)

# OPS COMMAND
GROUP_5_HOUR_OFFSET = 13
GROUP_5_MINUTE_OFFSET = 0

# FEEDBACK COMMANDS
GROUP_3_HOUR_OFFSET = 20
GROUP_3_MINUTE_OFFSET = 0

# SWAP COMMANDS
GROUP_2_HOUR_OFFSET = 16
GROUP_2_MINUTE_OFFSET = 30

# SNAPSHOT COMMANDS
GROUP_1_HOUR_OFFSET = 16
GROUP_1_MINUTE_OFFSET = 0

# GENERATE SWAP FILE
GROUP_4_OFFSET = '*/10'

# SYSTEM_DATE_UPDATE
SYSTEM_UPDATE_HOUR = 0
SYSTEM_UPDATE_MINUTE = 0

# Demographics User Data directory
DEMOGRAPHICS_DATA_FOLDER = "demographic_data"
ACXIOM_DATA_FOLDER = "acxiom"
EXPERIAN_DATA_FOLDER = "experian"
EPSILON_DATA_FOLDER = "epsilon"
STB_FOLDER = "stb"
STB_ID_DUMP_FOLDER = "stb_id_dump"
DEMOGRAPHICS_DATA_FOLDER_PATH = os.path.join(STORAGE_DIR, DEMOGRAPHICS_DATA_FOLDER)
ACXIOM_DATA_FOLDER_PATH = os.path.join(STORAGE_DIR, ACXIOM_DATA_FOLDER)
EPSILON_DATA_FOLDER_PATH = os.path.join(STORAGE_DIR, EPSILON_DATA_FOLDER)
EXPERIAN_DATA_FOLDER_PATH = os.path.join(STORAGE_DIR, EXPERIAN_DATA_FOLDER)
STB_FOLDER_PATH = os.path.join(STORAGE_DIR, STB_FOLDER)
STB_ID_DUMP_FOLDER_PATH = os.path.join(STORAGE_DIR, STB_ID_DUMP_FOLDER)

# FTP related variables
FTP_USERNAME = 'adcuratio'
FTP_HOSTNAME = os.environ.get('FTP_HOSTNAME')
FTP_PRIVATE_KEY_FILE = 'scripts/docker/docker_pem/adcsftp.pem'
FTP_DISH_DIR_PATH = 'dish/to_dish'
ANE_DIR_PATH = 'ane/uploads'

# test files update_demographics_serial management commands.
TEST_DEMOGRAPHICS_DIR = "test_suite/resources/demo_files/"

# invidi specific api end points

# This api endpoint for window, avail, slot
INVIDI_REST_API_ENDPOINT = 'http://XXXXXXXXXXXXX'
INVIDI_REST_API_USERNAME = 'XXXXXXXXXX'
INVIDI_REST_API_PASSWORD = 'XXXXXXXXXX'

# This api endpoint for order and orderline
INVIDI_SOAP_API_ENDPOINT = 'http://XXXXXXXXXXXXX'
INVIDI_SOAP_API_USERNAME = 'XXXXXXXXXX'
INVIDI_SOAP_API_PASSWORD = 'XXXXXXXXXX'

# configs for network feedback mechanism
WEEKLY_ENTITY_TRACKER = 'week_entity_tracker'
WEEKLY_TRADE_TRACKER = 'week_trade_tracker'
DEFAULT_RATIO = 1.2
NETWORK_PROPAGATION = 10

# onfigs for orderline feedback mechanism
ORDERLINE_FEEDBACK_TRACKER = 'orderline_feedback_tracker'
ORDERLINE_PRAPOGATION_DAYS = 2

# OKTA Api Token

OKTA_API_TOKEN = os.environ.get('OKTA_API_TOKEN')

#Configuration Parameter for Frequency Cap and Frequency Cap percentage
FREQUENCY_CAP = 10
FREQUENCY_CAP_PERCENTAGE = 20

# Local path to store target meta file
LOCAL_DISH_TARGET_FILE_PATH = 'dish_target_meta_file/'

# Vizio s3 information
VIZIO_S3_URL = ""

#config for vizio order tracker collection
VIZIO_ORDER_TRACKER = 'vizio_order_tracker'

# Watermarking module dai-ffmpeg path
DAI_FFMPEG = '/opt/dai-ffmpeg/ffmpeg'
