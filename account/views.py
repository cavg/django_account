from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import Account, ROLE_CHOICES
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings

def _update_account(request, template, params_template, redirect_link, self_update):
    if request.method == 'GET':
        return render(request, template, params_template)
    elif request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if (password1 != password2):
            messages.add_message(request, messages.SUCCESS, 'Las contraseñas ingresadas no coinciden, los datos no fueron actualizados.')
            return render(request, template, params_template)
        else:
            if self_update:
                user = request.user
            else:
                user = User()
            update_password = False
            if  password1 is not '' and password2 is not '':
                user.set_password(password1)
                if self_update:
                    messages.add_message(request, messages.SUCCESS, 'Los datos fueron actualizados, inicie sesión nuevamente.')
                else:
                    messages.add_message(request, messages.SUCCESS, 'Usuario ingresado exitosamente, se le ha enviado un correo de notificación.')
                update_password = True
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = email
            user.save()

            if 'role' in request.POST:
                ac = Account.objects.get(user=user)
                ac.role = request.POST['role']
                ac.company = Account.objects.get(user=request.user).company
                ac.save()
                send_mail(
                    "Su cuenta en {} ha sido creada".format(settings.DKIM_DOMAIN),
                    "Estimado/a {},\nLe han creado una cuenta para administrar la flota de vehículos, para acceder ingrese a:\n\nhttp://gps.{}/.\n\n Atte. Equipo {}".format(first_name, settings.DKIM_DOMAIN, settings.DKIM_DOMAIN),
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

            if self_update:
                if not update_password:
                    messages.add_message(request, messages.SUCCESS, 'Los datos fueron actualizados.')
                else:
                    logout(request)
            return redirect(redirect_link)

@login_required
def me(request):
    return _update_account(request, 'me.htm', {'user':request.user}, '/login', True)

@login_required
def users(request):
    account = Account.objects.get(user__pk = request.user.pk)
    accounts = Account.objects.filter(company__pk = account.company.pk).exclude(user__pk=account.pk)
    return render(request, 'users.htm', {'user':request.user, 'accounts': accounts})

@login_required
def new(request):
    return _update_account(request, 'account-new.htm', {'roles': ROLE_CHOICES}, '/account/users', False)


@login_required
def list(request):
    accounts = [obj.as_dict() for obj in Account.objects.all()]
    return JsonResponse(accounts, safe=False)

