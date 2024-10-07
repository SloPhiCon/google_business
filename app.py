from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def say_hi():
    return 'Hi! This is the addition service.'

@app.route('/saml/login', methods=['GET'])
def saml_login():
    logging.info('saml_login function processed a request.')
    req_data = prepare_request()
    auth = init_saml_auth(req_data)
    return redirect(auth.login())

@app.route('/saml/callback', methods=['POST'])
def saml_callback():
    logging.info('saml_callback function processed a request.')
    req_data = prepare_request()
    auth = init_saml_auth(req_data)
    auth.process_response()
    errors = auth.get_errors()

    if not errors:
        user_data = auth.get_attributes()
        name_ = user_data.get('http://schemas.microsoft.com/identity/claims/displayname', ['User'])[0]
        return jsonify({"message": f"{name_} User authenticated!"})
    else:
        return jsonify({"error": "Error in SAML Authentication", "details": errors}), 500

@app.route('/add', methods=['POST'])
def add_numbers():
    # Get JSON data from the request
    data = request.get_json()
    
    # Extract numbers from the JSON data
    num1 = data.get('num1')
    num2 = data.get('num2')
    
    # Check if both numbers are provided and are valid
    if num1 is None or num2 is None:
        return jsonify({'error': 'Please provide both num1 and num2'}), 400
    if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
        return jsonify({'error': 'Both num1 and num2 must be numbers'}), 400

    # Perform addition
    result = num1 + num2

    # Return the result as JSON
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
