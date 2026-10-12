# 📦 Installation & Setup Guide

This page contains copy-pasteable commands to quickly install all required Python packages for the **Solar Battery Health Monitor & AI Messenger**.

---

## ⚡ Option 1: Install Everything in One Command (Recommended)

Copy and paste this line directly into your terminal (PowerShell, Command Prompt, or VS Code Terminal):

```bash
pip install -r requirements.txt
```

Or install all dependencies explicitly in a single command:

```bash
pip install google-generativeai pyserial requests scikit-learn pandas numpy joblib
```

---

## 🤖 Option 2: Install Google Gemini AI Library Only

If you already have other dependencies and only need the Google Gemini AI library:

```bash
pip install google-generativeai
```

---

## ✅ Verify Your Installation

Run this one-liner to verify that all modules are properly recognized by Python:

```bash
python -c "import google.generativeai, serial, sklearn, requests; print('✅ All libraries installed successfully!')"
```

If it prints `✅ All libraries installed successfully!`, you are good to go!

---

## 🔑 Configure Your Google Gemini API Key

1. Get a free API key from [Google AI Studio](https://aistudio.google.com).
2. Open [`live_monitor.py`](live_monitor.py) and paste your key on line 51:

```python
GEMINI_API_KEY = "AIzaSy..."  # Replace with your actual Gemini API key
```

---

## 🚀 Running the Project

### 1. Train the ML Model (Run Once)
```bash
python train_model.py
```

### 2. Start Live Monitoring & AI Telegram Alerts
```bash
python live_monitor.py
```

---

## 🛠️ Troubleshooting

- **`pip` is not recognized?**  
  Run with Python module flag:
  ```bash
  python -m pip install google-generativeai pyserial requests scikit-learn pandas numpy joblib
  ```

- **Need to upgrade pip?**
  ```bash
  python -m pip install --upgrade pip
  ```
