from .common import *

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

## 로컬DB
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "HOST": "localhost",
#         "NAME": "gurmdari",
#         "USER": "postgres",
#         "PASSWORD": "qawsedrf",
#         "PORT": 5432,
#     },
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "133.186.146.159",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "qawsedrf",
        "PORT": 5432,
    }
}
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
