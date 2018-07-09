ENV_NAME = 'prd'

SECRET_KEY = '123'

DEBUG = False

DEBUG_LOGPATH = '/var/log/flaskseed-debug-prd'
LOG_REQ_RES = True

PID_FILE = 'flaskseed'

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'lt7116'
DBHOST = '127.0.0.1'
DBPORT = '3306'
DATABASE = 'ustutor'
SQLALCHEMY_DATABASE_URI = "{0}+{1}://{2}:{3}@{4}:{5}/{6}"\
    .format(DIALECT, DRIVER, USERNAME, PASSWORD, DBHOST, DBPORT, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ECHO = True

DEBUG_TB_INTERCEPT_REDIRECTS=False

# followed upload config items
UPLOAD_FOLDER = '/var/upload'
ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg', 'gif']
# upload file size limitation
MAX_CONTENT_LENGTH = 16 * 1024 * 1024


MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = '13521273258@163.com'
MAIL_PASSWORD = 'wl7116'
MAIL_DEFAULT_SENDER = '13521273258@163.com'

JWT_SECRET = 'src-flask-dev-no-random'
JWT_ALG = 'HS256'
JWT_HEADER = 'Authorization'
JWT_SUBJECT_KEY = 'sub'

REDIS_URL = "redis://:@localhost:6379/0"

CUR_ID = 'cur_identity'
CUR_USER = 'cur_user'

HOST = '0.0.0.0'
ESHOST = None
PORT = 5000

EP_LOCATION = "http://39.106.143.18:7080"
EP_SMS_PATH = "/login/sendVerifyCode"
EP_LIVE_PATH = '/live'

