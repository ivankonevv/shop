from django.urls import path

from .api_views import (
    CategoryAPIView,
    SmartphoneListAPIView,
    NotebookListAPIView,
    SmartphoneDetailAPIView,
    NotebookDetailAPIView,
    CustomersListAPIView,
)

urlpatterns = [
    path('categories/<str:id>', CategoryAPIView.as_view(), name='categories'),
    path('customers/', CustomersListAPIView.as_view(), name='customers_list'),

    path('smartphones/', SmartphoneListAPIView.as_view(), name='smartphones_list'),
    path('smartphones/<str:id>', SmartphoneDetailAPIView.as_view(), name='smartphone_detail'),
    path('notebooks/', NotebookListAPIView.as_view(), name='notebooks_list'),
    path('notebooks/<str:id>', NotebookDetailAPIView.as_view(), name='notebooks_detail'),
]
