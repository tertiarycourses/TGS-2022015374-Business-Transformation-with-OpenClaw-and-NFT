from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

db = {}

def invoice_hash(data):
    text = f"{data['invoice_id']}{data['vendor']}{data['amount']}{data['date']}"
    return hashlib.sha256(text.encode()).hexdigest()

@app.route('/store', methods=['POST'])
def store():
    data = request.json
    db[data['invoice_id']] = invoice_hash(data)
    return jsonify({"status": "stored"})

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    current_hash = invoice_hash(data)

    stored_hash = db.get(data['invoice_id'])

    verified = stored_hash == current_hash

    return jsonify({
        "invoice_id": data['invoice_id'],
        "verified": verified,
        "tampered": not verified
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
