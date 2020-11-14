from django.contrib import admin
from django.urls import path
from account.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Account
    path('', index_view, name="index"),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('me/', profile_view, name="profile"),
    path('edit-profile/', edit_profile_view, name="edit_profile"),
    path('me/password', profile_pass_view, name="profile_pass"),
    path('me/notification', profile_not_view, name="profile_not"),
    path('me/billings', profile_bills_view, name="profile_bills"),
    path('edit-pass/', edit_pass_view, name="edit_pass"),
    path('me/dashboard/', profile_dashboard, name="dashboard"),
    path('changePlan/foundation/', changeplan_foundation, name="foundation"),
    path('changePlan/intermediate/', changeplan_intermediate, name="intermediate"),
    path('changePlan/enterprise/', changeplan_enterprise, name="enterprise"),



    path('courses/', courses_view, name="course_view"),
    # path('new-course/', new_course, name="new_course"),
    path('courses/overview/<str:id>/', courses_overview, name="course_over_view"),
    path('courses/start/<str:id>/', courses_start, name="course_start_view"),
    path('updateProgress/<str:id>/', update_progress, name="update_progress"),
    path('show_pdf/<str:path>/', show_pdf, name="show_pdf"),


    path('contact/', contact, name="contact"),

    path('subcribe/', subcsribe, name="subscribe"),

    path("password_reset/", auth_views.PasswordResetView.as_view(),
         name="reset_password"),
    path("password_reset_sent/", auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("password_reset_complete/",
         auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),


    # Admin Panel
    path('admin-login/', admin_login, name="admin_login"),
    path('admin-dashboard/', admin_board, name="admin_board"),
    path('admin-course/', admin_course, name="admin_course"),
    path('admin-course/add/', admin_course_add, name="admin_course_add"),
    path('admin-course/update/<str:id>/',
         admin_course_update, name="admin_course_update"),
    path('admin-message/', admin_message, name="admin_message"),
    path('admin-settings/', admin_settings, name="admin-settings"),
    path('admin-edit-pass/', admin_edit_pass_view, name="admin_edit_pass"),
    path('admin-edit-profile/', admin_edit_profile_view, name="admin_edit_profile"),
    path('admin-logout/', admin_logout, name="admin_logout"),
    path('admin-subsribers/', admin_subsribers, name="admin_subsribers"),
    path('admin-subsribers-search/', admin_subsribers_search, name="admin_subsribers_search"),
    path('admin-subsribers-cancel/<str:id>/', admin_subsribers_cancel, name="admin_subsribers_cancel"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
