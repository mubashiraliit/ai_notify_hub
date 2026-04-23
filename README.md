# 🚀 AI Notify Hub: Smart Digital Notice Board System

AI Notify Hub is an advanced **Smart Digital Notice Board System** designed to replace traditional paper-based communication with a **real-time, centralized, and AI-powered solution**.

---

## 📌 Overview
This system enables administrators to manage notices, timetables, and urgent alerts through a unified web-based panel. All updates are instantly broadcasted to **Smart LCD/LED screens** over the internet. To enhance student experience, the system features an **AI Assistant** powered by the Gemini API to provide instant answers to university-related queries.

---

## 🎯 Key Features
* **Real-time Synchronization:** Instant updates delivered via Wi-Fi to all connected displays.
* **AI Chatbot Integration:** Intelligent query handling for student schedules and FAQs.
* **Centralized Dashboard:** A single portal to manage exam schedules, alerts, and achievements.
* **Smart Display Engine:** A high-performance Python/PyQt5 interface designed for large-scale screens.
* **Eco-Friendly Initiative:** A 100% paperless solution for modern campuses.

---

## 🛠️ Tech Stack
* **Frontend:** React.js
* **Backend:** Node.js & Express.js
* **Database:** MongoDB
* **Display Engine:** Python (PyQt5)
* **AI Model:** Google Gemini API

---

## 📸 System Previews

| **Admin Control Panel** | **Smart LCD Interface** |
|:---:|:---:|
| ![Dashboard](./screenshots/dashboard.png) | ![Display](./screenshots/display.png) |

> **Setup Note:** Create a `/screenshots` folder in your root directory and place your images named `dashboard.png` and `display.png` there to see them in this table.

---

## ⚙️ Setup & Installation

Run the following commands in your terminal to get the full system up and running:

```bash
# 1. Clone the repository
git clone [https://github.com/your-username/ai-notify-hub.git](https://github.com/your-username/ai-notify-hub.git)
cd ai-notify-hub

# 2. Launch Admin Portal & Backend (Terminal 1)
cd admin_portal && npm install && npm start

# 3. Launch LCD Display Interface (Terminal 2)
# Navigate to the lcd_display directory from the root
cd lcd_display && pip install -r requirements.txt && python main.py
