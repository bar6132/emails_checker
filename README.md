## **Project: Email Notification Service**

---

### **Overview**
This project is a Python-based email notification service that checks your Gmail inbox periodically for new emails. It sends desktop notifications with the sender's email address and subject of the message. You can configure the project to run as a background Windows service.

---

### **Features**
- Periodically checks for unread emails using IMAP.
- Sends desktop notifications with:
- Sender's email address.
- Subject of the unread email.
- Logs processed email IDs to prevent duplicate notifications.
- Clickable notifications to open Gmail directly.
- Easily configurable using environment variables.

---

### **Setup Instructions**

#### **1. Clone the Repository**
Clone the repository to your local machine:
```bash
git clone <repository_url>
cd <repository_folder>
```

#### **2. Install Dependencies**
Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # For Windows
```
Install required Python libraries:
```bash
pip install -r requirements.txt
```

#### **3. Configure Environment Variables**
Create a `.env` file in the project directory:
```makefile
IMAP_SERVER=imap.gmail.com
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```
Enable IMAP on Gmail:
- Go to Gmail settings → Forwarding and POP/IMAP.
- Enable IMAP access.

Generate an App Password:
- Visit Google App Passwords.
- Generate a password for "Mail" and "Windows" and use it in the `EMAIL_PASS` field.

#### **4. Run the Script**
Run the script manually to ensure it works:
```bash
python reminder_service.py
```
The script will check your Gmail inbox every minute for new emails. Notifications will appear for unread emails.

#### **5. Make It a Background Windows Service**

##### **Using a .bat File**
Create a file named `start_service.bat` in the project directory. Add the following content:
```bat
@echo off
pythonw "C:\path\to\your\project\reminder_service.py"
exit
```
Replace `C:\path\to\your\project\reminder_service.py` with the full path to your Python script.

**How to Use:**
- Double-click `start_service.bat` to run the script in the background.
- Notifications will start appearing as per the schedule.

##### **Using a .vbs File**
Create a file named `start_service.vbs` in the project directory. Add the following content:
```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "C:\path\to\your\project\start_service.bat", 0
```
Replace `C:\path\to\your\project\start_service.bat` with the full path to your `.bat` file.

**How to Use:**
- Double-click `start_service.vbs` to run the `.bat` file invisibly.
- This ensures the script runs silently in the background.

