#filename is settings_local.py
import sys
import os
coverage = False
#coverage = True
if coverage:
    NOSE_ARGS = [ '-s', '-v', '-d', '--cover-package=mozdns,core',
            "--with-coverage", "--pdb" ]
else:
    NOSE_ARGS = [ '-s', '-v', '-d']
_base = os.path.dirname(__file__)
site_root = os.path.realpath(os.path.join(_base, '../'))
sys.path.append(site_root)
sys.path.append(site_root + '/adapters')
sys.path.append(site_root + '/libs')
sys.path.append(site_root + '/modules')
sys.path.append(site_root + '/vendor')

STATIC_DOC_ROOT=os.path.join(_base, site_root + '/static')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('rtucker', 'rtucker@mozilla.com'),
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chili',
        'USER': 'root',
        'PASSWORD': 'yoursql',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {
            'init_command': 'SET storage_engine=InnoDB',
            'charset' : 'utf8',
            'use_unicode' : True,
        },
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
    },
    # 'slave': {
    #     ...
    # },
}

#SLAVE_DATABASES = ['default',]
#TEST_DATABASE = ['test_inventory_mozilla']
#DATABASE_ROUTERS = ('multidb.PinningMasterSlaveRouter',)
#DATABASE_ROUTERS = ('multidb.MasterSlaveRouter',)
# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

REMOTE_LOGINS_ON = True


SYSADMINS = ()

BUILD_TEAM = ()


WIKI_USER = 'inv_bot'
WIKI_PASSWORD = 'inv'

USE_LDAP = True
if USE_LDAP:
    LDAP_HOST = 'localhost'
    LDAP_USER = 'uid=binduser,ou=logins,dc=mozilla'
    LDAP_PASS = ''
BUG_URL = 'https://bugzilla.mozilla.org/show_bug.cgi?id='
#import mysite.monitor
#mysite.monitor.start(interval=1.0)
# Specify your custom test runner to use
#TEST_RUNNER='test_runner_with_coverage'

 # List of modules to enable for code coverage
#COVERAGE_MODULES = ['api.views']
#TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'
USER_SYSTEM_ALLOWED_DELETE = ('')
TEMPLATE_DIRS = (
    site_root + '/templates',
)
MEDIA_URL = '/static/'
DEV = True

def jinja_url(view_name, *args, **kwargs):
    from django.core.urlresolvers import reverse, NoReverseMatch
    try:
        return reverse(view_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        try:
            project_name = settings.SETTINGS_MODULE.split('.')[0]
            return reverse(project_name + '.' + view_name,
                           args=args, kwargs=kwargs)
        except NoReverseMatch:
            return ''

#from jinja2 import nodes
#from jinja2.ext import Extension
from jinja2 import FileSystemLoader, Environment
JINJA_EXTS=('jinja2.ext.i18n','libs.jinja_extensions.csrf_token',)
env = Environment( loader=FileSystemLoader(TEMPLATE_DIRS))
env.filters['url'] = jinja_url
env.globals['MEDIA_URL'] = MEDIA_URL

import logging
error = dict(level=logging.ERROR)
info = dict(level=logging.INFO)
debug = dict(level=logging.DEBUG)

LOGGING = {
    'loggers': {
        'product_details': error,
        'nose.plugins.manager': error,
        'django.db.backends': error,
        'elasticsearch': info,
        'inventory': debug,
    },
}
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
API_ACCESS = ('GET','POST','PUT','DELETE')
SCRIPT_URL = 'https://inventory.mozilla.org'
DESKTOP_EMAIL_ADDRESS = 'desktop@mozilla.com'
FROM_EMAIL_ADDRESS = 'inventory@mozilla.com'
UNAUTHORIZED_EMAIL_ADDRESS = ['rtucker@mozilla.com']
DHCP_CONFIG_OUTPUT_DIRECTORY = '/tmp'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

#JINJA_CONFIG = {'autoescape': False}

BUILD_PATH = '/builds'
