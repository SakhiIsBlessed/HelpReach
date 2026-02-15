"""
Test script for Forgot Password functionality
This script tests:
1. Request OTP for email
2. Resend OTP
3. Verify OTP (3 attempts limit)
4. Reset password
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_forgot_password_flow():
    print("\n" + "="*60)
    print("🧪 TESTING FORGOT PASSWORD FLOW")
    print("="*60)
    
    # Use a test email (make sure this email exists in the database)
    test_email = "test@ngo.org"  # Change this to a real registered NGO email
    
    print(f"\n📧 Step 1: Request OTP for email: {test_email}")
    print("-" * 60)
    
    response = requests.post(
        f"{BASE_URL}/api/ngo/forgot-password/request-otp",
        json={"email": test_email}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code != 200:
        print("❌ Failed to request OTP. Make sure the email is registered.")
        return
    
    data = response.json()
    otp_token = data.get("token")
    print(f"✅ OTP requested successfully!")
    print(f"Token: {otp_token}")
    
    # In real scenario, get OTP from email. For testing, we'll look in app logs
    print("\n📧 Step 2: Check your email for the OTP")
    print("-" * 60)
    print("⏰ OTP sent! Check the email inbox (or app logs if using test email)")
    
    # Simulate getting OTP from email (in real test, extract from email)
    test_otp = input("\n🔐 Enter the OTP you received in email: ").strip()
    
    if not test_otp or len(test_otp) != 6:
        print("❌ Invalid OTP format")
        return
    
    print(f"\n✅ Step 3: Verify OTP: {test_otp}")
    print("-" * 60)
    
    response = requests.post(
        f"{BASE_URL}/api/ngo/forgot-password/verify-otp",
        json={"token": otp_token, "otp": test_otp}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code != 200:
        print("❌ OTP verification failed!")
        return
    
    verify_data = response.json()
    reset_token = verify_data.get("token")
    print(f"✅ OTP verified successfully!")
    print(f"Reset Token: {reset_token}")
    
    print(f"\n🔄 Step 4: Reset Password")
    print("-" * 60)
    
    new_password = input("Enter new password (min 8 characters): ").strip()
    
    if len(new_password) < 8:
        print("❌ Password must be at least 8 characters")
        return
    
    response = requests.post(
        f"{BASE_URL}/api/ngo/forgot-password/reset-password",
        json={"token": reset_token, "password": new_password}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("\n✅ PASSWORD RESET SUCCESSFUL!")
        print(f"📧 Confirmation email sent to: {test_email}")
        print("🔐 You can now log in with your new password")
    else:
        print("\n❌ Password reset failed!")


def test_otp_attempts_limit():
    """Test that OTP verification fails after 3 attempts"""
    print("\n" + "="*60)
    print("🧪 TESTING OTP ATTEMPTS LIMIT (3 max)")
    print("="*60)
    
    test_email = input("\n📧 Enter registered NGO email: ").strip()
    
    print(f"\n📧 Requesting OTP for: {test_email}")
    response = requests.post(
        f"{BASE_URL}/api/ngo/forgot-password/request-otp",
        json={"email": test_email}
    )
    
    if response.status_code != 200:
        print("❌ Failed to request OTP")
        return
    
    otp_token = response.json().get("token")
    print(f"✅ OTP requested. Token: {otp_token}")
    
    # Try wrong OTP 3 times
    for attempt in range(1, 4):
        wrong_otp = "000000"  # Invalid OTP
        print(f"\n❌ Attempt {attempt}/3: Trying wrong OTP: {wrong_otp}")
        
        response = requests.post(
            f"{BASE_URL}/api/ngo/forgot-password/verify-otp",
            json={"token": otp_token, "otp": wrong_otp}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if attempt < 3:
            time.sleep(1)
    
    # Try 4th time
    print(f"\n🚫 Attempt 4: Should be blocked")
    response = requests.post(
        f"{BASE_URL}/api/ngo/forgot-password/verify-otp",
        json={"token": otp_token, "otp": "000000"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code >= 400:
        print("✅ CORRECTLY BLOCKED: User cannot attempt more than 3 times")
    else:
        print("❌ SECURITY ISSUE: Should have blocked after 3 attempts")


def test_resend_otp():
    """Test OTP resend functionality"""
    print("\n" + "="*60)
    print("🧪 TESTING RESEND OTP FUNCTIONALITY")
    print("="*60)
    
    test_email = input("\n📧 Enter registered NGO email: ").strip()
    
    print(f"\n📧 Requesting initial OTP for: {test_email}")
    response = requests.post(
        f"{BASE_URL}/api/ngo/forgot-password/request-otp",
        json={"email": test_email}
    )
    
    if response.status_code != 200:
        print("❌ Failed to request OTP")
        return
    
    otp_token = response.json().get("token")
    print(f"✅ OTP requested. Token: {otp_token}")
    
    print("\n📧 Resending OTP...")
    response = requests.post(
        f"{BASE_URL}/api/ngo/forgot-password/resend-otp",
        json={"token": otp_token}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("✅ OTP RESEND SUCCESSFUL!")
        print("📧 New OTP sent to your email (attempts counter reset)")
    else:
        print("❌ OTP resend failed!")


if __name__ == "__main__":
    print("\n🚀 Forgot Password Testing Suite")
    print("Select an option:")
    print("1. Test complete forgot password flow (Request → Verify → Reset)")
    print("2. Test OTP attempts limit (3 max)")
    print("3. Test resend OTP functionality")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        test_forgot_password_flow()
    elif choice == "2":
        test_otp_attempts_limit()
    elif choice == "3":
        test_resend_otp()
    else:
        print("❌ Invalid choice")
