from django.urls import path
from .views import (ProduitListView, 
                    ProduitDetailtView, 
                    ProduitCreateView,
                    ProduitUpdateView,
                    ProduitDeleteView,
                    UserProduitListView,
                    Search)
from . import views

urlpatterns = [
    path('', ProduitListView.as_view(), name='site-home'),
    path('search/', Search.as_view(), name='search'),
    path('user/<str:username>/', UserProduitListView.as_view(), name='user-produits'),
    path('actualite/', views.actu, name='site-actualite'),
    path('register/', views.register, name='register'),
    path('publication/', views.public, name='site-publication'),
    path('produit/new/',ProduitCreateView.as_view(), name='produit-create'),
    path('produit/<int:pk>/',ProduitDetailtView.as_view(), name='produit-detail'),
    path('produit/<int:pk>/update/',ProduitUpdateView.as_view(), name='produit-update'),
    path('produit/<int:pk>/delete/',ProduitDeleteView.as_view(), name='produit-delete'),
    #afficher detail dun produit
    path('charge/', views.charge, name='charge'), # new
]
