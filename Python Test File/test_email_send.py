#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend_python')
from email_service import send_email

# Test email to your own address
test_email = "your_email@gmail.com"  # Change this to your email

subject = "Test Email from HelpReach"
message = """
This is a test email from HelpReach donation claiming system.

If you received this, the email service is working correctly!

Best regards,
HelpReach Team
"""

print("Sending test email...")
send_email(test_email, subject, message)
print("Test email sent! Check your inbox.")
