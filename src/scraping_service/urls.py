"""scraping_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from scraping.views import home_view, list_view, v_detail, VacancyDetail, VacancyList

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('list/', list_view, name='list'),
    path('list/', VacancyList.as_view(), name='list'),

    path('accounts/', include(('accounts.urls', 'accounts'))),
    # path('detail/<int:pk>/', v_detail, name='detail'),
    path('detail/<int:pk>/', VacancyDetail.as_view(), name='detail'),

    path('', home_view, name='home'),
]
