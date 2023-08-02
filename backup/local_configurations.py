import redis

MONGO_HOST = 'mongodb://test:test@localhost:27017/'
VIEWERSHIP_HOST = 'mongodb://test:test@localhost:27017/'
REPORTING_HOST = 'mongodb://localhost:27018/'
MONGO_DATABASE = "adcuratio_full"
REDIS_DB = 'localhost'
REDIS_PASSWORD = "Adcuratio123"
REDIS_STB_MAP_POOL = redis.ConnectionPool(host=REDIS_DB, port=6379, db=0, max_connections=5000, password=REDIS_PASSWORD)
REDIS_BIT_VECTOR_POOL = redis.ConnectionPool(host=REDIS_DB, port=6379, db=1, max_connections=5000, password=REDIS_PASSWORD)
# CELERY_BROKER_URL = 'redis://localhost:6379/2'
# BROKER_URL = CELERY_BROKER_URL

MONGO_ADMIN_USERNAME = "test"
MONGO_ADMIN_PASSWORD = "test"
MONGO_AUTHENTICATION_DATABASE = "admin"

MONGO_HOST_MASTER = MONGO_HOST
MONGO_DATABASE_MASTER = MONGO_DATABASE

MONGO_DATABASE_PENDING = "adcuratio_pending"
REPORTING_DATABASE = "reporting_adcuratio"
GROUP_FREQUENCY = "group_frequency"
TRADE_ELIGIBILITY_MAP_COLLECTION = "trade_eligibility_map"
AGGREGATE_COLLECTION = "aggregations"
PREDICTION_COLLECTION = "prediction_table_yesterday"
PREDICTION_UPDATE_COLLECTION = "prediction_table"
STB_COLLECTION = "stb"
ADSPOT_COLLECTION = "adspot"
NETWORK_FILTER_COLLECTION = "network_filter"
TRADE_COLLECTION = "trade"
ADID_COLLECTION = "adid"
TEMPORARY_PACING_COLLECTION = "temp_pacing_table"
PACING_COLLECTION = "pacing_table"
PACING_COLLECTION_YESTERDAY = PACING_COLLECTION + "_yesterday"
PACING_COLLECTION_GLOBAL = PACING_COLLECTION + "_global"
SWAP_COLLECTION = "swap"
DAYSPLIT_META_COLLECTION = "day_split_meta"
SWAP_COLLECTION_YESTERDAY = SWAP_COLLECTION + "_yesterday"  # this cannot be changed without changing seed_feedback.js
TEMP_SWAP_FEEDBACK_COLLECTION = "swap_temp_feedback"
FEEDBACK_TRACKER_COLLECTION = "feedback_tracker"
DAILY_FEEDBACK_TRACKER_COLLECTION = "daily_feedback_tracker"
EXCLUSION_BY_NETWORK = "exclusion_by_network"
SWAP_INTERSECTION_COLLECTION = "swap_intersection"
SEGMENT_REACH_COLLECTION = "segment_reach"

TEMP_SWAP_COLLECTION = "swap_temp"
PRE_FEEDBACK_COLLECTION = "pre_feedback"
POST_FEEDBACK_COLLECTION = "eod_feedback"
SWAP_PROJECTION_COLLECTION = "swap_projection"
MONGO_FEEDBACK_SEED_PATH = "/home/nikhil/adcuratio_v2/engine/seed_feedback.js"

GROUP_STB_MAP = 'group_stb_map'
REPORTING_DATA = 'reporting_data'

BACKUP_PATH = "/home/nikhil/S3_BACKUP/"
ARCHIVE_BACKUP = "ARCHIVE_BACKUP/"
CMT_SUMMARY = "cmt_summary"
# Postgres
#DB_NAME = 'experian_exp'
DB_NAME = 'demographics'
SWAP_CMT = 'swap_cmt'


FTP_PATH = "/home/yashas/adcuratio/adc_storage/mnt2/drtuser3/"
EOD_PATH = FTP_PATH + "EOD/"
POLLING_FEEDBACK_PATH = FTP_PATH + "POLLING/"

FTP_INTERNAL_PATH = "/home/yashas/adcuratio/adc_storage/mnt2/ftp_internal/"
EOD_INTERNAL_PATH = FTP_INTERNAL_PATH + "EOD/"
POLLING_FEEDBACK_INTERNAL_PATH = FTP_INTERNAL_PATH + "POLLING/"
PREDICTION_BATCH_SIZE = 1000

BIT_VECTOR_PATH = "/home/yashas/adcuratio/adc_storage/mnt2/bit_vectors/"
SEGMENT_BIT_VECTOR_PATH = BIT_VECTOR_PATH + "segment/"

S3_BACKUP_PATH = FTP_INTERNAL_PATH + "MASTER/"
OPERATOR_ID=1
SERVER_NAME="master"

