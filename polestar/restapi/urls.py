from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^import/$', views.UploadFile.as_view()),
    url(r'^ships/$', views.ShipsView.as_view()),
    url(r'^positions/(?P<imo>\d+)/$', views.PositionsView.as_view()),
    
]