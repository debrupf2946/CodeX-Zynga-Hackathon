import React, { useRef, useState } from "react";
import Webcam from "react-webcam";

const App = () => {
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);

  const [capturedImage, setCapturedImage] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [cameraError, setCameraError] = useState(false);
  const [isBlurry, setIsBlurry] = useState(false);

  // Blurriness detection
  const isImageBlurry = (image) => {
    return new Promise((resolve) => {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      const img = new Image();
      img.src = image;

      img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);
        const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        let total = 0;

        for (let i = 0; i < imgData.data.length; i += 4) {
          const gray =
            0.299 * imgData.data[i] +
            0.587 * imgData.data[i + 1] +
            0.114 * imgData.data[i + 2];
          total += gray;
        }

        const mean = total / (imgData.data.length / 4);
        let variance = 0;

        for (let i = 0; i < imgData.data.length; i += 4) {
          const gray =
            0.299 * imgData.data[i] +
            0.587 * imgData.data[i + 1] +
            0.114 * imgData.data[i + 2];
          variance += Math.pow(gray - mean, 2);
        }

        variance = variance / (imgData.data.length / 4);
        resolve(variance < 100); // adjust threshold if needed
      };
    });
  };

  const capture = async () => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (!imageSrc) {
      alert("⚠️ Failed to capture. Make sure your camera is allowed and working.");
      return;
    }

    const blurry = await isImageBlurry(imageSrc);
    setCapturedImage(imageSrc);
    setIsBlurry(blurry);

    if (blurry) {
      alert("⚠️ This image is blurry. Please retake the selfie.");
    } else {
      alert("✅ Selfie captured clearly!");
    }
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

    if (isBlurry) {
      alert("⚠️ Cannot submit a blurry selfie. Please retake it.");
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
        <input
          type="file"
          accept=".pdf,.jpg,.jpeg,.png"
          onChange={handleFileChange}
        />
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
          onUserMediaError={() => setCameraError(true)}
          style={{
            borderRadius: "50%",
            border: "3px solid #3b82f6",
            boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
            backgroundColor: "#ddd"
          }}
        />
        {cameraError && (
          <p style={{ color: "red", marginTop: "10px" }}>
            ❌ Camera access denied or not working. Please enable it in your browser settings.
          </p>
        )}
        <button className="capture-button" onClick={capture} aria-label="Capture Selfie">
          Capture Selfie
        </button>
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
              objectFit: "cover",
            }}
          />
          {isBlurry && (
            <p style={{ color: "orange", textAlign: "center" }}>
              ⚠️ This selfie appears blurry. Please retake it.
            </p>
          )}
        </div>
      )}

      <button
        onClick={handleSubmit}
        disabled={loading}
        style={{ marginTop: "20px" }}
      >
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

      {/* Hidden canvas for processing */}
      <canvas ref={canvasRef} style={{ display: "none" }} />
    </div>
  );
};

export default App;
