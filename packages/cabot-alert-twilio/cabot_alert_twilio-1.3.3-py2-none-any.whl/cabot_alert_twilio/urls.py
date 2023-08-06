from django.conf.urls import include, url
from .views import twiml_callback

urlpatterns = [
    url(r'^result/(?P<service_id>\d+)/twiml_callback/', twiml_callback, name="twiml-callback"),
]
