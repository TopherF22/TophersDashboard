from django.contrib import admin
from django.urls import path
from LandingPage.views import landing, graph

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", landing, name='home'),
    path("graph/", graph, name='graph'),
]