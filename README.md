# 🚀 AI Notify Hub: Smart Digital Notice Board System

AI Notify Hub ek **Smart Digital Notice Board System** hai jo traditional paper-based notice boards ko real-time, centralized, aur AI-powered solution se replace karta hai. 

---

## 📌 Overview
Is system ke zariye administrators notices, timetables, aur alerts ko web-based panel se manage karte hain jo foran **Smart LCD/LED screens** par internet ke zariye display ho jate hain. Isme university queries solve karne ke liye aik **AI Assistant (Gemini)** bhi integrated hai.

## 🎯 Key Features
* **Real-time Synchronization:** Wi-Fi ke zariye instant notice updates.
* **AI Chatbot:** Students ke sawalon ke liye intelligent assistant.
* **Comprehensive Management:** Exam schedules, alerts, aur achievements ka portal.
* **Paperless Ecosystem:** University communication ka modern aur green hal.

## 🛠️ Tech Stack
* **Web:** React.js, Node.js, Express.js
* **Database:** MongoDB
* **Display:** Python (PyQt5)
* **Intelligence:** Google Gemini API

---

## 📸 Screenshots & Previews
| **Admin Dashboard** | **Smart LCD Display** |
|:---:|:---:|
| ![Dashboard](./screenshots/dashboard.png) | ![Display](./screenshots/display.png) |

> **Tip:** Apne project mein `screenshots` folder bana kar usme `dashboard.png` aur `display.png` rakhein taake wo yahan nazar aayen.

---

## ⚙️ Setup & Run Guide
Niche di gayi commands ko terminal mein step-by-step run karein:

```bash
# 1. Clone the Project
git clone [https://github.com/your-username/ai-notify-hub.git](https://github.com/your-username/ai-notify-hub.git)
cd ai-notify-hub

# 2. Run Admin Panel & Backend (Terminal 1)
cd admin_portal && npm install && npm start


# 3. Run LCD Display App (Terminal 2)
cd ../lcd_display && pip install -r requirements.txt && python main.py
