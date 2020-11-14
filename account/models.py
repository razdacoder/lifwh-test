from django.db import models
from django.contrib.postgres.fields import ArrayField
# from django.contrib.postgres.fields.jsonb import JSONField as JSONBField
from django.db.models import JSONField

import uuid
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, number, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not number:
            raise ValueError('Users must have a number')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            number=number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            number=number,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


plans = (
    ("foundation", "Foundation"),
    ("intermediate", "Intermediate"),
    ("enterprise", "Enterprise")
)


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    number = models.CharField(max_length=15)
    my_course = JSONField(default=list, null=True, blank=True)
    plan = models.CharField(
        choices=plans, max_length=300, null=True, blank=True)
    # photo = models.FileField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'number']

    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_initial(self):
        return self.first_name[0]

    # For checking permissions. to keep it simple all admin have ALL permissons

    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=2000)
    image = models.FileField(upload_to="images")
    pdf = models.FileField(upload_to="files", null=True, blank=True)
    plan = models.CharField(max_length=300, default="foundation")
    students = JSONField(default=list, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # def get_video_name(self):
    #     for video in self.videos:
    #         return video.name

    def save(self, *args, **kwargs):
        # Opening the uploaded image
        im = Image.open(self.image)

        output = BytesIO()

        # Resize/modify the image
        im = im.resize((1200, 900))

        # after modifications, save it to the output
        im.save(output, format='JPEG', quality=100)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        self.image = InMemoryUploadedFile(output, 'FileField', "%s.jpg" % self.image.name.split(
            '.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super().save(*args, **kwargs)


class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    video = models.FileField(upload_to="videos")

    def __str__(self):
        return self.course.title

    def get_name(self):
        ned = self.video.name.split("/")[1]

        name = ned.split(".")[0]
        return name


class Subscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60)
    email = models.EmailField()
    message = models.TextField(max_length=2500)

    def __str__(self):
        return self.name
