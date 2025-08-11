from django.urls import path
from .views import ReadingListView,ReadingListBookManagement,ListBookView


urlpatterns = [
    path('reading-list/', ReadingListView.as_view(), name='reading-list'),
    path('reading-list/<int:pk>/', ReadingListView.as_view(), name='reading-list'),
    path('list-book/<int:pk>/', ListBookView.as_view(), name='list-book'),
    path('list-book-management/', ReadingListBookManagement.as_view(), name ='list-book-management'),
    


]
