from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import random
import string
import logging

logger = logging.getLogger(__name__)

def generate_otp():
    """Generate a 6-digit OTP code"""
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(user):
    """
    Send OTP email to user for verification
    """
    try:
        # Generate OTP
        otp_code = generate_otp()
        
        # Email subject and content
        subject = f'🔐 Your Verification Code: {otp_code}'
        
        # HTML email template
        html_message = f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Arial', sans-serif; margin: 0; padding: 0; background-color: #f7f9fc; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
                .content {{ padding: 40px 30px; }}
                .otp-box {{ background: #f8f9fa; border: 2px dashed #6c757d; border-radius: 10px; padding: 20px; margin: 20px 0; text-align: center; }}
                .otp-code {{ font-size: 32px; font-weight: bold; color: #495057; letter-spacing: 5px; }}
                .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #6c757d; font-size: 12px; }}
                .btn {{ display: inline-block; background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 Task Manager Pro</h1>
                    <p>Email Verification Required</p>
                </div>
                <div class="content">
                    <h2>Hello {user.username}!</h2>
                    <p>Welcome to Task Manager Pro! Please verify your email address to complete your registration.</p>
                    
                    <div class="otp-box">
                        <p><strong>Your Verification Code:</strong></p>
                        <div class="otp-code">{otp_code}</div>
                        <p><small>⏰ This code expires in 5 minutes</small></p>
                    </div>
                    
                    <p>Enter this code on the verification page to activate your account.</p>
                    
                    <p><strong>Security Tips:</strong></p>
                    <ul>
                        <li>Never share this code with anyone</li>
                        <li>We'll never ask for this code via phone or email</li>
                        <li>If you didn't request this, please ignore this email</li>
                    </ul>
                </div>
                <div class="footer">
                    <p>This email was sent to {user.email}</p>
                    <p>© 2024 Task Manager Pro. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        plain_message = f"""
        Task Manager Pro - Email Verification
        
        Hello {user.username}!
        
        Welcome to Task Manager Pro! Please verify your email address to complete your registration.
        
        Your Verification Code: {otp_code}
        
        This code expires in 5 minutes.
        
        Enter this code on the verification page to activate your account.
        
        If you didn't request this, please ignore this email.
        
        Thank you!
        Task Manager Pro Team
        """
        
        # Send email
        sent = send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        if sent:
            logger.info(f"OTP email sent successfully to {user.email}")
            # Store OTP in session instead of database
            return True, otp_code
        else:
            logger.error(f"Failed to send OTP email to {user.email}")
            return False, "Failed to send email. Please try again."
            
    except Exception as e:
        logger.error(f"Error sending OTP email to {user.email}: {str(e)}")
        return False, f"Error sending email: {str(e)}"

def verify_otp(session_otp, input_otp):
    """
    Verify OTP code
    """
    try:
        if session_otp == input_otp:
            return True, "Email verified successfully!"
        else:
            return False, "Invalid OTP code."
            
    except Exception as e:
        logger.error(f"Error verifying OTP: {str(e)}")
        return False, "Verification failed. Please try again."