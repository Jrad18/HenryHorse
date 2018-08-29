from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Forms/add', views.add, name='Add Form'),
    path('Forms/', views.index, name='Form'),
    path('Forms/newForm/<int:form_id>', views.newForm, name='New Form'),

]