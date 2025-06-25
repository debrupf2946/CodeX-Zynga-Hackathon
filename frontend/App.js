import React, { useRef, useState } from "react";
import Webcam from "react-webcam";

const App = () => {
  const webcamRef = useRef(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const capture = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setCapturedImage(imageSrc);
    alert("✅ Selfie captured!");
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setUploadedFile(file);
    alert("✅ Aadhaar uploaded!");
  };

  const handleSubmit = async () => {
    if (!uploadedFile || !capturedImage) {
      alert("⚠️ Please upload Aadhaar and capture a selfie first.");
      return;
    }

    setLoading(true);
    try {
      const blob = await (await fetch(capturedImage)).blob();
      const formData = new FormData();
      formData.append("aadhar", uploadedFile);
      formData.append("selfie", blob, "selfie.jpg");

      const response = await fetch("http://localhost:5000/verify", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setResult(data);
    } catch (err) {
      alert("❌ Error verifying: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Age & Identity Verification</h1>

      <div className="upload-section">
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

      <div style={{ margin: "20px 0", textAlign: "center" }}>
        <Webcam
          audio={false}
          height={240}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          width={240}
          videoConstraints={{ facingMode: "user" }}
          style={{
            borderRadius: "50%",
            border: "3px solid #3b82f6",
            boxShadow: "0 4px 12px rgba(0,0,0,0.2)"
          }}
        />
        <button className="capture-button" onClick={capture} aria-label="Capture Selfie" />
      </div>

      {capturedImage && (
        <div>
          <h3>Selfie Preview:</h3>
          <img
            src={capturedImage}
            alt="Captured"
            style={{
              width: "200px",
              height: "200px",
              borderRadius: "50%",
              border: "3px solid #10b981",
              margin: "10px auto",
              display: "block",
              objectFit: "cover"
            }}
          />
        </div>
      )}

      <button onClick={handleSubmit} disabled={loading} style={{ marginTop: "20px" }}>
        {loading ? "Verifying..." : "Submit"}
      </button>

      {result && (
        <div className="result-section">
          <h3>Verification Result</h3>
          <p><strong>Age:</strong> {result.age}</p>
          <p><strong>Match:</strong> {result.isMatch ? "✅ Likely Same Person" : "❌ Not Same"}</p>
          {result.matchScore !== undefined && (
            <p><strong>Match Confidence:</strong> {result.matchScore.toFixed(2)}%</p>
          )}
          <p><strong>18+:</strong> {result.is18Plus ? "✅ Yes" : "❌ No"}</p>
        </div>
      )}
    </div>
  );
};

export default App;
