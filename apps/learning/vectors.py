from redis import Redis
from nearpy.storage import RedisStorage
from nearpy.hashes import RandomBinaryProjections
from nearpy import Engine


# Create redis storage adapter
redis_object = Redis(host='localhost', port=6379, db=0)
redis_storage = RedisStorage(redis_object)

# Get hash config from redis
config = redis_storage.load_hash_configuration('MyHash')

if config is None:
    # Config is not existing, create hash from scratch, with 10 projections
    lshash = RandomBinaryProjections('MyHash', 10)
else:
    # Config is existing, create hash with None parameters
    lshash = RandomBinaryProjections(None, None)
    # Apply configuration loaded from redis
    lshash.apply_config(config)

# Create engine for feature space of 100 dimensions and use our hash.
# This will set the dimension of the lshash only the first time, not when
# using the configuration loaded from redis. Use redis storage to store
# buckets.
engine = Engine(100, lshashes=[lshash], storage=redis_storage)

# Do some stuff like indexing or querying with the engine...

# Finally store hash configuration in redis for later use
redis_storage.store_hash_configuration(lshash)