import os
import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FROM_EMAIL = 'hello@holdsum.com'


SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True#os.getenv('DEBUG', '0') == '1'
HEROKU = os.getenv('HEROKU', '0') == '1'
AUTH_USER_MODEL = 'accounts.User'

PLAID_CLIENT_ID = os.environ['PLAID_CLIENT_ID']
PLAID_SECRET = os.environ['PLAID_SECRET']
PLAID_ENDPOINT = os.environ['PLAID_ENDPOINT']
PLAID_PUBLIC_KEY = '05e2e2ea696e8a6cd19a8433d34109'

DOCUSIGN_ENDPOINT = os.environ['DOCUSIGN_ENDPOINT']
DOCUSIGN_USERNAME = os.environ['DOCUSIGN_USERNAME']
DOCUSIGN_PASSWORD = os.environ['DOCUSIGN_PASSWORD']
DOCUSIGN_TEMPLATE_ID = os.environ['DOCUSIGN_TEMPLATE_ID']
DOCUSIGN_INTEGRATOR_KEY = os.environ['DOCUSIGN_INTEGRATOR_KEY']

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'private'
ACCOUNT_EMAIL_VERIFICATION = 'none'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 3rd party
    'nested_admin',
    'model_utils',
    'solo',
    # Auth
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    # Apps
    'accounts',
    'transactions',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'holdsum.urls'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
if HEROKU:
    EMAIL_BACKEND = 'sgbackend.SendGridBackend'
    SENDGRID_USER = os.environ['SENDGRID_USERNAME']
    SENDGRID_PASSWORD = os.environ['SENDGRID_PASSWORD']

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'holdsum.wsgi.application'


# Databases

DATABASES = {}
DATABASES['default'] = dj_database_url.config()

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'accounts.serializers.LoginResponseSerializer',
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.UserSerializer',
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}
# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = 1

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split('|')

# Static files (CSS, JavaScript, Images)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# Simplified static file serving.
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


try:
    MOMMY_CUSTOM_FIELDS_GEN = {
        'fernet_fields.fields.EncryptedDateField': 'model_mommy.generators.gen_date',
        'localflavor.us.models.USZipCodeField': lambda: '90210',
        'accounts.fields.EncryptedSSNField': lambda: '123-45-6789',
    }
except ImportError:
    pass

# rest auth settings for registrations.
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'accounts.serializers.RegistrationSerializer',
}