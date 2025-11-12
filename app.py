from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# In-memory tasks list (for demo)
tasks = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.get_json()
    task = data.get("task")
    if task:
        tasks.append(task)
        return jsonify({"success": True, "tasks": tasks})
    return jsonify({"success": False, "error": "No task provided"}), 400

@app.route("/get_tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks})

@app.route("/analyze", methods=["POST"])
def analyze():
    if not tasks:
        return jsonify({"reply": "You have no tasks yet."})
    try:
        # Create prompt for Gemini
        prompt = f"Here are my tasks: {tasks}. As a helpful productivity assistant, suggest priorities and a short plan. Keep the response concise and practical."
        
        # Generate content using Gemini
        response = model.generate_content(prompt)
        
        # Extract the reply content
        reply = response.text
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)