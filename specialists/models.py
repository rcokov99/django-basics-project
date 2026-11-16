from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


class Department(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        error_messages={'unique': 'This department already exists!'}
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0, message="Price cannot be negative.")]
    )
    duration_minutes = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3, message="Doctor's name must be at least 3 characters long.")]
    )
    specialty = models.CharField(max_length=100)
    bio = models.TextField()
    years_of_experience = models.PositiveIntegerField(default=0)

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='doctors'
    )

    services = models.ManyToManyField(
        Service,
        related_name='doctors',
        blank=True
    )

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f"Dr. {self.full_name} ({self.specialty})"

    @property
    def average_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0.0
