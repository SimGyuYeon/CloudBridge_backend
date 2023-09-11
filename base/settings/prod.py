from .common import *

# ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

DEBUG = os.environ.get("DEBUG") in ["1", "t", "true", "T", "True"]

CORS_ORIGIN_WHITELIST = os.environ.get("CORS_ORIGIN_WHITELIST", "").split(",")

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