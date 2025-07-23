from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('operational_staff', 'Operational Staff'),
        ('project_manager', 'Project Manager'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='projects_created')

    def __str__(self):
        return self.name

class Cashflow(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='cashflows')
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='cashflows_created')

    def __str__(self):
        return f"{self.project.name} - {self.amount} on {self.date}"

class Progress(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='progresses')
    date = models.DateField()
    description = models.TextField()
    photo = models.ImageField(upload_to='progress_photos/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='progresses_created')

    def __str__(self):
        return f"{self.project.name} progress on {self.date}"

class RAB(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='rabs')
    item = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='rabs_created')

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project.name} - {self.item}"

class Schedule(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='schedules')
    task = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='schedules_assigned')

    def __str__(self):
        return f"{self.project.name} - {self.task}"
