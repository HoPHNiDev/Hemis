> [!IMPORTANT]
> This tool is intended for educational purposes only. Use it responsibly and comply with your institution's policies. 🚨

# 🛠️ Hemis System Bypass  

This script allows you to get answers to tests even during exams! Just open your console and run some code. 🧑‍💻

---

## 🚀 Features
- Parse `.docx` files containing test questions and answers.
- Upload parsed questions to a running server for easy access.
- Retrieve answers during exams by using the provided code snippets.

---

## 📖 How to Use

### 1️⃣ Clone the Repository
First, clone the repository and navigate to the project folder:
```bash
git clone https://github.com/HoPHNiDev/Hemis.git
cd Hemis
```
### 2️⃣ Installation
**🐧 Linux**
```
sudo sh install.sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 main.py
```
🪟 Windows
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
### 3️⃣ Upload Questions to the Server <a name = "parse"></a>
1. Run the test parser:
```
python parse.py
```
2. Provide the file path:

Paste the absolute path to your .docx file with test questions:
```
/Users/HoPHNiDev/Downloads/english.docx
```
3. Enter the subject name:

For example:
```
English
```
4. Input the server URL:

Use the public server or your own:
```
https://hemisstudent.pythonanywhere.com/questions/
```
## 🌐 Access the Server
Visit the [Hemis Student Page](https://hemisstudent.pythonanywhere.com/) to:
- Get guidance on how to use the server during exams.
- Obtain the code you need to fetch answers directly from the console.

## 🛠️ Configure Your Own Server
You can use your own server instead of the public one. Free hosting services like [PythonAnywhere](https://pythonanywhere.com/) are supported.

Follow this [official guide](https://help.pythonanywhere.com/pages/Flask/) to configure a Flask server.

After setup:

- Upload your questions using the same steps mentioned above.
- Replace the public server URL with your server URL during the [Upload Questions](#parse) step.


## ✍️ Authors <a name = "authors"></a>

- [@HoPHNiDev](https://github.com/HoPHNiDev) - Idea & Initial work
