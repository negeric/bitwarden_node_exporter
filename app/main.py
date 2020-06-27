from flask import Flask, make_response
from helpers import get_counts
import os
app = Flask(__name__)

app_port = os.getenv('PORT', 8090)

@app.route('/metrics')
def prom_exporter():
    response = make_response(get_counts(), 200)
    response.mimetype = "text/plain"
    return response

@app.route('/health')
def health_check():
    response = make_response("OK", 200)
    response.mimetype = "text/plain"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app_port)
    