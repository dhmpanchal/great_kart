from django.urls import path

from accounts.views import ChangePAsswordView, ForgotPAsswordView, LoginVire, MyOrderView, OrderDetailView, ProfileView, ResetPasswordConfirmView, SignUpView, UpdatePasswordView, logout_view, AccountActivationView, DashboardView

urlpatterns = [
    path('register/', SignUpView.as_view(), name="register_view"),
    path('login/', LoginVire.as_view(), name="login_view"),
    path('logout/', logout_view, name="logout_view"),
    path('activate/<uidb64>/<token>', AccountActivationView.as_view(), name='activate'),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('', DashboardView.as_view(), name="dashboard"),
    path('my_orders/', MyOrderView.as_view(), name='my_orders'),
    path('edit_profile/', ProfileView.as_view(), name='edit_profile'),
    path('change_password/', UpdatePasswordView.as_view(), name='change_password'),
    path('order_detail/<order_id>/', OrderDetailView.as_view(), name='order_detail'),

    #forget password
    path('forgotpassword', ForgotPAsswordView.as_view(), name="forgotpassword"),
    path('reset_password_confirm/<uidb64>/<token>', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
    path('password_change', ChangePAsswordView.as_view(), name="password_change"),
]