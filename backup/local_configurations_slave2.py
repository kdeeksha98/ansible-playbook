import redis


MONGO_DATABASE = "adcuratio_slave2"
REDIS_DB = 'localhost'
VIEWERSHIP_HOST = 'mongodb://test:test@localhost:27017/'
REDIS_PASSWORD = "Adcuratio123"
MONGO_DATABASE = "adcuratio_slave2"
DB_NAME = 'demographics'


class REDIS_POOL():
    ''' This class contains static variable of redis pools'''
    ACXIOM_SHARD_INFO = redis.ConnectionPool(host=REDIS_DB, port=6379, db=9, max_connections=3000, password=REDIS_PASSWORD)
    EXPERIAN_SHARD_INFO = redis.ConnectionPool(host=REDIS_DB, port=6379, db=10, max_connections=3000, password=REDIS_PASSWORD)
    STB_SHARD_INFO = redis.ConnectionPool(host=REDIS_DB, port=6379, db=11, max_connections=3000, password=REDIS_PASSWORD)
    EPSILON_SHARD_INFO = redis.ConnectionPool(host=REDIS_DB, port=6379, db=13, max_connections=3000, password=REDIS_PASSWORD)
    BIT_VECTOR_DATA = redis.ConnectionPool(host=REDIS_DB, port=6379, db=12, max_connections=3000, password=REDIS_PASSWORD)
    OFFSET_DATA = redis.ConnectionPool(host=REDIS_DB, port=6379, db=1, max_connections=3000, password=REDIS_PASSWORD)


DEMOGRAPHICS_DB_SKIP = 500000
DEMOGRAPHICS_DB_SIZE = 500000
POOL_SIZE = 3
BATCH_SIZE = 10000
NUM_WORKER_THREADS = 3