import os
from flask import Flask, render_template
from LeaseFetch import dumbFetchLeases

app = Flask(__name__)
MNV_HOST = os.environ["MNV_HOST"]
MNV_USER = os.environ["MNV_USER"]
MNV_PASS = os.environ["MNV_PASS"]

# Route for dynamic page
@app.route("/")
def index():
    leases = dumbFetchLeases(MNV_HOST, MNV_USER, MNV_PASS)
    return render_template("index.html", leases=leases)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001, debug=True)
