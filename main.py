from flask import Flask, send_from_directory
from api_routes import init as api_routes_init
import webview

app = Flask(__name__)
api_routes_init(app)
# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('frontend/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('frontend/public', path)


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5005) # for developing

    # production
    # window = webview.create_window('Next Linux', app)
    # webview.start(debug=True)