from django.conf.urls import url
from django.contrib import admin

from .views import HomeView
from .views import SpotligthView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^spotligth/$', SpotligthView.as_view(), name='spotligth'),
]
