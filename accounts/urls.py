from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.views import home, products, customer, create_order, \
    update_order, delete_order, loginPage, registerPage, logoutUser, user_page, \
    account_settings

urlpatterns = [
    path('home/', home, name="home"),
    path('products/', products, name="products"),
    path('customer/<str:pk_test>', customer, name="customer"),
    path('create_order/<str:pk>', create_order, name="create_order"),
    path('update_order/<str:pk>', update_order, name="update_order"),
    path('delete_order/<str:pk>', delete_order, name="delete_order"),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerPage, name='register'),
    path("user/", user_page, name="user"),
    path('account/', account_settings, name="account"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),
]
