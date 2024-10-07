from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Azure! Your Flask app is deployed successfully."

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    result = data['a'] + data['b']
    return jsonify(result=result)

@app.route('/multiply', methods=['POST'])
def multiply():
    data = request.get_json()
    result = data['a'] * data['b']
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
