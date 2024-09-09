from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm , CourseForm , StatusUpdateForm , FeedbackForm , CoursePDFUploadForm
from .models import Course, Enrollment, User , StatusUpdate, Feedback
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics
from .serializers import UserSerializer, CourseSerializer




User = get_user_model()  # Get the User model


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to the user's home page
    else:
        form = UserRegistrationForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to the user's home page
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

from django.contrib.auth.decorators import login_required

# @login_required
# def home(request):
#     user = request.user
#     context = {}
    
#     if user.user_type == 'student':  # Change to check user_type
#         context = {
#             'courses': user.enrollments.all(),  # Correct the usage of related_name
#             'status_updates': user.status_updates.all(),  # Assuming you have a StatusUpdate model
#         }
#     elif user.user_type == 'teacher':  # Change to check user_type
#         context = {
#             'courses': user.courses.all(),  # Fetch courses related to the teacher
#             'students': User.objects.filter(enrollments__course__teacher=user),  # Get students for the courses
#         }
    
#     return render(request, 'main/home.html', context)

# @login_required
# def home(request):
#     user = request.user
#     context = {}
    
#     if user.user_type == 'student':  # Assuming you're using user_type to differentiate
#         # Handle status update form submission
#         if request.method == 'POST':
#             form = StatusUpdateForm(request.POST)
#             if form.is_valid():
#                 status_update = form.save(commit=False)
#                 status_update.user = request.user  # Assign the logged-in user as the author
#                 status_update.save()
#                 return redirect('home')  # Reload the page to show the new status
#         else:
#             form = StatusUpdateForm()

#         # Pass the form and status updates to the template
#         context = {
#             'courses': user.enrollments.all(),
#             'status_updates': user.status_updates.all(),
#             'status_form': form,
#         }

#     elif user.user_type == 'teacher':
#         context = {
#             'courses': user.courses.all(),
#             'students': User.objects.filter(enrollments__course__teacher=user),  # Get students for the courses
#         }
    
#     return render(request, 'main/home.html', context)
# @login_required
# def home(request):
#     user = request.user
#     context = {}

#     if user.user_type == 'student':
#         if request.method == 'POST':
#             form = StatusUpdateForm(request.POST)
#             if form.is_valid():
#                 status_update = form.save(commit=False)
#                 status_update.user = request.user
#                 status_update.save()
#                 return redirect('home')
#         else:
#             form = StatusUpdateForm()

#         context = {
#             'courses': user.enrollments.all(),
#             'status_updates': user.status_updates.all(),
#             'status_form': form,
#         }

#     elif user.user_type == 'teacher':
#         # Search functionality
#         search_query = request.GET.get('search', '')
#         search_results = []
#         if search_query:
#             search_results = User.objects.filter(
#                 (Q(real_name__icontains=search_query) | Q(email__icontains=search_query)) &
#                 (Q(user_type='teacher') | Q(user_type='student'))
#             )

#         context = {
#             'courses': user.courses.all(),
#             'students': User.objects.filter(enrollments__course__teacher=user),
#             'search_query': search_query,
#             'search_results': search_results,
#         }

#     return render(request, 'main/home.html', context)


@login_required
def home(request):
    user = request.user
    context = {}

    if user.user_type == 'student':
        if request.method == 'POST':
            form = StatusUpdateForm(request.POST)
            if form.is_valid():
                status_update = form.save(commit=False)
                status_update.user = request.user
                status_update.save()
                return redirect('home')
        else:
            form = StatusUpdateForm()

        context = {
            'courses': user.enrollments.all(),
            'status_updates': user.status_updates.all(),
            'status_form': form,
        }

    elif user.user_type == 'teacher':
        # Search functionality
        search_query = request.GET.get('search', '')
        search_results = []
        if search_query:
            search_results = User.objects.filter(
                (Q(real_name__icontains=search_query) | Q(email__icontains=search_query)) &
                (Q(user_type='teacher') | Q(user_type='student'))
            )

            # Check if the request is AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                results_data = [
                    {
                        'real_name': user.real_name,
                        'user_type': user.user_type,
                        'email': user.email,
                    } for user in search_results
                ]
                return JsonResponse({'results': results_data})

        # Get all courses and students enrolled in those courses
        courses = user.courses.all()
        students = User.objects.filter(user_type='student')

        # Create a list of dictionaries to store enrollment status
        enrollment_status = []
        for course in courses:
            for student in students:
                enrolled = student.enrollments.filter(course=course).exists()
                enrollment_status.append({
                    'course_id': course.id,
                    'student_id': student.id,
                    'enrolled': enrolled,
                    'student_name': student.real_name,
                })

        context = {
            'courses': courses,
            'students': students,
            'search_query': search_query,
            'search_results': search_results,
            'enrollment_status': enrollment_status,  # Pass the enrollment status to the context
        }

    return render(request, 'main/home.html', context)



