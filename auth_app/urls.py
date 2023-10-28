from django.urls import path
from . import views

#urlConfiguration
urlpatterns = [
    path('', views.home),
    path('signup', views.signup),
    path('login', views.login_f),
    path('logout', views.logout_f),
    # from main urls file, if it send urls here called signup/ then run signup(method) from views(file containing the method)
]