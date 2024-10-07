from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Azure! Your Flask app is deployed successfully."

if __name__ == '__main__':
    app.run(debug=True)



