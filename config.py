import os

_basedir = os.path.abspath(os.path.dirname(__file__))


DEBUG = True
#DATABASE = 'n.db'

SECRET_KEY = os.urandom(24)

#DATABASE_PATH = os.path.join(_basedir, DATABASE)
SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:root@localhost/connection_proj?charset=utf8&use_unicode=0"
SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')

ERROR_LOG_PATH = "/tmp/err.log"

# email server
MAIL_SERVER = 'smtp-mail.outlook.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'navaneethan.r@reallex.in'
MAIL_PASSWORD = '******'


# administrator list
ADMINS = ['navaneethan.r@reallex.in']
OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
