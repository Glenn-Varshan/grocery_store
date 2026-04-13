

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///store.db'
    SECRET_KEY = "dummy secret key"
    SECURITY_PASSWORD_SALT = "dummysalt"
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "dummy header"
    SECURITY_TRACKABLE = True
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = "add redis port here"
    CACHE_REDIS_DB = 3
    CACHE_DEFAULT_TIMEOUT = 300
    

class DevelopmentConfig(Config):
    DEBUG = True