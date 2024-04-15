from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index, name="index"),	 
    path('register', views.register, name= "register"),  
    path('log_in', views.log_in, name= "log_in"),
    path('success', views.success, name="success"),
    path('log_out', views.log_out, name= "log_out")
    

]
