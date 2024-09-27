from flask import *

app = Flask(__name__)

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


@app.route("/")
def index():
    return render_template('chat.html', version=identity.__version__)


@app.route("/chat")
def openChat():
    return render_template("chat.html", version=identity.__version__)


if __name__ == "__main__":
    app.run()