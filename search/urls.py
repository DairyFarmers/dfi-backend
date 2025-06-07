# orders URL Configuration

from django.urls import path
from search.views.search_view import SearchView

urlpatterns = [
    path('', SearchView.as_view(), name='search')
]
