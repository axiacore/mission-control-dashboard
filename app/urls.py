from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from .views import SpotligthView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(r'^spotligth/$', SpotligthView.as_view(), name='spotligth'),
]
