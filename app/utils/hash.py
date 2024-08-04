import hashlib

def deterministic_hash(input_string: str) -> str:
    input_bytes = input_string.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(input_bytes)
    hex_dig = hash_object.hexdigest()
    return hex_dig