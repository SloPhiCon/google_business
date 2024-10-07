from flask import Flask, request, jsonify

app = Flask(_name_)

@app.route('/')
def say_hi():
    return 'Hi! This is the addition service.'

app.secret_key = os.urandom(24)  # Replace this with a secure key in production

# Configuration for SAML
SAML_PATH = os.path.join(os.getcwd(), 'saml')


def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=SAML_PATH)
    return auth

def prepare_flask_request(request):
    url_data = request.url.split('?')
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'script_name': request.path,
        'server_port': request.host.split(':')[1] if ':' in request.host else '80',
        'get_data': request.args.copy(),
        'post_data': request.form.copy(),
    }


@app.route('/saml/login')
def login():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    return redirect(auth.login())

'''
@app.route('/saml/logout')
def logout():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    name_id = session['samlNameId'] if 'samlNameId' in session else None
    session.clear()
    return redirect(auth.logout(name_id=name_id))
'''

@app.route('/saml/callback', methods=['POST'])
def login_callback():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    auth.process_response()
    errors = auth.get_errors()

    if not errors:
        session['samlUserdata'] = auth.get_attributes()
        session['samlNameId'] = auth.get_nameid()
        name_ = session['samlUserdata']['http://schemas.microsoft.com/identity/claims/displayname']
        #return redirect(url_for('index'))
        return f"{name_} User authenticated!"
    else:
        return f"Error in SAML Authentication: {errors}", 500
[15:38, 07/10/2024] Sachin Bhusnurmath: from f

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

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)
