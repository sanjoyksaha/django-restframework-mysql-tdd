from django.urls import path

from modules.expenses.views.category_views import CategoryListCreateView, CategoryDetailView

urlpatterns = [
    path("categories", CategoryListCreateView.as_view(),name="category-list-create"),
    path('categories/<int:pk>', CategoryDetailView.as_view(),name="category-detail")
]