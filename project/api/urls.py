from django.urls import path

from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('database/', views.DatabaseView.as_view(), name='database'),
     path('database/scan/<int:id>/', views.DatabaseScanView.as_view(),
          name='scan'),
     path('information_type/', views.InformationTypeView.as_view(),
          name='information_type'),
     path('information_type/<int:id>/', views.InformationTypeView.as_view()),
     path('record/', views.RecordView.as_view(), name='record')
]
