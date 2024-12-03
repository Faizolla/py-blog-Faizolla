from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login, authenticate, logout
from .forms import RegistrationForm, UserLoginForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .token import TokenGenerator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
from .models import User


account_activation_token = TokenGenerator()

def delete_inactive_users():
    check_time = timezone.now() - timezone.timedelta(minutes=15)
    inactive_users = User.objects.filter(is_active=False, date_joined__lt=check_time)
    
    for user in inactive_users:
        user.delete()

def registration(request):
    if request.method != 'POST':
        delete_inactive_users()
        form = RegistrationForm()    
    else:
        delete_inactive_users()
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
        
            try:
                existing_user = User.objects.get(email=email)
                if not existing_user.is_active():
                    existing_user.delete()
                else:
                    return render(request, '#', {'error':'Данный пользователь зарегестрирован и активен'})
            except: 
                pass
            
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Ссылка для активации аккаунта на сайте' + str(current_site)
            messege = render_to_string('auth/acc_active_email.html',{
                'user' : user,
                'domain' : current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : account_activation_token.make_token(user),

            })
            to_email = email
            email = EmailMessage(mail_subject, messege, to = [to_email])
            email.send()
            return render(request, 'auth/register_email_messege.html', {'email': to_email})
    return render(request, 'auth/registration.html', {'form': form})

def activation(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        time_elapsed = timezone.now() - user.date_joined
        if time_elapsed.total_seconds() < 900:
            user.is_active = True
            user.save()
            return render(request, 'auth/success_activate.html')
        else:
            delete_inactive_users()
            return render(request, 'auth/fail_activate.html')

def user_login(request):
    if request.method != 'POST':
        form = UserLoginForm()
    else:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email = form.cleaned_data['email'], password = form.cleaned_data['password'])
            print(user)
            if user is not None:
                auth_login(request, user)
                return redirect('all_post')
    return render(request, 'auth/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('all_post')

# Create your views here.

