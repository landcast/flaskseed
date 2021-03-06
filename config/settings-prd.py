ENV_NAME = 'production'

TESTING = False

SECRET_KEY = '123'

DEBUG = False

DEBUG_LOGPATH = '/var/log/flaskseed-debug-prd'
LOG_REQ_RES = True

PID_FILE = 'flaskseed'

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'ustutor'
PASSWORD = 'Us_Tutor'
DBHOST = 'rm-2ze6kzf5ig80613f7vo.mysql.rds.aliyuncs.com'
DBPORT = '3306'
DATABASE = 'ustutor'
SQLALCHEMY_DATABASE_URI = f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@" \
                          f"{DBHOST}:{DBPORT}/{DATABASE}?charset=utf8"

SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ECHO = True

DEBUG_TB_INTERCEPT_REDIRECTS=False

# followed upload config items
UPLOAD_FOLDER = '/var/upload'
ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg', 'gif','ppt','PDF', 'PNG', 'JPG', 'JPEG', 'GIF','pptx','PPTX']
# upload file size limitation
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

MAIL_SERVER = 'smtp.139.com'
MAIL_PORT = 25
MAIL_USE_SSL = True
MAIL_USERNAME = '13521273258@139.com'
MAIL_PASSWORD = 'lt780404'
MAIL_DEFAULT_SENDER = '13521273258@139.com'

JWT_SECRET = 'src-flask-dev-no-random'
JWT_ALG = 'HS256'
JWT_HEADER = 'Authorization'
JWT_SUBJECT_KEY = 'sub'

#REDIS_URL = "redis://:Us_Tutor@r-2ze6f26b30516ca4.redis.rds.aliyuncs.com:6379/0"

REDIS_URL = "redis://:@localhost:6379/0"

CUR_ID = 'cur_identity'
CUR_USER = 'cur_user'

HOST = '0.0.0.0'
ESHOST = None
PORT = 5000

EP_LOCATION = "http://localhost:7080"
EP_SMS_PATH = "/login/sendVerifyCode"
EP_LIVE_PATH = '/live'
EP_CLASSIN_PATH = '/classIn'

