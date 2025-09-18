import os, time
from flask import Flask, render_template
from LeaseFetch import dumbFetchLeases
from config import AppConfig, AppConfigMikrotik, AppConfigServer, load_config

app = Flask(__name__, static_folder="static", template_folder="templates")

_config = load_config(os.environ.get("MNV_CONF", "/app/config/config.yaml"))


# Route for dynamic page
@app.route("/")
def index():
    try:
        leases = dumbFetchLeases(
            _config.mikrotik.host,
            _config.mikrotik.user,
            _config.mikrotik.password.get_secret_value(),
        )
    except Exception as e:
        print(f"Error fetching leases: {e}")
        leases = []

    start_time = time.time()
    html = render_template("index.html", leases=leases)
    end_time = time.time()
    print(f"Rendered template in {end_time - start_time:.3f} seconds")
    return html


if __name__ == "__main__":
    app.run(
        host=_config.server.host, port=_config.server.port, debug=_config.server.debug
    )
