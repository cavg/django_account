from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib import messages
from django.contrib.auth.models import User


ROLE_CHOICES = (
    ('Titular', 'Titular'),
    ('Usuario', 'Usuario')
)

def build_account(first_name, last_name, email, phone, company_name, password, identifier =None, address = None, line_of_business = None):
    if not Company.objects.filter(name=company_name).exists():
            company = Company()
            company.name = company_name
            company.phone = phone
            if identifier is not None:
                company.identifier = identifier
            if address is not None:
                company.address = address
            if line_of_business is not None:
                company.line_of_business = line_of_business
            if not User.objects.filter(email=email).exists():
                company.save()
                user = User.objects.create_user(email, email=email, password=password, first_name=first_name, last_name=last_name)
                if user:
                    account = Account.objects.get(user=user)
                    account.company = company
                    account.save()
                    return True, messages.SUCCESS, 'Se ha registrado exitosamente en Leantech, bienvenido!'
                else:
                    return False, messages.WARNING, 'No se pudo registrar el usuario.'
            else:
                return False, messages.WARNING, 'Su correo ya está asociado a una empresa. No se pudo completar el registro.'
    else:
        return False, messages.WARNING, 'Su empresa ya ha sido registrada previamente, por favor ingrese en la zona de clientes.'
    return False, None, None

class Company(models.Model):
    name = models.CharField(max_length=25)
    identifier = models.CharField(max_length=25, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    line_of_business = models.CharField(max_length=255, blank=True, null=True, default=None)

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