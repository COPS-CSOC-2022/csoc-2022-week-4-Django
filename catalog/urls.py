import imp
from django.urls import path
from . import views
from django.urls import include, re_path
urlpatterns = [
    path("", views.index, name="index" ),
    path("books/", views.BookListView.as_view(), name="books"),
    # path("books/", views.BookList, name="books"),
    path("books/<int:pk>", views.BookDetailView.as_view(), name="book-detail"),
    path("authors/", views.AuthorListView.as_view(), name="authors"),
    path("authors/<int:pk>", views.AuthorDetailView.as_view(), name="author-detail"),
    path('accounts/',include('django.contrib.auth.urls')),
    path('books/<int:pk>/renew/',views.renew_book,name='renew-book'),
    path("books/loaned", views.loaned_books, name="loaned-books"),
    path("register", views.register_request, name="register")
    # path("books/loaned", views.BookCopyListView.as_view(), name="loaned-books"),

    # path('books/<int:pk>/return/',views.return_book,name='return-book'),
]
