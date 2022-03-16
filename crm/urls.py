"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings # to add images pattern url
from django.conf.urls.static import static

from crm.settings import MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("accounts.urls")), # adding all app urls

]
# getting images to print in browser url
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
