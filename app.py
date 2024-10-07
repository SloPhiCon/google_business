import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def say_hi():
    return 'Hi!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT from environment variables
    app.run(host='0.0.0.0', port=port)
