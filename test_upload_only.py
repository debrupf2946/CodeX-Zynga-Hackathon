import requests
import json

def test_upload_aadhaar_only():
    """Test only the /upload_aadhaar endpoint"""
    print("Testing /upload_aadhaar endpoint...")
    url = "http://localhost:5000/upload_aadhaar"
    
    try:
        # Use the Aadhaar image file
        with open("Aadhar Card-2.png", "rb") as img_file:
            files = {"aadhaar_image": ("aadhar.png", img_file, "image/png")}
            
            print("Sending request to /upload_aadhaar...")
            response = requests.post(url, files=files)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ SUCCESS! Upload Aadhaar endpoint working")
                result = response.json()
                print("Response:")
                print(json.dumps(result, indent=2))
                
                # Print summary
                print("\n--- Summary ---")
                print(f"DOB: {result.get('dob', 'Not found')}")
                print(f"Age: {result.get('age_years', 'Unknown')} years")
                print(f"18+: {'Yes' if result.get('is_18_plus', False) else 'No'}")
                
            else:
                print(f"❌ FAILED! Status: {response.status_code}")
                print(f"Response: {response.text}")
                
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_upload_aadhaar_only() 