from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from typing import List, Dict 
from pathlib import Path

from app.core.config import settings # Your application settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
    # TEMPLATE_FOLDER=Path(__file__).parent / 'templates' / 'email', # Optional: if using .html templates
    # For now, let's not assume a template folder structure unless specifically created
)

fm = FastMail(conf)

async def send_email(
    recipients: List[EmailStr],
    subject: str,
    html_body: str | None = None,
    template_name: str | None = None, # Not used if TEMPLATE_FOLDER is commented out
    template_body: Dict[str, any] | None = None, # Changed to Dict[str, any] for more flexibility
    ):

    if settings.MAIL_CONSOLE_OUTPUT:
        print("---- EMAIL TO BE SENT (CONSOLE OUTPUT ENABLED) ----")
        print(f"To: {', '.join(recipients)}")
        print(f"Subject: {subject}")
        if template_name and template_body:
            print(f"Template: {template_name}") # This branch won't be hit if TEMPLATE_FOLDER is not set
            print(f"Body/Context: {template_body}")
        else:
            print(f"HTML Body (first 100 chars): {html_body[:100] if html_body else 'N/A'}...")
        print("---- END OF EMAIL PREVIEW ----")
        # If only console output is desired for testing and no actual email sending:
        # return # Uncomment this line if you want to prevent actual email sending during console output mode

    # Determine message content and subtype
    message_text_content: str | None = None
    if template_name and conf.TEMPLATE_FOLDER and template_body:
        # This case is for when using fastapi-mail's template rendering
        # The 'body' field of MessageSchema will be the context dict for the template
        message_data_for_schema = template_body
        message_subtype = MessageType.html # Assuming templates are HTML
    elif html_body:
        message_data_for_schema = html_body
        message_subtype = MessageType.html
    else:
        # Fallback to a very plain text body if nothing else is provided
        message_text_content = "This is a plain text email body if no html_body or template is provided."
        message_data_for_schema = message_text_content
        message_subtype = MessageType.plain
        
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=message_data_for_schema, # This is either HTML string or context dict for template
        subtype=message_subtype,
    )

    try:
        if template_name and conf.TEMPLATE_FOLDER: # Check if template rendering is intended
            await fm.send_message(message, template_name=template_name)
        else:
            # If not using templates or TEMPLATE_FOLDER is not set, send as is (html or plain)
            await fm.send_message(message)
        # print(f"Email sent to {', '.join(recipients)} with subject: {subject}") # Optional success log
    except Exception as e:
        print(f"Error sending email via fastapi-mail: {e}")
        # In a real app, you might want to raise an exception or handle this more gracefully

async def send_password_reset_email(recipient_email: EmailStr, username: str, token: str):
    subject = f"{settings.MAIL_FROM_NAME} - Password Reset Request"
    # In a real app, frontend_url should come from settings or be constructed more robustly
    frontend_url = "http://localhost:5173" # Assuming Vite's default dev port for frontend
    reset_link = f"{frontend_url}/reset-password?token={token}"
    
    html_content = f"""
    <p>Hello {username},</p>
    <p>You requested a password reset for your account with {settings.MAIL_FROM_NAME}.</p>
    <p>Click this link to reset your password: <a href="{reset_link}">{reset_link}</a></p>
    <p>If you did not request this, please ignore this email.</p>
    <p>Thanks,</p>
    <p>The {settings.MAIL_FROM_NAME} Team</p>
    """
    await send_email(
        recipients=[recipient_email],
        subject=subject,
        html_body=html_content
    )

async def send_email_verification_email(recipient_email: EmailStr, username: str, token: str):
    subject = f"{settings.MAIL_FROM_NAME} - Verify Your Email Address"
    frontend_url = "http://localhost:5173"
    verification_link = f"{frontend_url}/verify-email?token={token}"
    
    html_content = f"""
    <p>Hello {username},</p>
    <p>Thanks for signing up with {settings.MAIL_FROM_NAME}! Please verify your email address by clicking the link below:</p>
    <p><a href="{verification_link}">{verification_link}</a></p>
    <p>If you did not sign up for this account, please ignore this email.</p>
    <p>Thanks,</p>
    <p>The {settings.MAIL_FROM_NAME} Team</p>
    """
    await send_email(
        recipients=[recipient_email],
        subject=subject,
        html_body=html_content
    )
