from sunrinseed.settings.base import *  # NOQA
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
SWAGGER_SETTINGS['base_path'] = 'dev.ner0.kr/docs'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sunrinseed',
        'USER': 'nero',
        'PASSWORD': 'nerodatabase',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
