from django.db import models
from django.core.validators import RegexValidator,EmailValidator
from django.contrib.auth.hashers import make_password

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

    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Teacher(models.Model):
    SUBJECT_CHOICES = [
        ('Math', 'Math'),
        ('English', 'English'),
        ('Science', 'Science'),
        # ניתן להוסיף כאן מקצועות נוספים לפי הצורך
    ]
    CLASS_CHOICES = [
        ('A', 'First grade'),
        ('B', 'Second grade'),
        ('C', 'Third grade'),
        ('D', 'Fourth grade'),
        ('E', 'Fifth grade'),
        ('F', 'Sixth grade'),
    ]
    id_number = models.CharField(
        max_length=9, 
        unique=True, 
        validators=[RegexValidator(r'^\d{9}$', "Please enter exactly 9 digits.")]
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True, validators=[EmailValidator(message="Invalid email address.")])
    phone_number = models.CharField(
        max_length=10, 
        validators=[
            RegexValidator(
                regex=r'^(05\d|0[23489])\d{7}$',
                message='Invalid Israeli phone number. Please enter 10 digits starting with 05 .'
            )
        ]
        
    )
    password = models.CharField(max_length=128)  # הוספת שדה סיסמה
    subjects = models.CharField(
        max_length=50,
        choices=SUBJECT_CHOICES,
        help_text="Select the subject the teacher can teach"
    )
    classes = models.CharField(
        max_length=1,
        choices=CLASS_CHOICES,
        help_text="Select the grade the teacher can educate"
    )
    def save(self, *args, **kwargs):
        # הצפנת הסיסמה לפני שמירה
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"




class Admin(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        # הצפנת הסיסמה לפני שמירה
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

        return self.username


class Message(models.Model):
    sender = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='sent_messages')
    recipients = models.ManyToManyField(Teacher, related_name='received_messages')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.subject
    
    
 
    
    
 
    
    
