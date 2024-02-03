DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'siberian_engine',
        'USER': 'postgres',
        'PASSWORD': 'Maestro',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
