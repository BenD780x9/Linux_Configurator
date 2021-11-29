from flask import Flask, send_from_directory
from api_routes import init as api_routes_init
import webview
import threading
from flask import request


def shutdown_flask():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

app = Flask(__name__)
app.config['port'] = 5005
api_routes_init(app)
# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('frontend/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('frontend/public', path)


def webapp():
    app.run(debug=False, host='localhost', port=5005) # for developing

if __name__ == "__main__":
    

    threading.Thread(target=webapp).start()
    # production
    window = webview.create_window('Next Linux', 'http://localhost:5005')
    # window = webview.create_window('Next Linux', app)
    window.closed += shutdown_flask
    webview.start(debug=False)