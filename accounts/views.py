from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import SignupForm, LoginForm, OTPVerificationForm
from .models import CustomUser, UserProfile
from .utils import send_otp_email, verify_otp

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Store user data in session
            user_data = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password1']
            }
            request.session['user_data'] = user_data
            
            # Create temporary user object for OTP
            temp_user = CustomUser(
                username=user_data['username'],
                email=user_data['email']
            )
            
            # Send OTP email
            success, otp = send_otp_email(temp_user)
            if success:
                # Store OTP in session
                request.session['otp_code'] = otp
                request.session['verification_email'] = temp_user.email
                messages.success(request, 'Please check your email for verification code.')
                return redirect('verify_email')
            else:
                messages.error(request, f'Failed to send verification email: {otp}')
    else:
        form = SignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def verify_email_view(request):
    user_data = request.session.get('user_data')
    verification_email = request.session.get('verification_email')
    session_otp = request.session.get('otp_code')
    
    if not user_data or not verification_email or not session_otp:
        messages.error(request, 'No pending verification found.')
        return redirect('signup')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            input_otp = form.cleaned_data['otp_code']
            success, message = verify_otp(session_otp, input_otp)
            
            if success:
                try:
                    # Check if user already exists
                    if CustomUser.objects.filter(email=user_data['email']).exists():
                        messages.error(request, 'A user with this email already exists.')
                        return redirect('signup')
                    
                    # Create the actual user
                    user = CustomUser.objects.create_user(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=user_data['password']
                    )
                    user.is_email_verified = True
                    user.save()
                    
                    # Clear session data
                    del request.session['user_data']
                    del request.session['verification_email']
                    del request.session['otp_code']
                    
                    messages.success(request, 'Email verified successfully! You can now login.')
                    return redirect('login')
                except Exception as e:
                    messages.error(request, f'Error creating user: {str(e)}')
                    return redirect('signup')
            else:
                messages.error(request, message)
    else:
        form = OTPVerificationForm()
    
    return render(request, 'accounts/verify_email.html', {
        'form': form,
        'email': verification_email
    })

def resend_otp_view(request):
    if request.method == 'POST':
        user_data = request.session.get('user_data')
        verification_email = request.session.get('verification_email')
        
        if not user_data or not verification_email:
            return JsonResponse({
                'success': False,
                'message': 'No pending verification found.'
            })
        
        # Create temporary user object for sending OTP
        temp_user = CustomUser(
            username=user_data['username'],
            email=user_data['email']
        )
        
        success, otp = send_otp_email(temp_user)
        if success:
            # Update OTP in session
            request.session['otp_code'] = otp
            return JsonResponse({
                'success': True,
                'message': 'OTP sent successfully!'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': otp
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'task_list')
            return redirect(next_url)
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'profile': request.user.userprofile
    })

@login_required
def update_profile_view(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        
        # Update profile picture if provided
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']
        
        # Update bio
        profile.bio = request.POST.get('bio', '')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return redirect('profile')

@login_required
def profile_settings_view(request):
    if request.method == 'POST':
        # Get the user and profile
        user = request.user
        profile = user.userprofile
        
        # Update user fields
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        
        # Update profile fields
        profile.phone_number = request.POST.get('phone_number')
        profile.bio = request.POST.get('bio')
        
        # Handle profile picture upload
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']
        
        try:
            user.save()
            profile.save()
            messages.success(request, 'Profile updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
        
        return redirect('profile_settings')
    
    return render(request, 'accounts/profile_settings.html')
