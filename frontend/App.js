import React, { useState, useRef } from "react";
import Webcam from "react-webcam";
import "./style.css";

function App() {
  const [aadharFile, setAadharFile] = useState(null);
  const [selfie, setSelfie] = useState(null);
  const [result, setResult] = useState(null);
  const webcamRef = useRef(null);

  const handleFileChange = (e) => {
    setAadharFile(e.target.files[0]);
  };

  const capture = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    fetch(imageSrc)
      .then(res => res.blob())
      .then(blob => {
        const selfieFile = new File([blob], "selfie.jpg", { type: "image/jpeg" });
        setSelfie(selfieFile);
        flashScreen();
      });
  };

  const flashScreen = () => {
    const flash = document.createElement("div");
    flash.className = "flash";
    document.body.appendChild(flash);
    setTimeout(() => document.body.removeChild(flash), 300);
    const audio = new Audio("https://actions.google.com/sounds/v1/camera/camera_click.ogg");
    audio.play();
  };

  const handleSubmit = async () => {
    if (!aadharFile || !selfie) {
      alert("Please upload Aadhar and capture Selfie");
      return;
    }

    const formData = new FormData();
    formData.append("aadhar", aadharFile);
    formData.append("selfie", selfie);

    try {
      const response = await fetch("http://localhost:5000/api/verify", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to send files to server.");
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      alert("Upload failed: " + error.message);
    }
  };

  return (
    <div className="container">
      <h1>Age Verification</h1>

      <div className="upload-section">
        <label htmlFor="aadhar">Upload Aadhar (PDF/JPG/PNG):</label>
        <input
          id="aadhar"
          type="file"
          accept=".pdf,.png,.jpg,.jpeg"
          onChange={handleFileChange}
        />
      </div>

      <div className="webcam-section">
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          width={300}
          height={300}
          videoConstraints={{ facingMode: "user" }}
          style={{ borderRadius: "50%" }}
        />
        <button onClick={capture}>Capture Selfie</button>
      </div>

      <button onClick={handleSubmit} className="submit-button">Submit</button>

      {result && (
        <div className="result">
          <h3>Server Response:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;