"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from .views import CustomLoginView
from .views import CustomSignupView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),  # includes the urls of 'pages' app
    path('leads/', include('leads.urls')),  # includes the urls of 'leads' app
    path("studio/", include("studio.urls")),
    path("todo/", include("todo_app.urls")),
    path("logger/", include("logger.urls")),
    path('blog/', include("blog.urls"), name='blog'),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    path("accounts/", include("allauth.urls")),
    path('core/', include("core.urls")),
    path('files_core/', include("files_core.urls")),
    path('api-auth/', include("rest_framework.urls")),
    path('summernote/', include("django_summernote.urls")),
    path('chatbot/', include("chatbot.urls")),
    path('panels/', include('panels.urls')),
    path("chat_asgi/", include("chat_asgi.urls")),
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
