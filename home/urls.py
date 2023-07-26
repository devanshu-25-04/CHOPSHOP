from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from home import views
from home.forms import Loginform
urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('about2', views.about2, name='about2'),
    path('contact', views.contact, name='contact'),
    path('project', views.project, name='project'),   
    path('project2', views.project2, name='project2'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html',authentication_form=Loginform), name='login'),
    path('signup', views.signup.as_view(), name='signup'),
    path('home2', views.home2, name='home2'),
    path('shopmenu', views.shopmenu, name='shopmenu'),
    path('EmployerReg', views.EmployerReg, name='EmployerReg'),
    path('drappoint', views.drappoint, name='drappoint'),
    path('getPredictionsHairloss', views.getPredictionsHairloss,name='getPredictionsHairloss'),
    path('product', views.product, name='product'),
    path('confirmationpage', views.confirmationpage, name='confirmationpage'),
    path('appointmentcheck', views.appointmentcheck, name='appointmentcheck'),
]