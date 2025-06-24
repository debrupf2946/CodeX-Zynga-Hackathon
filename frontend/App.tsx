import React, { useState, useRef } from "react";
import Webcam from "react-webcam";
import "./styles.css";

const translations = {
  en: {
    title: "Age & Identity Verification",
    upload: "Upload Aadhar Card",
    capture: "Capture Live Selfie",
    captureBtn: "Capture Selfie",
    submit: "Submit for Verification",
    resultTitle: "Verification Result",
    dob: "Date of Birth",
    age: "Age",
    eligible: "✅ Eligible",
    notEligible: "❌ Not Eligible",
    confidence: "Face Match Confidence",
    status: "Status",
    uploaded: "Uploaded",
    error: "Unsupported file type. Please upload a PDF or JPG/PNG image.",
  },
  hi: {
    title: "आयु और पहचान सत्यापन",
    upload: "आधार कार्ड अपलोड करें",
    capture: "सेल्फी कैप्चर करें",
    captureBtn: "सेल्फी लें",
    submit: "सत्यापन के लिए सबमिट करें",
    resultTitle: "सत्यापन परिणाम",
    dob: "जन्म तिथि",
    age: "आयु",
    eligible: "✅ पात्र",
    notEligible: "❌ अपात्र",
    confidence: "चेहरे के मिलान की पुष्टि",
    status: "स्थिति",
    uploaded: "अपलोड किया गया",
    error: "असमर्थित फ़ाइल प्रकार। कृपया PDF या JPG/PNG फ़ाइल अपलोड करें।",
  },
};

export default function App() {
  const [language, setLanguage] = useState("en");
  const t = translations[language];

  const [aadharFile, setAadharFile] = useState<File | null>(null);
  const [aadharPreview, setAadharPreview] = useState<string | null>(null);
  const [aadharError, setAadharError] = useState<string | null>(null);
  const [selfie, setSelfie] = useState<File | null>(null);
  const [captured, setCaptured] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);
  const webcamRef = useRef<Webcam>(null);

  const handleAadharUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const allowedTypes = [
      "application/pdf",
      "image/jpeg",
      "image/jpg",
      "image/png",
    ];
    if (!allowedTypes.includes(file.type)) {
      setAadharError(t.error);
      setAadharFile(null);
      setAadharPreview(null);
      return;
    }
    setAadharError(null);
    setAadharFile(file);
    if (file.type.startsWith("image/")) {
      setAadharPreview(URL.createObjectURL(file));
    } else {
      setAadharPreview(null);
    }
  };

  const captureSelfie = () => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (!imageSrc) return;

    // Flash effect
    const flash = document.createElement("div");
    flash.className = "flash";
    document.body.appendChild(flash);
    setTimeout(() => document.body.removeChild(flash), 300);

    fetch(imageSrc)
      .then((res) => res.blob())
      .then((blob) => {
        const file = new File([blob], "selfie.png", { type: "image/png" });
        setSelfie(file);
        setCaptured(imageSrc);
      });
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

      if (!response.ok) throw new Error("Upload failed");

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      alert("Upload failed: " + err.message);
    }
  };

  return (
    <div className="container">
      <select onChange={(e) => setLanguage(e.target.value)} value={language}>
        <option value="en">English</option>
        <option value="hi">हिंदी</option>
      </select>
      <h1>{t.title}</h1>

      <div className="section">
        <div className="card">
          <h2>{t.upload}</h2>
          <label className="upload-label">
            <input
              type="file"
              accept="application/pdf,image/jpeg,image/jpg,image/png"
              onChange={handleAadharUpload}
            />
            Click to Upload
          </label>
          {aadharError && <p className="error">{aadharError}</p>}
          {aadharFile && (
            <p>
              {t.uploaded}: {aadharFile.name}
            </p>
          )}
          {aadharPreview && (
            <img
              src={aadharPreview}
              alt="Aadhar Preview"
              className="preview-img"
            />
          )}
        </div>

        <div className="card">
          <h2>{t.capture}</h2>
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/png"
            className="webcam"
          />
          <button onClick={captureSelfie}>{t.captureBtn}</button>
          {captured && (
            <img src={captured} alt="Selfie" className="selfie-preview" />
          )}
        </div>
      </div>

      <button className="submit-btn" onClick={handleSubmit}>
        {t.submit}
      </button>

      {result && (
        <div className="results">
          <h2>{t.resultTitle}</h2>
          <p>
            <strong>{t.dob}:</strong> {result.dob}
          </p>
          <p>
            <strong>{t.age}:</strong> {result.age}
          </p>
          <p>
            <strong>{t.eligible}:</strong>{" "}
            {result.is_18_plus ? t.eligible : t.notEligible}
          </p>
          <p>
            <strong>{t.confidence}:</strong> {result.face_match_confidence}%
          </p>
          <p>
            <strong>{t.status}:</strong> {result.status}
          </p>
        </div>
      )}
    </div>
  );
}
