from django.urls import path
from . import views

urlpatterns = [
    path('', views.items_list, name='items_list'),       # List & Create
    path('<int:pk>/', views.item_detail, name='item_detail'),  # Retrieve, Update, Delete
    path('import_csv/', views.import_csv, name='import_csv'),
]
