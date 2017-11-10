# api/settings.py

# Optional MONGO variables
#MONGO_HOST = 'localhost'
#MONGO_PORT = 27017
#MONGO_USERNAME = 'user'
#MONGO_PASSWORD = 'user'

URL_PREFIX = 'api'
MONGO_DBNAME = 'nobel_prize'
DOMAIN = {'winners':{
    'schema':{
        'country':{'type':'string'},
        'category':{'type':'string'},
        'name':{'type':'string'},
        'year':{'type':'string'},
        'gender':{'type':'string'}
    }
}}