@login_required
def remove_student(request, student_id, course_id):
    # Get the student and course
    student = get_object_or_404(User, id=student_id)
    course = get_object_or_404(Course, id=course_id)

    # Remove the student from the course
    enrollment = Enrollment.objects.filter(course=course, student=student).first()
    if enrollment:
        enrollment.delete()
        messages.success(request, f'Student {student.real_name} has been removed from {course.title}.')
    else:
        messages.error(request, 'Enrollment not found.')

    return redirect('home')



# # View to create a new course
# @login_required
# def create_course(request):
#     if request.method == 'POST':
#         form = CourseForm(request.POST)
#         if form.is_valid():
#             course = form.save(commit=False)
#             course.teacher = request.user  # Assign the logged-in user as the teacher
#             course.save()
#             return redirect('course_list')  # Redirect to a course list view
#     else:
#         form = CourseForm()
#     return render(request, 'main/create_course.html', {'form': form})
@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)  # Add request.FILES to handle file uploads
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user  # Assign the logged-in user as the teacher
            course.save()
            return redirect('course_list')  # Redirect to course list after creating the course
    else:
        form = CourseForm()
    return render(request, 'main/create_course.html', {'form': form})

@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)

    if created:
        # Enrollment was successful
        messages.success(request, 'You have successfully enrolled in the course.')
    else:
        # User was already enrolled
        messages.info(request, 'You are already enrolled in this course.')

    return redirect('course_detail', course_id=course.id)  # Redirect to course detail



# View to list all courses
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'main/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    feedbacks = Feedback.objects.filter(course=course)

    # Handle feedback form for students
    if request.user.user_type == 'student' and request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.student = request.user  # Assign the logged-in user as the student
            feedback.course = course
            feedback.save()
            return redirect('course_detail', course_id=course_id)
    else:
        feedback_form = FeedbackForm()

    # Handle PDF upload for teachers
    if request.user.user_type == 'teacher' and request.method == 'POST':
        pdf_form = CoursePDFUploadForm(request.POST, request.FILES, instance=course)
        if pdf_form.is_valid():
            pdf_form.save()
            return redirect('course_detail', course_id=course_id)
    else:
        pdf_form = CoursePDFUploadForm(instance=course) if request.user.user_type == 'teacher' else None

    context = {
        'course': course,
        'feedbacks': feedbacks,
        'feedback_form': feedback_form,
        'pdf_form': pdf_form  # Only passed for teachers
    }
    return render(request, 'main/course_detail.html', context)
#not needed after having a new profile page for everyone 
# @login_required 
# def student_profile(request, student_id):
#     student = get_object_or_404(User, id=student_id, user_type='student')
#     context = {
#         'student': student,
#     }
#     return render(request, 'main/student_profile.html', context)

def enter_room(request):
    return render(request, 'main/enter_room.html')

# def chat_room(request, room_name):
#     return render(request, 'main/chat_room.html', {
#         'room_name': room_name,
#         'username': request.user.username,  # Pass the logged-in user's username to the template
#     })

@login_required
def chat_room(request, room_name):
    return render(request, 'main/chat_room.html', {
        'room_name': room_name,
        'username': request.user.real_name,  # Pass the username to the template
    })

@login_required
def profile_page(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    
    context = {
        'profile_user': profile_user,
        'courses': profile_user.enrollments.all() if profile_user.user_type == 'student' else profile_user.courses.all(),
        'status_updates': profile_user.status_updates.all() if profile_user.user_type == 'student' else None,
    }
    
    return render(request, 'main/profile_page.html', context)


# List all users
class UserListAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# List all courses
class CourseListAPI(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# User List (GET), Create (POST)
class UserListCreateAPI(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Retrieve (GET), Update (PUT/PATCH), Delete (DELETE) a single user
class UserDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Course List (GET), Create (POST)
class CourseListCreateAPI(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# Retrieve (GET), Update (PUT/PATCH), Delete (DELETE) a single course
class CourseDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


