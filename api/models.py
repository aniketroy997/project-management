from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, default="", blank= True)
    completed = models.BooleanField(default=False, blank= True)
    date_of_creation = models.DateField(auto_now_add=True, null=True, blank= True)
    date_of_start = models.DateField(auto_now_add=False, null=True, blank= True)
    date_of_end = models.DateField(auto_now_add=False, null=True, blank= True)
    responsible = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    border_color = models.CharField(max_length=8, default="#ffffff")

    def __str__(self):
        return str(self.title)

class State(models.Model):
    title = models.CharField(max_length=255, null=True, blank= True)
    description = models.CharField(max_length=255, null=True, default="", blank= True)    

class Phase(models.Model):
    title= models.CharField(max_length=255, null=True, blank= True)
    description = models.CharField(max_length=255, default="", blank= True)
    completed = models.BooleanField(default=False, blank= True)
    date_of_creation = models.DateField(auto_now_add=True, blank= True)
    date_of_start = models.DateField(auto_now_add=False, null=True, blank= True)
    date_of_end = models.DateField(auto_now_add=False, null=True, blank= True)
    responsible = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    project_Id = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

class Milestone(models.Model):
    title= models.CharField(max_length=255, null=True, blank= True)
    description = models.CharField(max_length=255, default="", blank= True)
    completed = models.BooleanField(default=False, blank= True)
    date_of_creation = models.DateField(auto_now_add=True, blank= True)
    date_of_start = models.DateField(auto_now_add=False, null=True, blank= True)
    date_of_end = models.DateField(auto_now_add=False, null=True, blank= True)
    responsible = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    project_Id = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    phase_Id = models.ForeignKey(Phase, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

class Department(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null = True, blank =True)

    def __str__(self):
        return str(self.title)

class WorkPackage(models.Model):
    PRIORITY = (
        ('LOW', 1), ('MEDIUM', 2), ('HIGH', 3)
    )
    title= models.CharField(max_length=255, null=True, blank= True)
    description = models.CharField(max_length=255, default="", blank= True)
    completed = models.BooleanField(default=False, blank= True)
    date_of_creation = models.DateField(auto_now_add=True, blank= True)
    date_of_start = models.DateField(auto_now_add=False, null=True, blank= True)
    date_of_end = models.DateField(auto_now_add=False, null=True, blank= True)
    duration = models.IntegerField(null=True, blank= True)
    responsible = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    project_Id = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    milestone_Id = models.ForeignKey(Milestone, null=True, on_delete=models.CASCADE)
    phase_Id = models.ForeignKey(Phase, null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, on_delete=models.CASCADE)
    state = models.CharField(max_length=255, default="", blank= True)

    priority = models.IntegerField(default= 1, choices=PRIORITY)
    efforts_actual = models.IntegerField(null=True)
    efforts_planned = models.IntegerField(null=True)

    border_color = models.CharField(max_length=8, default="#ffffff")

    def __str__(self):
        return str(self.title)

class SubWorkPackage(models.Model):
    PRIORITY = (
        ('LOW', 1), ('MEDIUM', 2), ('HIGH', 3)
    )
    title= models.CharField(max_length=255, null=True, blank= True)
    description = models.CharField(max_length=255, default="", blank= True)
    
    completed = models.BooleanField(default=False, blank= True)

    date_of_creation = models.DateField(auto_now_add=True, blank= True)

    date_of_state1 = models.DateField(auto_now_add=True, null=True, blank= True)
    date_of_state2 = models.DateField(auto_now_add=False, null=True, blank= True)
    date_of_state3 = models.DateField(auto_now_add=False, null=True, blank= True)
    date_of_state4 = models.DateField(auto_now_add=False, null=True, blank= True)

    date_of_start = models.DateField(auto_now_add=False, null=True, blank= True)

    date_of_end = models.DateField(auto_now_add=False, null=True, blank= True)

    duration = models.IntegerField(null=True, blank= True)

    actual_date_of_start = models.DateField(auto_now_add=False, null=True, blank= True)
    actual_date_of_end = models.DateField(auto_now_add=False, null=True, blank= True)

    efforts_actual = models.IntegerField(null=True)
    efforts_planned = models.IntegerField(null=True)

    responsible = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    project_Id = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    milestone_Id = models.ForeignKey(Milestone, null=True, on_delete=models.CASCADE)
    phase_Id = models.ForeignKey(Phase, null=True, on_delete=models.CASCADE)
    workPackage =  models.ForeignKey(WorkPackage, null=True, on_delete=models.CASCADE)
    priority = models.IntegerField(default= 1, choices=PRIORITY)
    state = models.ForeignKey(State, null=True, on_delete=models.CASCADE, default = 1)

    border_color = models.CharField(max_length=8, default="#ffffff")

    def __str__(self):
        return str(self.title)

class ManagerGroup(models.Model):
    project_Id = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

class UserGroup(models.Model):
    project_Id = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

class UserProfileDetail(models.Model):
    
    user = models.OneToOneField(User, null = True, blank = True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null = True)
    phone = models.CharField(max_length=200, null = True)
    email = models.CharField(max_length=200, null = True)
    profile_pic = models.ImageField(default="default_profile.png", null = True, blank = True)
    department = models.ForeignKey(Department, null=True, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=False, null=True)

    def __str__(self):
        return str(self.user)

def create_profile(sender, instance, created, **kwargs):
    if created:
        new_user = UserProfileDetail.objects.create(user = instance, name = instance.first_name +" "+ instance.last_name)
               
        print("Profile Created!", instance.first_name)

post_save.connect(create_profile, sender = User)
