from django.urls import path ,re_path
from .views import remove_student,profile_page, enter_room, chat_room,register, login_view, home, create_course, enroll_in_course,course_detail,course_list, UserListCreateAPI, UserDetailAPI, CourseListCreateAPI, CourseDetailAPI
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('create-course/', create_course, name='create_course'),
    path('enroll/<int:course_id>/', enroll_in_course, name='enroll_in_course'),
    path('courses/', course_list, name='course_list'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('enter/', enter_room, name='enter_room'),
    re_path(r'chat/(?P<room_name>\w+)/$',chat_room, name='chat_room'),
    path('profile/<int:user_id>/', profile_page, name='profile_page'),
    path('remove_student/<int:student_id>/<int:course_id>/', remove_student, name='remove_student'),

    

    # User API endpoints
    path('api/users/', UserListCreateAPI.as_view(), name='user-list-create-api'),
    path('api/users/<int:pk>/', UserDetailAPI.as_view(), name='user-detail-api'),

    # Course API endpoints
    path('api/courses/', CourseListCreateAPI.as_view(), name='course-list-create-api'),
    path('api/courses/<int:pk>/', CourseDetailAPI.as_view(), name='course-detail-api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)