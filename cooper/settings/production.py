from .base import *
import dj_database_url


#Override defualt setings here

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}


PAYSTACK_PUBLIC_KEY	= config('PAYSTACK_PUBLIC_LIVE_KEY')

PAYSTACK_SECRET_KEY  = config('PAYSTACK_SECRET_LIVE_KEY')
