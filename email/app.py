from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai
from flask_cors import CORS

#python app.py
app = Flask(__name__)
CORS(app)

genai.configure(api_key="")
model = genai.GenerativeModel("gemini-pro")

# Home page with a button
@app.route('/')
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Email Generator</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 50px;
                }
                button {
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    border-radius: 5px;
                }
                button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to the Email Generator API</h1>
            <p>Click the button below to generate an email.</p>
            <button onclick="window.location.href='/email-generator'">Go to Email Generator</button>

        </body>
        </html>
    ''')

@app.route('/hello/<name>')
def hello(name):
    return 'Hello  ' + name
# Email generator page
@app.route('/email-generator')
def email_generator_page():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Email Generator</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 50px;
                }
                form {
                    max-width: 600px;
                    margin: 0 auto;
                }
                label {
                    display: block;
                    margin-bottom: 8px;
                    font-weight: bold;
                }
                input, select, textarea {
                    width: 100%;
                    padding: 10px;
                    margin-bottom: 20px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                button {
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                    background-color: #28a745;
                    color: white;
                    border: none;
                    border-radius: 5px;
                }
                button:hover {
                    background-color: #218838;
                }
            </style>
        </head>
        <body>
            <h1>Email Generator</h1>
            <form id="email-form">
                <label for="src">From</label>
                <input type="text" id="src" name="src" placeholder="Sender's name" required>
                
                <label for="des">To</label>
                <input type="text" id="des" name="des" placeholder="Recipient's name" required>
                
                <label for="subject">Subject</label>
                <input type="text" id="subject" name="subject" placeholder="Subject" required>
                
                <label for="tone">Tone</label>
                <select id="tone" name="tone" required>
                    <option value="Formal">Formal</option>
                    <option value="Informal">Informal</option>
                    <option value="Professional">Professional</option>
                </select>
                
                <label for="about">About</label>
                <textarea id="about" name="about" placeholder="What is the email about?" required></textarea>
                
                <button type="submit">Generate Email</button>
            </form>
            <p id="result"></p>
            <script>
                document.getElementById("email-form").addEventListener("submit", async function (event) {
                    event.preventDefault();
                    
                    const src = document.getElementById("src").value;
                    const des = document.getElementById("des").value;
                    const subject = document.getElementById("subject").value;
                    const tone = document.getElementById("tone").value;
                    const about = document.getElementById("about").value;

                    const response = await fetch("http://127.0.0.1:5000/generate-email", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ src, des, subject, tone, about })
                    });

                    const result = await response.json();

                    if (response.ok) {
                        document.getElementById("result").innerText = "Generated Email: " + result.email;
                    } else {
                        document.getElementById("result").innerText = "Error: " + (result.error || "Failed to generate email.");
                    }
                });
            </script>
        </body>
        </html>
    ''')

# API for generating email
@app.route('/generate-email', methods=['POST'])
def generate_email():
    print(f"Request method: {request.method}")
    data = request.json
    src = data.get("src")
    des = data.get("des")
    subject = data.get("subject")
    tone = data.get("tone")
    about = data.get("about")
    
    if not all([src, des, subject, tone, about]):
        return jsonify({"error": "All fields are required"}), 400
    
    prompt = f"write an email from {src} to {des} with the subject {subject} and the tone {tone} about {about}"
    response = model.generate_content(prompt)
    return jsonify({"email": response.text})

if __name__ == "__main__":
    app.run(port=5000)
