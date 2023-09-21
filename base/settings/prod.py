from .common import *

# ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

DEBUG = os.environ.get("DEBUG") in ["1", "t", "true", "T", "True"]

# CORS_ORIGIN_WHITELIST = os.environ.get("CORS_ORIGIN_WHITELIST", "").split(",")
# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOW_CREDENTIALS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[DJANGO] %(levelname)s %(asctime)s %(module)s '
                      '%(name)s.%(funcName)s:%(lineno)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {                       # handlers : 로그 레코드로 무슨 작업을 할 것인지 정의
#         'logstash': {
#             'level': 'INFO',
#             'class': 'logstash.TCPLogstashHandler',
#             'host': os.environ.get('HOST_IP'),
#             'port': 5959,  # Default value: 5959
#             'version': 1,
#         },
#     },
#     'loggers': {                        # loggers : 처리해야 할 로그 레코드를 어떤 handler로 전달할지 정의
#         'django': {
#             'handlers': ['logstash'],   # 로그 레코드를 logstash handler로 전달
#         },
#     },
# }