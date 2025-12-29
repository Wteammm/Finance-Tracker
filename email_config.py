"""
Email Configuration and Sending Module for Finance Tracker
Handles Gmail SMTP integration for AR payment reminders
"""

import smtplib
import os
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

# Configuration file path
CONFIG_DIR = Path(__file__).parent / 'config'
CONFIG_FILE = CONFIG_DIR / 'email_config.json'

# Ensure config directory exists
CONFIG_DIR.mkdir(exist_ok=True)

def load_email_config():
    """Load email configuration from file"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {
        'email': '',
        'app_password': '',
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'sender_name': 'Finance Tracker'
    }

def save_email_config(config):
    """Save email configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def get_email_template(ar_name, amount, currency='MYR', description=''):
    """
    Generate professional payment reminder email template
    
    Args:
        ar_name: Name of person/company who owes money
        amount: Amount owed
        currency: Currency (default MYR)
        description: Optional description
    
    Returns:
        tuple: (subject, html_body, plain_text_body)
    """
    config = load_email_config()
    sender_name = config.get('sender_name', 'Finance Tracker')
    current_date = datetime.now().strftime('%B %d, %Y')
    
    subject = f"Payment Reminder - {currency} {amount:,.2f} Outstanding"
    
    # HTML version (professional template)
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .header {{
                background: linear-gradient(135deg, #52b788 0%, #40916c 100%);
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 5px 5px 0 0;
            }}
            .content {{
                background-color: white;
                padding: 30px;
                border-radius: 0 0 5px 5px;
            }}
            .amount {{
                font-size: 24px;
                font-weight: bold;
                color: #52b788;
                text-align: center;
                margin: 20px 0;
            }}
            .details {{
                background-color: #f0f0f0;
                padding: 15px;
                border-left: 4px solid #52b788;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                font-size: 12px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Payment Reminder</h2>
            </div>
            <div class="content">
                <p>Dear {ar_name},</p>
                
                <p>This is a friendly reminder regarding your outstanding balance with us.</p>
                
                <div class="amount">
                    {currency} {amount:,.2f}
                </div>
                
                <div class="details">
                    <strong>Payment Details:</strong><br>
                    <strong>Amount Owed:</strong> {currency} {amount:,.2f}<br>
                    <strong>Date:</strong> {current_date}<br>
                    {f'<strong>Description:</strong> {description}<br>' if description else ''}
                </div>
                
                <p>We kindly request that you arrange payment at your earliest convenience.</p>
                
                <p>If you have already made this payment, please disregard this reminder. If you have any questions or concerns regarding this amount, please don't hesitate to contact us.</p>
                
                <p>Thank you for your prompt attention to this matter.</p>
                
                <p>Best regards,<br>
                <strong>{sender_name}</strong></p>
            </div>
            <div class="footer">
                <p>This is an automated reminder from Finance Tracker</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text version (fallback)
    plain_text = f"""
Payment Reminder

Dear {ar_name},

This is a friendly reminder regarding your outstanding balance with us.

AMOUNT OWED: {currency} {amount:,.2f}

Payment Details:
- Amount Owed: {currency} {amount:,.2f}
- Date: {current_date}
{f'- Description: {description}' if description else ''}

We kindly request that you arrange payment at your earliest convenience.

If you have already made this payment, please disregard this reminder. 
If you have any questions or concerns regarding this amount, please don't 
hesitate to contact us.

Thank you for your prompt attention to this matter.

Best regards,
{sender_name}

---
This is an automated reminder from Finance Tracker
    """
    
    return subject, html_body.strip(), plain_text.strip()

def send_email(to_email, subject, html_body, plain_text):
    """
    Send email via Gmail SMTP
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_body: HTML version of email
        plain_text: Plain text version of email
    
    Returns:
        tuple: (success: bool, message: str)
    """
    config = load_email_config()
    
    # Validate configuration
    if not config.get('email') or not config.get('app_password'):
        return False, "Email not configured. Please set up email settings first."
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{config.get('sender_name', 'Finance Tracker')} <{config['email']}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Attach both plain text and HTML versions
        part1 = MIMEText(plain_text, 'plain')
        part2 = MIMEText(html_body, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Connect to Gmail SMTP server
        server = smtplib.SMTP(config.get('smtp_server', 'smtp.gmail.com'), 
                             config.get('smtp_port', 587))
        server.starttls()  # Enable TLS encryption
        
        # Login
        server.login(config['email'], config['app_password'])
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        return True, f"Email sent successfully to {to_email}"
        
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed. Please check your email and app password."
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {str(e)}"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"

def send_payment_reminder(ar_name, to_email, amount, currency='MYR', description=''):
    """
    Send payment reminder email for AR item
    
    Args:
        ar_name: Name of person/company
        to_email: Recipient email
        amount: Amount owed
        currency: Currency (default MYR)
        description: Optional description
    
    Returns:
        tuple: (success: bool, message: str)
    """
    # Generate email template
    subject, html_body, plain_text = get_email_template(ar_name, amount, currency, description)
    
    # Send email
    return send_email(to_email, subject, html_body, plain_text)

def test_email_config(test_email):
    """
    Send a test email to verify configuration
    
    Args:
        test_email: Email address to send test to
    
    Returns:
        tuple: (success: bool, message: str)
    """
    config = load_email_config()
    sender_name = config.get('sender_name', 'Finance Tracker')
    
    subject = "Test Email - Finance Tracker"
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #52b788;">Email Configuration Test</h2>
        <p>This is a test email from Finance Tracker.</p>
        <p>If you received this email, your email configuration is working correctly!</p>
        <p>Best regards,<br>{sender_name}</p>
    </body>
    </html>
    """
    plain_text = f"""
Email Configuration Test

This is a test email from Finance Tracker.

If you received this email, your email configuration is working correctly!

Best regards,
{sender_name}
    """
    
    return send_email(test_email, subject, html_body, plain_text)
