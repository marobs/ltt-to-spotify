from flask import Flask
import controllers
import helpers
import argparse
import os

if not os.path.exists('log'):
    os.makedirs('log')

if not os.path.exists('cache'):
    os.makedirs('cache')

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

# Register the controllers
app.register_blueprint(controllers.main)
app.register_blueprint(controllers.listentothis)
app.register_blueprint(controllers.playlist)
app.secret_key = helpers.getFlaskSecret()

# Get and set flags
parser = argparse.ArgumentParser(description="Start up a ltt-to-spotify server.")
parser.add_argument('-nc', '--nocache', action='store_true', help="Enable to not cache or used cache data")

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host='0.0.0.0', port=3000, debug=True, use_reloader=False)