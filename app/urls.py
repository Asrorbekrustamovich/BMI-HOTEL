from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import (
    RoleListCreateView, RoleRetrieveUpdateDestroyView,
    UserInfoListCreateView, UserInfoRetrieveUpdateDestroyView,
    UserRoleListCreateView, UserRoleRetrieveUpdateDestroyView,
    RoomListCreateView, RoomRetrieveUpdateDestroyView,
    CustomerListCreateView, CustomerRetrieveUpdateDestroyView,
    BookingListCreateView, BookingRetrieveUpdateDestroyView,
    LoginView, StatusListCreateView, StatusRetrieveUpdateDestroyView,
    UserListCreateView, UserRetrieveUpdateDestroyView,
    MessageListCreateView, MessageRetrieveUpdateDestroyView, MessageExchangeView,
    DepartmentListCreateView, DepartmentRetrieveUpdateDestroyView,RoomTypeDeleteUpdateView,RoomTypeListCreateView
)

urlpatterns = [
    # Authentication
    path('login/', LoginView.as_view(), name='login-page'),
    path('room-types/', RoomTypeListCreateView.as_view(), name='roomtype-list'),
    path('room-types/<int:pk>/', RoomTypeDeleteUpdateView.as_view(), name='roomtype-detail'),
    # User URLs
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),

    # Role URLs
    path('roles/', RoleListCreateView.as_view(), name='role-list-create'),
    path('roles/<int:pk>/', RoleRetrieveUpdateDestroyView.as_view(), name='role-retrieve-update-destroy'),

    # UserInfo URLs
    path('user-infos/', UserInfoListCreateView.as_view(), name='user-info-list-create'),
    path('user-infos/<int:user_id>/', UserInfoRetrieveUpdateDestroyView.as_view(), name='user-info-retrieve-update-destroy'),

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

    # Status URLs
    path('status/', StatusListCreateView.as_view(), name='status-list-create'),
    path('status/<int:pk>/', StatusRetrieveUpdateDestroyView.as_view(), name='status-retrieve-update-destroy'),

    # Department URLs
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentRetrieveUpdateDestroyView.as_view(), name='department-retrieve-update-destroy'),

    # Message URLs
    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageRetrieveUpdateDestroyView.as_view(), name='message-retrieve-update-destroy'),
    path('messages/<int:sender_id>/<int:receiver_id>/', MessageExchangeView.as_view(), name='message-exchange'),
   
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)