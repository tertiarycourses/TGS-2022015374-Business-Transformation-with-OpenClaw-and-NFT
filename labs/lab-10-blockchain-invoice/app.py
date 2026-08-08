from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# Simple in-memory storage
db = {}

def invoice_hash(data):
    text = f"{data['invoice_id']}{data['vendor']}{data['amount']}{data['date']}"
    return hashlib.sha256(text.encode()).hexdigest()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "invoice-verifier"
    })

@app.route('/store', methods=['POST'])
def store():
    data = request.get_json()

    required_fields = ["invoice_id", "vendor", "amount", "date"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    db[data["invoice_id"]] = invoice_hash(data)

    return jsonify({
        "status": "stored",
        "invoice_id": data["invoice_id"]
    })

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()

    required_fields = ["invoice_id", "vendor", "amount", "date"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    stored_hash = db.get(data["invoice_id"])

    if not stored_hash:
        return jsonify({
            "invoice_id": data["invoice_id"],
            "verified": False,
            "tampered": True,
            "message": "Invoice not found"
        }), 404

    current_hash = invoice_hash(data)

    verified = stored_hash == current_hash

    return jsonify({
        "invoice_id": data["invoice_id"],
        "verified": verified,
        "tampered": not verified
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
