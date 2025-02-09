
from django.urls import path
from .views import (
    RoleListCreateView, RoleRetrieveUpdateDestroyView,
    UserInfoListCreateView, UserInfoRetrieveUpdateDestroyView,
    UserRoleListCreateView, UserRoleRetrieveUpdateDestroyView,
    RoomListCreateView, RoomRetrieveUpdateDestroyView,
    CustomerListCreateView, CustomerRetrieveUpdateDestroyView,
    BookingListCreateView, BookingRetrieveUpdateDestroyView,
    HistoryListView, HistoryRetrieveUpdateDestroyView,
    LoginView
)
from .views import UserListCreateView, UserRetrieveUpdateDestroyView
urlpatterns =[
    path('login/', LoginView.as_view()),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('roles/', RoleListCreateView.as_view(), name='role-list-create'),
    path('roles/<int:pk>/', RoleRetrieveUpdateDestroyView.as_view(), name='role-retrieve-update-destroy'),

    # UserInfo URLs
    path('user-infos/', UserInfoListCreateView.as_view(), name='user-info-list-create'),
    path('user-infos/<int:pk>/', UserInfoRetrieveUpdateDestroyView.as_view(), name='user-info-retrieve-update-destroy'),

    # UserRole URLs
    path('user-roles/', UserRoleListCreateView.as_view(), name='user-role-list-create'),
    path('user-roles/<int:pk>/', UserRoleRetrieveUpdateDestroyView.as_view(), name='user-role-retrieve-update-destroy'),

    # Room URLs
    path('rooms/', RoomListCreateView.as_view(), name='room-list-create'),
    path('rooms/<int:pk>/', RoomRetrieveUpdateDestroyView.as_view(), name='room-retrieve-update-destroy'),

    # Customer URLs
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerRetrieveUpdateDestroyView.as_view(), name='customer-retrieve-update-destroy'),

    # Booking URLs
    path('bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', BookingRetrieveUpdateDestroyView.as_view(), name='booking-retrieve-update-destroy'),

    # History URLs
    path('history/', HistoryListView.as_view(), name='history-list'),
    path('history/<int:pk>/', HistoryRetrieveUpdateDestroyView.as_view(), name='history-retrieve-update-destroy'),
]