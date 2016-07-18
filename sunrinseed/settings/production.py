from sunrinseed.settings.base import *  # NOQA
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
SWAGGER_SETTINGS['base_path'] = 'dev.sunrin.io/docs'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sunrinseed',
        'USER': 'secret',
        'PASSWORD': 'secret',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
