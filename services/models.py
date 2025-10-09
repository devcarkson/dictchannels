from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fab fa-android')  # FontAwesome icon class
    page = models.CharField(max_length=100, blank=True, null=True)  # URL name for the service link

    def __str__(self):
        return self.title