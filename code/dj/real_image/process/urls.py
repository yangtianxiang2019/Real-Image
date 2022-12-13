from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve
from . import views




urlpatterns = [
    path('process_image', views.process_image, name='process_image'),
    re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.BASE_IMAGE_DIR + '/output',
    })
]
