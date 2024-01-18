from email import message
import email
from django.core.mail import EmailMessage
from multiprocessing import context
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
import json
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm, HackerCreationForm, WaitingListCreationForm, CustomUserChangeForm, PhoneVerificationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from hacker.models import HackerInfo
from organizer.models import OrganizerInfo
from .helper import add_group, decide_redirect, decide_type
from .emailer import *
from .models import WaitingList, CustomUser
from .tokens import account_activate_token
from .decorators import user_not_authenticated
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from twilio.rest import Client
account_sid = 'AC9cef4f76fdda9c88bda8b03ef16cb4d1'
auth_token = 'b4440e9d1b2bb679fd0f35ebff37ca44'
client = Client(account_sid, auth_token)
import logging

# Add this at the top of your views.py file
logger = logging.getLogger(__name__)

@user_not_authenticated
def registration(request):
    if request.method == 'POST':
        create_user_form = CustomUserCreationForm(request.POST, request.FILES)
        create_hacker_form = HackerCreationForm(request.POST)
        print("valid11")
        if create_hacker_form.is_valid() and create_user_form.is_valid():
            print("valid")
            pword = create_user_form.cleaned_data['password1']

            # user = create_user_form.save()
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip = request.POST.get('zip')
            country = request.POST.get('country')
            user = create_user_form.save()
            # city = request.POST.get('city')
            # country = request.POST.get('country')

            phone = request.POST.get('phone')

            # user.save() we have to commit this now
            # ------------------------------------------------------
            user = create_user_form.save(commit=False)
            # user.is_active=False
            email = create_user_form.cleaned_data['email'].lower()
            user.email = email
            user.save()
            # Send activation email
            activateEmail(request, user, create_user_form.cleaned_data.get('email'))
            # Generate token
            token = default_token_generator.make_token(user)
            print(f"User Token is: {token}")

            # -----------------------------------------
            user.phone = phone
            code_to_generate_for_phone_verifi = generate_random_code()
            print("--------------------------------------------------")
            print(code_to_generate_for_phone_verifi)
            send_sms(code_to_generate_for_phone_verifi,phone)
            user.phone_verification_code = code_to_generate_for_phone_verifi
            user.save()
            # address = str(country) + ", " + str(city)

            # user.address = address

            hacker = create_hacker_form.save(commit=False)
            hacker.user = user
            hacker.save()
            add_group(user, 'hacker')

            print()
            user = authenticate(request, username=user.email, password=pword)
            if user is not None:
                login(request, user)
                return redirect('landing')
        else:
            for error in list(create_user_form.errors.values()):
                messages.error(request, error)
    else:
        create_user_form = CustomUserCreationForm()
        create_hacker_form = HackerCreationForm()

    context = {'create_hacker_form': create_hacker_form,
               'create_user_form': create_user_form}
    return render(request, 'defaults/register.html', context)

def send_sms(user_code, phone):
    message = client.messages.create(
        body=f"Hi! Your user and verification code is {user_code}",
        from_='+16363240647',
        to=f'{phone}'
    )

    print(message.sid)

def verify_phone(request):
    if request.method == 'POST':
        form = PhoneVerificationForm(request.POST)

        if form.is_valid():
            entered_code = form.cleaned_data['verification_code']
            print(entered_code)
            print(request.user)
            print(request.user.is_phone_verified)
            # Compare the entered code with the stored code
            if request.user.phone_verification_code == entered_code:
                # Update the phone_is_verified field
                request.user.is_phone_verified = True
                request.user.save()
                messages.success(request, "Phone number verified successfully.")
                return redirect('login')
            else:
                messages.error(request, "Invalid verification code.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = PhoneVerificationForm()

    return render(request, 'defaults/verify_phone.html', {'form': form})

def generate_random_code():

    import secrets
    return secrets.randbelow(10000)
