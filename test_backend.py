import requests
import json

def test_upload_aadhaar():
    """Test the /upload_aadhaar endpoint with an image file."""
    url = "http://localhost:5000/upload_aadhaar"
    
    # Open the image file in binary mode
    with open("Aadhar Card-2.png", "rb") as img_file:
        # Create the multipart form data with the image file
        files = {"aadhaar_image": ("aadhar.png", img_file, "image/png")}
        
        # Send the POST request
        response = requests.post(url, files=files)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Success! API responded with:")
            try:
                # Try to parse the response as JSON
                result = response.json()
                print(json.dumps(result, indent=2))
            except:
                # If JSON parsing fails, print the raw response
                print(response.text)
        else:
            print(f"Error: API returned status code {response.status_code}")
            print(response.text)

def test_verify_faces():
    """Test the /verify endpoint with both Aadhaar and selfie images."""
    url = "http://localhost:5000/verify"
    
    # Open both image files in binary mode
    with open("Aadhar Card-2.png", "rb") as aadhar_file, \
         open("Passport_Photograph.jpeg", "rb") as selfie_file:
        
        # Create the multipart form data with both image files
        files = {
            "aadhar": ("aadhar.png", aadhar_file, "image/png"),
            "selfie": ("selfie.jpg", selfie_file, "image/jpeg")
        }
        
        # Send the POST request
        print("Sending request to /verify endpoint...")
        response = requests.post(url, files=files)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Success! Verification API responded with:")
            try:
                # Try to parse the response as JSON
                result = response.json()
                print(json.dumps(result, indent=2))
                
                # Print a human-readable summary
                print("\nSummary:")
                print(f"DOB: {result.get('dob', 'Not found')}")
                print(f"Age: {result.get('age', 'Unknown')}")
                print(f"18+: {'Yes' if result.get('is18Plus', False) else 'No'}")
                print(f"Face Match: {'Yes' if result.get('isMatch', False) else 'No'}")
                if 'matchScore' in result:
                    print(f"Match Confidence: {result['matchScore']:.2f}%")
                
            except Exception as e:
                # If JSON parsing fails, print the raw response
                print(f"Error parsing JSON: {e}")
                print("Raw response:", response.text)
        else:
            print(f"Error: API returned status code {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    print("Testing backend API...")
    print("\n=== Testing /verify endpoint ===")
    test_verify_faces() 