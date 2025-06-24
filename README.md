# CodeX-Zynga-Hackathon

A Proof-of-Concept web application that verifies an individual's age and identity using a **simulated Aadhar card image/PDF** and a **live selfie**.

> ⚠️ This is a **proof-of-concept only**. It does not use real government APIs or data. Built for educational and hackathon purposes.

---

##  Problem Statement

Design a web-based system that can:
-  Extract **Date of Birth (DOB)** and **Photo** from a simulated Aadhar card.
-  Compare the extracted Aadhar photo with a **live selfie**.
-  Verify if the person matches the document and is **18+ years old**.

---

##  Features

-  Upload simulated Aadhar card (image or PDF).
-  Extract DOB and image using **OCR (Tesseract)**.
-  Capture live selfie via webcam.
-  Compare Aadhar photo and selfie using **FaceNet/DeepFace**.
-  Show **confidence score** (e.g., "Match: 87%").
-  Feedback on blurry/poor lighting selfies.
-  Support for **multi-language OCR** (optional).
-  Local file-based storage to ensure basic **data privacy**.

---

##  Architecture Overview

```txt
User Input (Aadhar + Selfie)
        │
        ▼
Frontend (React/Next.js)
        │
        ▼
Backend (Flask/FastAPI)
 ├── OCR Module (Tesseract)
 ├── Face Comparison (FaceNet/MobileFaceNet)
 └── Age Verification Logic
