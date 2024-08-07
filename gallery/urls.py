from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('author/', views.author, name='author'),
    path('book/', views.book, name='book'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_book/', views.add_book, name='add_book'),
    path('update/<int:pk>', views.update, name='update'),
    path('books_of_author/<int:pk>', views.books_of_author, name='books_of_author'),
    path('delete_book/<int:pk>', views.delete_book, name='delete_book'),
    path('done_book/<int:pk>', views.done_book, name='done_book'),
    path('update_author/<int:pk>', views.update_author, name='update_author'),
    path('delete_author/<int:pk>', views.delete_author, name='delete_author')
]