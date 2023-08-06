from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^alipay/', include('alipay.urls')),

    url(r'^admin/', admin.site.urls),

    url(r'^', include('sample.urls')),
]
