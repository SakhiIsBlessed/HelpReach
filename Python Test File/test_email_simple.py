#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend_python')
from email_service import send_email

print("=" * 60)
print("🧪 TESTING EMAIL SERVICE")
print("=" * 60)

test_email = "sakhitapre9@gmail.com"
subject = "Test Email from HelpReach"
message = """
Hello,

This is a test email from HelpReach.

If you receive this, the email service is working!

Best regards,
HelpReach Team
"""

print(f"\nAttempting to send test email to: {test_email}")
print("-" * 60)

result = send_email(test_email, subject, message)

print("-" * 60)
if result:
    print("✅ TEST PASSED: Email sent successfully!")
else:
    print("❌ TEST FAILED: Email could not be sent!")
    print("\nPossible issues:")
    print("1. Gmail App Password is incorrect or expired")
    print("2. Less secure apps are disabled")
    print("3. Network connectivity issue")
    print("4. Gmail account has 2FA enabled without app password")

print("=" * 60)
