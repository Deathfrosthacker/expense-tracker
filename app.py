from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import SECRET_KEY
from routes import bp

app = Flask(__name__)

@app.template_filter("currency")
def currency(value):
    try:
        return f"{float(value):.2f}"
    except (ValueError, TypeError):
        return "0.00"

# Config
app.config["SECRET_KEY"] = SECRET_KEY

# Security
csrf = CSRFProtect(app)
limiter = Limiter(app=app, key_func=get_remote_address)

# Register routes
app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(debug=True)