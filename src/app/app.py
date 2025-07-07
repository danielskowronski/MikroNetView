import os
from flask import Flask, render_template
from LeaseFetch import dumbFetchLeases
from config import AppConfig,AppConfigMikrotik,AppConfigServer,load_config

app = Flask(__name__)

_config = load_config(os.environ.get("MNV_CONF", "/app/config/config.yaml"))

# Route for dynamic page
@app.route("/")
def index():
    leases = dumbFetchLeases(_config.mikrotik.host, _config.mikrotik.user, _config.mikrotik.password.get_secret_value())
    return render_template("index.html", leases=leases)

if __name__ == "__main__":
    app.run(host=_config.server.host, port=_config.server.port, debug=_config.server.debug)
