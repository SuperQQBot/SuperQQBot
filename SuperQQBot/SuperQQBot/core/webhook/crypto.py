from cryptography.hazmat.primitives.asymmetric import ed25519

def generate_signature(data, secret_key):
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key)
    signature = private_key.sign(data)
    return signature
