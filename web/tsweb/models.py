from django.db import models
from django.core.validators import RegexValidator

class Student(models.Model):
    GRADE_CHOICES = [
         ('A', 'First grade'),
        ('B', 'Second grade'),
        ('C', 'Third grade'),
        ('D', 'Fourth grade'),
        ('E', 'Fifth grade'),
        ('F', 'Sixth grade'),
    ]

    id_number = models.CharField(max_length=9, unique=True, validators=[RegexValidator(r'^\d{9}$', "Please enter exactly 9 digits.")])
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(
        max_length=10, 
        validators=[
            RegexValidator(
                regex=r'^(05\d|0[23489])\d{7}$',
                message="Invalid Israeli phone number. Please enter 10 digits starting with 05."
            )
        ]
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"