from sunrinseed.settings import *

SWAGGER_SETTINGS['base_path'] = 'dev.ner0.kr/docs'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
