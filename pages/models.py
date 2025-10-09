from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage

class Student(AbstractUser):
    student_id = models.CharField(max_length=20, unique=True, blank=True, verbose_name="Student ID")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone Number")
    course = models.CharField(max_length=100, blank=True, verbose_name="Current Course")
    enrollment_date = models.DateField(default=timezone.now, verbose_name="Enrollment Date")

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def save(self, *args, **kwargs):
        if not self.student_id:
            # Auto-generate student ID: DCT + year + sequential number
            year = timezone.now().year
            last_student = Student.objects.filter(student_id__startswith=f'DCT{year}').order_by('-student_id').first()
            if last_student:
                last_num = int(last_student.student_id[7:])  # DCT2024001 -> 001
                new_num = last_num + 1
            else:
                new_num = 1
            self.student_id = f'DCT{year}{new_num:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_id} - {self.get_full_name()}"

class TeamMember(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    designation = models.CharField(max_length=100, verbose_name="Job Title/Designation")
    bio = models.TextField(verbose_name="Biography/Description", blank=True)
    image = models.ImageField(upload_to='team/', blank=True, null=True, verbose_name="Profile Image")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.name} - {self.designation}"

class ContactSubmission(models.Model):
    fname = models.CharField(max_length=100, verbose_name="First Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    subject = models.CharField(max_length=200, verbose_name="Subject")
    message = models.TextField(verbose_name="Message")
    submitted_at = models.DateTimeField(default=timezone.now, verbose_name="Submitted At")
    is_read = models.BooleanField(default=False, verbose_name="Is Read")

    class Meta:
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.fname} - {self.subject}"

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email Address")
    subscribed_at = models.DateTimeField(default=timezone.now, verbose_name="Subscribed At")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email

class QuoteSubmission(models.Model):
    SERVICE_CHOICES = [
        ('SOFTWARE DEVELOPMENT SERVICE', 'SOFTWARE DEVELOPMENT SERVICE'),
        ('PROFESSIONAL COMPUTER AND IT EDUCATION', 'PROFESSIONAL COMPUTER AND IT EDUCATION'),
        ('DIGITAL ADVERTISING AND BUSINESS BRANDING', 'DIGITAL ADVERTISING AND BUSINESS BRANDING'),
        ('INTERNATIONAL UNIVERSITY ADMISSION PROCESSING', 'INTERNATIONAL UNIVERSITY ADMISSION PROCESSING'),
        ('Others', 'Others'),
    ]

    name = models.CharField(max_length=100, verbose_name="Full Name")
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    email = models.EmailField(verbose_name="Email Address")
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES, verbose_name="Service Type")
    message = models.TextField(verbose_name="Project Details/Message")
    submitted_at = models.DateTimeField(default=timezone.now, verbose_name="Submitted At")
    is_read = models.BooleanField(default=False, verbose_name="Is Read")

    class Meta:
        verbose_name = "Quote Submission"
        verbose_name_plural = "Quote Submissions"
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} - {self.service}"

# Student Dashboard Models
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(default=timezone.now)
    progress_percentage = models.IntegerField(default=0)  # 0-100
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.course.title}"

class Assignment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='assignments')
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    max_score = models.IntegerField(default=100)

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"
        ordering = ['due_date']

    def __str__(self):
        return f"{self.title} - {self.course.title}"

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='assignments/', blank=True, null=True)
    content = models.TextField(blank=True)
    score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Assignment.STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name = "Assignment Submission"
        verbose_name_plural = "Assignment Submissions"
        unique_together = ['assignment', 'student']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.assignment.title}"

class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='certificates')
    issued_at = models.DateTimeField(default=timezone.now)
    certificate_number = models.CharField(max_length=50, unique=True)
    file = models.FileField(upload_to='certificates/', blank=True, null=True)

    class Meta:
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.course.title}"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='announcements', null=True, blank=True)
    created_by = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='announcements')
    created_at = models.DateTimeField(default=timezone.now)
    is_important = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Message(models.Model):
    sender = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.sender.get_full_name()} -> {self.recipient.get_full_name()}: {self.subject}"

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    payment_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.amount} - {self.status}"

class ServiceInquiry(models.Model):
    SERVICE_CHOICES = [
        ('SOFTWARE DEVELOPMENT SERVICE', 'SOFTWARE DEVELOPMENT SERVICE'),
        ('PROFESSIONAL COMPUTER AND IT EDUCATION', 'PROFESSIONAL COMPUTER AND IT EDUCATION'),
        ('DIGITAL ADVERTISING AND BUSINESS BRANDING', 'DIGITAL ADVERTISING AND BUSINESS BRANDING'),
        ('INTERNATIONAL UNIVERSITY ADMISSION PROCESSING', 'INTERNATIONAL UNIVERSITY ADMISSION PROCESSING'),
        ('WEBSITE SEO Optimization', 'WEBSITE SEO Optimization'),
        ('Others', 'Others'),
    ]

    name = models.CharField(max_length=100, verbose_name="Full Name")
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    email = models.EmailField(verbose_name="Email Address")
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES, verbose_name="Service Type")
    message = models.TextField(verbose_name="Message")
    submitted_at = models.DateTimeField(default=timezone.now, verbose_name="Submitted At")
    is_read = models.BooleanField(default=False, verbose_name="Is Read")

    class Meta:
        verbose_name = "Service Inquiry"
        verbose_name_plural = "Service Inquiries"
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} - {self.service}"