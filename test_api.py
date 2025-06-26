import requests
import sys
import time

BASE_URL = "http://localhost:5000"

def test_upload_aadhaar():
    print("Testing /upload_aadhaar endpoint...")
    url = f"{BASE_URL}/upload_aadhaar"
    files = {"aadhaar_image": open("Aadhar Card-2.png", "rb")}
    try:
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_verify():
    print("Testing /verify endpoint...")
    url = f"{BASE_URL}/verify"
    files = {
        "aadhar": open("Aadhar Card-2.png", "rb"),
        "selfie": open("Passport_Photograph.jpeg", "rb")
    }
    try:
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Wait for backend to fully initialize
    print("Waiting for backend to initialize (10 seconds)...")
    time.sleep(10)
    
    # Test endpoints
    upload_result = test_upload_aadhaar()
    verify_result = test_verify()
    
    print("\nTest Results:")
    print(f"Upload Aadhaar: {'✅ Passed' if upload_result else '❌ Failed'}")
    print(f"Verify: {'✅ Passed' if verify_result else '❌ Failed'}")

    if not upload_result or not verify_result:
        sys.exit(1) 