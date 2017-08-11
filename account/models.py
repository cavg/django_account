from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

ROLE_CHOICES = (
    ('Titular', 'Titular'),
    ('Usuario', 'Usuario')
)

class Company(models.Model):
    name = models.CharField(max_length=25)
    identifier = models.CharField(max_length=25, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CHOICES[0][0])

    def __str__(self):
        return "Username:{} - Email:{}".format(self.user.username, self.user.email)

    def company_name(self):
        if self.company_id:
            return self.company.name
        else:
            return None

    def user_username(self):
        return self.user.username

    def user_email(self):
        return self.user.email

    def as_dict(self):
        return {
            "name": "{} {}".format(self.user.first_name, self.user.last_name),
            "email": self.user_email(),
            "company": self.company_name(),
            "role": self.role
        }



@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    instance.account.save()