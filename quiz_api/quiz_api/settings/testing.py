import sys

from .base import *
from dotenv import load_dotenv

load_dotenv()

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('ENGINE'),
        'NAME': os.environ.get('TEST_NAME'),
        'USER': 'postgres',
        'PASSWORD': os.environ.get('PASSWORD'),
        'HOST': os.environ.get('HOST'),
        'PORT': os.environ.get('PORT'),
    }
}


# python manage.py runserver --settings=quiz_api.settings.development
