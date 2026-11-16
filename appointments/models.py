from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from specialists.models import Doctor, Service  # Make sure Service is imported


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='appointments')
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField(default='')
    appointment_date_time = models.DateTimeField()

    class Meta:
        ordering = ['appointment_date_time']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date_time'],
                name='unique_doctor_slot'
            ),
        ]

    def __str__(self):
        return f"{self.doctor} - {self.service.name} at {self.appointment_date_time.strftime('%Y-%m-%d %H:%M')}"


class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate from 1 to 5 stars"
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reviewer_name} - {self.rating} Stars for {self.doctor}"
