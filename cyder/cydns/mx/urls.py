from django.conf.urls.defaults import *
from django.views.decorators.csrf import csrf_exempt

from cyder.cydns.mx.views import *
from cyder.cydns.views import cydns_list_create_record


urlpatterns = patterns('',
   url(r'^$', cydns_list_create_record, name='mx-list',
       kwargs={'record_type': 'mx'}),

   url(r'(?P<domain>[\w-]+)/create/$',
       csrf_exempt(MXCreateView.as_view()), name='mx-create-in-domain'),

   url(r'(?P<pk>[\w-]+)/update/$',
       cydns_list_create_record, name='mx-update'),
   url(r'(?P<pk>[\w-]+)/delete/$',
       csrf_exempt(MXDeleteView.as_view()), name='mx-delete'),
   url(r'(?P<pk>[\w-]+)/$',
       csrf_exempt(MXDetailView.as_view()), name='mx-detail'),
)
