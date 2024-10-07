import identity.web
import requests
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session

import app_config

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

auth = identity.web.Auth(
    session=session,
    authority=app.config.get("AUTHORITY"),
    client_id=app.config["CLIENT_ID"],
    client_credential=app.config["CLIENT_SECRET"],
)

# Mock function to check if the user is admin
def is_admin(user):
    # You would extract the group/role from the token and check if it's 'admin'
    return user.get('roles', []) == ['admin']

@app.route("/login")
def login():
    return render_template("login.html", version=identity.__version__, **auth.log_in(
        scopes=app_config.SCOPE,
        redirect_uri=url_for("auth_response", _external=True),
    ))

@app.route(app_config.REDIRECT_PATH)
def auth_response():
    result = auth.complete_log_in(request.args)
    if "error" in result:
        return "Authentication error: " + result.get("error_description", "Unknown error")
    return redirect(url_for("welcome"))

@app.route("/logout")
def logout():
    return redirect(auth.log_out(url_for("index", _external=True)))

@app.route("/")
def index():
    if not (app.config["CLIENT_ID"] and app.config["CLIENT_SECRET"]):
        return render_template('config_error.html')
    if not auth.get_user():
        return redirect(url_for("login"))
    return render_template('index.html', user=auth.get_user(), version=identity.__version__)

@app.route("/welcome")
def welcome():
    user = auth.get_user()
    if not user:
        return redirect(url_for("login"))
    return render_template('welcome.html', user=user, is_admin=is_admin(user))

@app.route("/translate_text")
def translate_text():
    user = auth.get_user()
    if not user:
        return redirect(url_for("login"))
    return render_template('translate_text.html', user=user)

@app.route("/translate_document")
def translate_document():
    user = auth.get_user()
    if not user:
        return redirect(url_for("login"))
    return render_template('translate_document.html', user=user)

@app.route("/settings")
def settings():
    user = auth.get_user()
    if not user:
        return redirect(url_for("login"))
    if not is_admin(user):
        return "Access denied: You are not authorized to view this page.", 403
    return render_template('settings.html', user=user)

if __name__ == "__main__":
    app.run()
