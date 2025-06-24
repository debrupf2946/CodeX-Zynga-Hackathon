import React, { useRef, useState } from "react";
import Webcam from "react-webcam";

const App = () => {
  const webcamRef = useRef(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);

  const capture = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setCapturedImage(imageSrc);
    alert("Selfie captured!");
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setUploadedFile(file);
    alert("Aadhaar uploaded!");
  };

  const handleSubmit = () => {
    alert("Form submitted!");
    // Future: send data to backend here
  };

  return (
    <div className="container">
      <h1>Age Verification</h1>

      <div>
        <label>Upload Aadhaar (PDF/JPG/PNG): </label>
        <input type="file" accept=".pdf,.jpg,.jpeg,.png" onChange={handleFileChange} />
      </div>

      {uploadedFile && (
        <div>
          <h3>Aadhaar Preview:</h3>
          <img
            src={URL.createObjectURL(uploadedFile)}
            alt="Aadhaar Preview"
            style={{ width: "100%", borderRadius: "10px" }}
          />
        </div>
      )}

      <div style={{ margin: "20px 0" }}>
        <Webcam
          audio={false}
          height={300}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          width={300}
          videoConstraints={{ facingMode: "user" }}
          style={{ borderRadius: "50%" }}
        />
      </div>

      <button onClick={capture}>Capture Selfie</button>

      {capturedImage && (
        <div>
          <h3>Selfie Preview:</h3>
          <img
            src={capturedImage}
            alt="Captured"
            style={{ width: "100%", borderRadius: "10px", marginTop: "10px" }}
          />
        </div>
      )}

      <button onClick={handleSubmit} style={{ marginTop: "20px" }}>Submit</button>
    </div>
  );
};

export default App;
