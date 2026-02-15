#!/usr/bin/env python3
"""
Quick test of user forgot password endpoints
"""
import sys
sys.path.insert(0, 'c:\\Users\\Sakhi\\Documents\\GitHub\\HelpReach\\backend_python')

from app import app, user_forgot_password_store
import json

with app.test_client() as client:
    # Test 1: Request OTP
    print("Test 1: Request OTP")
    resp = client.post('/api/user/forgot-password/request-otp', 
                       json={"email": "sakhitapre9@gmail.com"})
    print(f"Status: {resp.status_code}")
    data = json.loads(resp.data)
    print(f"Response: {json.dumps(data, indent=2)}")
    
    if resp.status_code == 200 and data.get("ok"):
        token = data["token"]
        print(f"✅ OTP requested! Token: {token}\n")
        
        # Get the OTP from store
        otp_record = user_forgot_password_store.get(token)
        otp = otp_record["otp"] if otp_record else "000000"
        print(f"Generated OTP: {otp}\n")
        
        # Test 2: Verify OTP
        print("Test 2: Verify OTP")
        resp = client.post('/api/user/forgot-password/verify-otp',
                           json={"token": token, "otp": otp})
        print(f"Status: {resp.status_code}")
        data = json.loads(resp.data)
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if resp.status_code == 200 and data.get("ok"):
            verify_token = data["token"]
            print(f"✅ OTP verified! Verification Token: {verify_token}\n")
            
            # Test 3: Reset Password
            print("Test 3: Reset Password")
            resp = client.post('/api/user/forgot-password/reset-password',
                               json={"token": verify_token, "new_password": "NewPass@123"})
            print(f"Status: {resp.status_code}")
            data = json.loads(resp.data)
            print(f"Response: {json.dumps(data, indent=2)}")
            
            if resp.status_code == 200:
                print(f"✅ Password reset successfully!")
        else:
            print(f"❌ OTP verification failed")
    else:
        print(f"❌ OTP request failed")
