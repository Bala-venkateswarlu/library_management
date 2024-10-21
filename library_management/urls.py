from django.urls import path, include
from library_management import views
from django.http import HttpResponse

urlpatterns = [
    path('', views.register, name='library'),
    path('register/', views.register, name='register'),  # Registration
    path('login/', views.login, name='login'),  # Login
   
    path('readers/', views.reader, name='readers'),
    path('home', views.home, name='home'),
    path('books', views.books, name='books'),
    path('books/add/', views.add_book_view, name='add_book'),  # View for adding a book
    path('bag', views.bag, name='bag'),
    path('returns', views.returns, name='returns'),
    path('pre_login',views.pre_login,name='pre_login'),
    path('pre_readers',views.pre_readers,name='pre_readers'),
    path('pre_returns',views.pre_returns,name='pre_returns'),
    path('pre_bag',views.pre_bag,name='pre_bag'),
   
]
