import os
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'Sm9obiBTY2hyb20ga2lja3MgYXNz'
    STRIPE_API_KEY = 'SmFjb2IgS2FwbGFuLU1vc3MgaXMgYSBoZXJv'
    # Post Per Page
    POSTS_PER_PAGE = 2
    # ADMIN USERNAME
    ADMIN_ROLE='Admin'
    ADMIN_FIRSTNAME='Admin'
    ADMIN_LASTNAME='Test'
    ADMIN_EMAIL='admin@example.com'
    ADMIN_PASSWORD='Password1'
    # Flask Security
    SECURITY_LOGIN_URL = '/user/login'
    # SECURITY_LOGIN_USER_TEMPLATE = '/login.html'
    SECURITY_PASSWORD_SINGLE_HASH = True
    SECURITY_PASSWORD_HASH	= 'sha512_crypt'
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_DEFAULT_REMEMBER_ME = True
    SECURITY_CHANGEABLE = True
    SECURITY_CHANGE_URL = '/profile/change'
    # SECURITY_SUBDOMAIN = 'security'
    # Mail Configuration
    MAIL_SERVER = 'mail.apptester.net'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'admin@apptester.net'
    MAIL_PASSWORD = '41nw0PpT'
    SECURITY_EMAIL_SENDER  = MAIL_USERNAME
    #LANGUAGES
    LANGUAGES = {
        'en': 'English',
        'ar': 'Arabic'
    }

    # Google Analtics
    GA_TRACKING_ID = 'UA-120515428-1'

    LOGGING_FILEPATH = os.path.abspath(os.path.join(__file__,'../logging.yml'))

    ASSETS_FILEPATH = os.path.abspath(os.path.join(__file__,'../assets.yml'))

    GOOGLE_KEY_FILEPATH = os.path.abspath(os.path.join(__file__, '../My Project 3892-61c93430b4e5.json'))

class ProductionConfig(Config):
    SERVER_NAME='apptester.net'
    POSTS_PER_PAGE = 10
    #Production datebase setup phpmyadmin
    SQLALCHEMY_DATABASE_URI = 'mysql://appteste_root:$vsWCII5%^HY@localhost:2083/appteste_flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning
    WTF_CSRF_ENABLED = True

class DevelopmentConfig(Config):
    DEBUG = True
    SERVER_NAME='localhost:5000'
    #development datebase setup phpmyadmin
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = True    # Avoids SQLAlchemy warning
    WTF_CSRF_ENABLED = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = True    # Avoids SQLAlchemy warning
    WTF_CSRF_ENABLED = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestingConfig
}
