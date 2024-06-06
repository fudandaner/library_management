"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from web1 import views

urlpatterns = [
    path('library/login/', views.login),
    path('library/manage_login/', views.manage_login),
    path('library/register/', views.register),
    path('library/<int:id>/list/', views.library_list),
    path('manage_library/list/', views.manage_library_list),
    path('library/book_add/', views.book_add),
    path('library/<int:nid>/book_edit/', views.book_edit),
    path('library/book_delete/', views.book_delete),
    path('library/manage_book_search/', views.manage_book_search),
    path('library/<int:id>/student_book_search/', views.student_book_search),
    path('library/<int:nid>/<int:id>/student_rent/', views.student_rent),
    path('library/<int:id>/student_rent_record/', views.student_rent_record),
    path('library/manage_rent_record/', views.manage_rent_record),
    path('library/manage_student_record/', views.manage_student_record),
    path('library/<int:Borrowid>/<int:id>/student_return/', views.student_return),

]
