from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    image = models.ImageField(upload_to='testimonials/')
    text = models.TextField()

    def __str__(self):
        return self.name