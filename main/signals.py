# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Enrollment, Notification

# @receiver(post_save, sender=Enrollment)
# def notify_teacher_on_enrollment(sender, instance, created, **kwargs):
#     if created:
#         course = instance.course
#         teacher = course.teacher
#         student = instance.student

#         # Create an in-app notification for the teacher
#         Notification.objects.create(
#             user=teacher,
#             message=f'A new student, {student.username}, has enrolled in your course "{course.title}".'
#         )
