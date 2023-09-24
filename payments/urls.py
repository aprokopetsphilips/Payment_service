from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('config/', views.stripe_config),
    path('create-checkout-session/<pk>/', views.create_checkout_session, name='create-checkout-session'),
    path('show_item/<pk>/', views.show_selected_item),
    path('success/', views.SuccessView.as_view()),
    path('cancelled/', views.CancelledView.as_view()),
]