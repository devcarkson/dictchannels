from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Student, TeamMember, ContactSubmission, NewsletterSubscription,
    QuoteSubmission, ServiceInquiry, Enrollment, Assignment,
    AssignmentSubmission, Certificate, Announcement, Message, Payment
)

@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = ['student_id', 'username', 'email', 'first_name', 'last_name', 'course', 'is_active']
    list_filter = ['is_active', 'course', 'enrollment_date']
    search_fields = ['student_id', 'username', 'email', 'first_name', 'last_name']
    ordering = ['-enrollment_date']

    fieldsets = UserAdmin.fieldsets + (
        ('Student Information', {
            'fields': ('student_id', 'phone', 'course', 'enrollment_date')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Student Information', {
            'fields': ('student_id', 'phone', 'course', 'enrollment_date')
        }),
    )

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'display_order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'designation', 'bio']
    list_editable = ['display_order', 'is_active']
    ordering = ['display_order', 'name']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'designation', 'bio')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at']

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['fname', 'email', 'subject', 'submitted_at', 'is_read']
    list_filter = ['submitted_at', 'is_read']
    search_fields = ['fname', 'email', 'subject', 'message']
    readonly_fields = ['submitted_at']
    list_editable = ['is_read']
    ordering = ['-submitted_at']

    fieldsets = (
        ('Contact Information', {
            'fields': ('fname', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'submitted_at')
        }),
    )

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at', 'progress_percentage', 'is_completed']
    list_filter = ['is_completed', 'enrolled_at', 'course']
    search_fields = ['student__student_id', 'student__username', 'course__title']
    list_editable = ['progress_percentage', 'is_completed']
    ordering = ['-enrolled_at']

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'due_date', 'max_score', 'created_at']
    list_filter = ['due_date', 'created_at', 'course']
    search_fields = ['title', 'description', 'course__title']
    ordering = ['due_date']

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'submitted_at', 'score', 'status']
    list_filter = ['status', 'submitted_at', 'assignment__course']
    search_fields = ['assignment__title', 'student__student_id', 'student__username']
    list_editable = ['score', 'status']
    ordering = ['-submitted_at']

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'issued_at', 'certificate_number']
    list_filter = ['issued_at', 'course']
    search_fields = ['student__student_id', 'student__username', 'course__title', 'certificate_number']
    ordering = ['-issued_at']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'created_by', 'created_at', 'is_important']
    list_filter = ['is_important', 'created_at', 'course']
    search_fields = ['title', 'content', 'created_by__username']
    list_editable = ['is_important']
    ordering = ['-created_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'subject', 'sent_at', 'is_read']
    list_filter = ['is_read', 'sent_at']
    search_fields = ['sender__username', 'recipient__username', 'subject', 'content']
    list_editable = ['is_read']
    ordering = ['-sent_at']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount', 'description', 'payment_date', 'status']
    list_filter = ['status', 'payment_date']
    search_fields = ['student__student_id', 'student__username', 'description', 'transaction_id']
    list_editable = ['status']
    ordering = ['-payment_date']

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['subscribed_at', 'is_active']
    search_fields = ['email']
    readonly_fields = ['subscribed_at']
    list_editable = ['is_active']
    ordering = ['-subscribed_at']

@admin.register(QuoteSubmission)
class QuoteSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'service', 'submitted_at', 'is_read']
    list_filter = ['submitted_at', 'is_read', 'service']
    search_fields = ['name', 'email', 'service', 'message']
    readonly_fields = ['submitted_at']
    list_editable = ['is_read']
    ordering = ['-submitted_at']

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Quote Details', {
            'fields': ('service', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'submitted_at')
        }),
    )

@admin.register(ServiceInquiry)
class ServiceInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'service', 'submitted_at', 'is_read']
    list_filter = ['submitted_at', 'is_read', 'service']
    search_fields = ['name', 'email', 'service', 'message']
    readonly_fields = ['submitted_at']
    list_editable = ['is_read']
    ordering = ['-submitted_at']

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('service', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'submitted_at')
        }),
    )