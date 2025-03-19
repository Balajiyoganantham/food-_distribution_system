### **README for Smart Food Redistribution System**

# **Smart Food Redistribution System**
This project is an **AI-powered food redistribution platform** that connects food donors with NGOs to **minimize food waste** and **help communities in need**. It features **real-time tracking, AI-based donor-NGO matching, and automated notifications**.

---

## **🚀 Features**
- **Food Donation System** 📦  
  - Users can donate food with details like type, quantity, location, and expiry date.
  - Calendar and clock input for easy expiry date selection.
  
- **AI-Based Matching** 🤖  
  - Uses an intelligent algorithm to match donations with nearby NGOs efficiently.

- **Real-Time Tracking** 🛰️  
  - Google Maps API integration for tracking donations.

- **Automated Alerts** 📩  
  - Uses **Firebase and WebSockets** for real-time updates.
  - SMS/Email notifications using **Flask-Mail or Twilio**.

- **User Authentication & Management** 🔑  
  - Secure **login and registration** system with Flask.

- **Optimized Food List Display** 📊  
  - **High-quantity food appears first**.  
  - **Expired food is pushed to the bottom** (shown in red).  
  - **Green color** for large food quantities (40+ items).  
  - **Default color** for other cases.

---

## **🛠️ Tech Stack**
| **Technology** | **Purpose** |
|---------------|------------|
| Python (Flask) | Backend & API Development |
| SQLite & SQLAlchemy | Database Management |
| Scikit-learn | AI-Based Matching Algorithm |
| Google Maps API | Location & Real-time Tracking |
| WebSockets | Real-time Notifications |
| Firebase | Push Notifications |
| Flask-Mail / Twilio | Email & SMS Alerts |
| HTML, CSS, JavaScript | Frontend |
| Bootstrap | UI Design |

---

## **📂 Project Structure**
```
smart_food_redistribution/
│── app/
│   ├── __init__.py         # App initialization
│   ├── models.py           # Database models
│   ├── routes.py           # API routes
│   ├── templates/          # HTML templates
│   ├── static/             # CSS, JS, Images
│── migrations/             # Database migrations
│── config.py               # Configuration settings
│── run.py                  # Entry point for running the Flask app
│── README.md               # Project documentation
│── requirements.txt        # Dependencies list
```

---

## **⚙️ Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-repo-url.git
cd smart_food_redistribution
```

### **2️⃣ Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Database**
```bash
flask db upgrade
```

### **5️⃣ Run the Application**
```bash
flask run
```
- Open **`http://127.0.0.1:5000/`** in your browser.

---

## **🔗 API Endpoints**
| **Method** | **Endpoint** | **Description** |
|-----------|------------|----------------|
| **GET**   | `/`        | Home Page |
| **GET**   | `/donate_food` | Food Donation Form |
| **POST**  | `/donate_food` | Submit a food donation |
| **GET**   | `/food_list` | View available food donations |
| **GET**   | `/track_donation` | Track donation in real time |
| **GET**   | `/register` | User Registration |
| **POST**  | `/register` | Register new user |
| **GET**   | `/login` | User Login |
| **POST**  | `/login` | Authenticate user |
| **GET**   | `/logout` | Log out user |

---

## **🔍 Future Enhancements**
✅ **Machine Learning-based demand prediction**  
✅ **Multi-language support**  
✅ **Mobile app version**  


