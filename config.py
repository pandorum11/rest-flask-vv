import os

class Config(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fsdkfd32r234fsdf'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///api_01_service_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ################
    # Flask-Security
    ################

    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "fsdfdfsdfdfsdafds"
    SECRET_KEY_FOR_USER_CREATING = "2.-q6uw$,pqbc[(bM{Sly~ExT/Hkru"
    SECRET_KEY_FOR_USERS_EXTRACTING = "AJ!#r0vU4Ts1A*NO:kCbHUL`1CgInwN"
    SECRET_KEY_FOR_USERS_DELETE = "2.-q6uw$,pqbc[(bM{Sly~ExT/Hkru"