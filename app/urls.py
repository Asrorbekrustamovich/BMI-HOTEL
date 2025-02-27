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
    MessageListCreateView, MessageRetrieveUpdateDestroyView,
    WorkerSendMessageToManagerView, MessageList_beetween_manager_and_workers_View_For_manager,
    MessageList_beetween_manager_and_workers_View_For_Worker, ManagerAdmin_and_manager_MessageListView_for_admin,
    ManagerAdmin_and_manager_MessageListView_for_Manager, ManagerSendMessageToWorkersView,
    ManagerSendMessageToAdminView, AdminSendMessageToManagerView,
    DepartmentListCreateView, DepartmentRetrieveUpdateDestroyView
)

urlpatterns = [
    # Authentication
    path('login/', LoginView.as_view(), name='login-page'),

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

    # Worker sends message to manager
    path('workers-send-message-to-manager/<int:user_id>/', WorkerSendMessageToManagerView.as_view(), name='worker-send-message-to-manager'),

    # Manager sends message to workers
    path('manager-send-message-to-workers/<int:user_id>/', ManagerSendMessageToWorkersView.as_view(), name='manager-send-message-to-workers'),

    # Manager sends message to admin
    path('manager-send-message-to-admin/<int:user_id>/', ManagerSendMessageToAdminView.as_view(), name='manager-send-message-to-admin'),

    # Admin sends message to manager
    path('admin-send-message-to-manager/<int:receiver_id>/', AdminSendMessageToManagerView.as_view(), name='admin-send-message-to-manager'),

    # Messages between manager and workers (for manager)
    path('messages-between-manager-and-workers/manager/<int:sender_id>/<int:receiver_id>/', MessageList_beetween_manager_and_workers_View_For_manager.as_view(), name='messages-between-manager-and-workers-manager'),

    # Messages between manager and workers (for worker)
    path('messages-between-manager-and-workers/worker/<int:sender_id>/<int:receiver_id>/', MessageList_beetween_manager_and_workers_View_For_Worker.as_view(), name='messages-between-manager-and-workers-worker'),

    # Messages between admin and manager (for admin)
    path('messages-between-admin-and-manager/admin/<int:sender_id>/<int:receiver_id>/', ManagerAdmin_and_manager_MessageListView_for_admin.as_view(), name='messages-between-admin-and-manager-admin'),

    # Messages between admin and manager (for manager)
    path('messages-between-admin-and-manager/manager/<int:sender_id>/<int:receiver_id>/', ManagerAdmin_and_manager_MessageListView_for_Manager.as_view(), name='messages-between-admin-and-manager-manager'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)