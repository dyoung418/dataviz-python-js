# api/settings.py

# Optional MONGO variables
#MONGO_HOST = 'localhost'
#MONGO_PORT = 27017
#MONGO_USERNAME = 'user'
#MONGO_PASSWORD = 'user'

URL_PREFIX = 'api'
MONGO_DBNAME = 'nobel_prize'
DOMAIN = {'winners_all':{
    #'item_title': 'winners',
    'schema':{
        'country':{'type':'string'},
        'category':{'type':'string'},
        'name':{'type':'string'},
        'year':{'type':'integer'},
        'gender':{'type':'string'},
        'mini_bio':{'type':'string'},
        'bio_image':{'type':'string'}
    }
}}

X_DOMAINS = '*' # allow CORS requests from all domains
#X_DOMAINS = 'http://localhost:8080' # allow CORS requests from this domain
HATEOAS = False
PAGINATION = False
