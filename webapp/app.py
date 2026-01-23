from flask import Flask, render_template, jsonify, request
import hardware

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/status", methods=["GET"])
def api_status():
    return jsonify(hardware.get_status())

@app.route("/api/action", methods=["POST"])
def api_action():
    data = request.get_json(silent=True) or {}
    device = data.get("device")
    action = data.get("action")

    if not device or not action:
        return jsonify({"ok": False, "error": "Missing device/action"}), 400
        
    ok, msg = hardware.perform_action(device, action)
    return jsonify({"ok": ok, "message": msg, "status": hardware.get_status()}), (200 if ok else 400)


if __name__ == "__main__":
    hardware.init()
    app.run(host="0.0.0.0", port=5050, debug=False)
