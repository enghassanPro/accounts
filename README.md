in setting file add some variables 
in installing app:
add "account.apps.AccountConfig" , "social_django"
add some lines at the end:
AUTHENTICATION_BACKENDS = [

    'social_core.backends.google.GoogleOAuth2',  # for Google authentication
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',

]
SOCIAL_AUTH_URL_NAMESPACE = "auth:social"
LOGIN_REDIRECT_URL = '/auth/'
EMAIL_USE_TLS = True
EMAIL_USE_SSL= False
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'email'
EMAIL_HOST_PASSWORD = 'password'
DEFAULT_FROM_EMAIL = 'email'
EMAIL_PORT = 587

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
