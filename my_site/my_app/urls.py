from django.urls import path
from . import views
from django.urls import path

from . import views

urlpatterns = [
    path('hello', views.hello),
    path('books', views.get_all_books),
    path('books/only_books_with_authors', views.get_only_books_with_authors),
    path('stores', views.get_all_stores),
    path('stores/stores_expensive_books', views.get_stores_with_expensive_books),
    path('publishers', views.get_all_publishers),
    path('publishers/publishers_expensive_books', views.get_publishers_with_expensive_books),
    path('books/expensive_books', views.get_expensive_books),
    path('all_authors', views.get_all_authors),
    path('books/authors_expensive_books', views.get_authors_with_expensive_books),
    path('books/first_three_books', views.get_first_three_books),
    path('user/create', views.get_user_form),
    path('user/save', views.add_user),
    path('publisher/create', views.get_publisher_form),
    path('publisher/save', views.add_publisher),
    path('book/create', views.get_book_form),
    path('book/save', views.add_book),
    path('books/<book_id>', views.get_book_by_id),
    path('publisher/<publisher_id>', views.get_publisher_by_id),
    path('stores/<store_id>', views.get_store_by_id),
    path('authors/<author_id>', views.get_author_by_id)

]
