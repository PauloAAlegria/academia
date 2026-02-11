import os
import logging.handlers
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')  # carrega as variáveis do .env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', '94.46.171.215,localhost').split(',')]

# Application definition

INSTALLED_APPS = [
    'amdf.apps.AmdfConfig', # app com os signals
    'event',
    'festival',
    'polo.apps.PoloConfig',
    'team.apps.TeamConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce', # editor de texto    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # o middleware de cache (ajustar o caminho conforme o app) não deixar cache em memória do login de admin
    'amdf.middleware.admin_no_cache.AdminNoCacheMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Corrigido para usar Pathlib
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'amdf.context_processors.footer_context',
                'amdf.context_processors.dev_link',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# login e logout personalizado
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-pt' #alterou-se a linguagem

TIME_ZONE = 'Europe/Lisbon' #alterou-se a time_zone

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Configurações de arquivos estáticos
STATIC_URL = '/static/'

#novos static adicionados

# Diretório para arquivos estáticos coletados (produção)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Diretórios adicionais para arquivos estáticos (desenvolvimento)
STATICFILES_DIRS = [
    BASE_DIR / 'templates' / 'static',  # Corrigido para Pathlib
]

# Configurações de arquivos de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Usando Pathlib

#configurações do editor de texto
TINYMCE_DEFAULT_CONFIG = {
    'height': 300,
    'width': '100%',
    'menubar': True,

    'plugins': (
        'advlist autolink lists link image charmap print preview anchor '
        'searchreplace visualblocks code fullscreen '
        'insertdatetime media table paste help wordcount'
    ),

    'toolbar': (
        'undo redo | formatselect | bold italic underline strikethrough | '
        'forecolor backcolor | alignleft aligncenter alignright alignjustify | '
        'bullist numlist outdent indent | link image media | '
        'removeformat | code fullscreen | help'
    ),

    # Carregar os arquivos de estilo CSS
    # garantir que o conteúdo que o utilizador edita no editor WYSIWYG (What You See Is What You Get),
    # fique visualmente parecido (ou idêntico) ao conteúdo que será exibido no site final após ser salvo.
    'content_css': [
        '/assets/css/about.css',
        '/assets/css/course.css',
        '/assets/css/event.css',
        '/assets/css/festival.css',
        '/assets/css/polo_penamacor.css',
        '/assets/css/styles.css',
        '/assets/css/team.css',
    ],

    # Evitar estilos inline e spans que quebrem o layout
    'valid_styles': {},  # impede inline style
    'style_formats': [],
    'formats': {
        'bold': {'inline': 'strong'},
        'italic': {'inline': 'em'},
        'underline': {'inline': 'u'},
        'strikethrough': {'inline': 'strike'},
    },

    # Forçar conteúdo limpo
    'forced_root_block': 'p',
    'force_br_newlines': False,
    'force_p_newlines': True,
    'cleanup': True,
    'cleanup_on_startup': True,

    # Bloquear elementos que bagunçem o HTML
    'invalid_elements': 'div,section,article,span,font,style,script',
    'extended_valid_elements': '',

    # Limitar o tipo de blocos que o utilizador pode usar
    'block_formats': 'Parágrafo=p; Cabeçalho 1=h1; Cabeçalho 2=h2; Cabeçalho 3=h3',
}

# sessões criadas para que alguém que esteja logado inativamente mais de 10 minutos, o site encerre a sessão automaticamente
# e também encerra se fecharem o browser
SESSION_COOKIE_AGE = 300  # 5 minutos (em segundos)
SESSION_SAVE_EVERY_REQUEST = True  # Reinicia o contador a cada requisição
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Isto criará um arquivo chamado logs/erros_criticos.log (podemos alterar o caminho)
# e armazenará lá os logs com nível ERROR — como o logger.error(...). até um máximo de 5 MB
# e cria até 2 pastas, e vai apagando a mais antiga.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs/erros_criticos.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 2,  # mantém até 2 arquivos antigos
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} {message}',
            'style': '{',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        '__main__': {
            'handlers': ['file'],
            'level': 'ERROR',
        },
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
