from django.urls import path
from cash_management.views import *

urlpatterns = [
    path('',register_page,name='register_page'),
    path('login/',login_page,name='login_page'),
    path('logout/',logout_page,name='logout_page'),
    path('dashboard/',dashboard_page,name='dashboard_page'),
    path('profile/',profile_page,name='profile_page'),
    path('add-cash/',addcash_page,name='addcash_page'),
    path('add-expense/',addexpense_page,name='addexpense_page'),
    path('update-cash/<int:id>/',update_cash_page,name='update_cash_page'),
    path('delete-cash/<int:id>/',delete_cash_page,name='delete_cash_page'),
    path('update-expense/<int:id>/',update_expense_page,name='update_expense_page'),
    path('delete-expense/<int:id>/',delete_expense_page,name='delete_expense_page'),
    path('cash/', cash_page, name='cash_page'),
    path('expense/', expense_page, name='expense_page'),
    
]