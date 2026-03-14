from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('signup/', views.signupt, name='signup'),
    path('',views.index, name='index'),
    path('login/', views.logint, name='login'),
    path('logout/', views.logoutt, name='logout'),
    path('form/',views.formupload, name='form'),
    path('forms/' ,views.formstu, name='forms'),
    path('dashboard/',views.dashboardf, name='dashboard'),
    path('delete/<int:id>/', views.delete_material, name='delete_material'),
    path('view_text/<int:id>/',views.view_text, name='view_text'),
    path('edit/<int:id>/', views.formupload, name='edit_material'),
    path("materials/<str:type>/", views.materials, name="materials"),
    path("verify/<uidb64>/<token>/",views.verify_email, name='verify_email'),

]
