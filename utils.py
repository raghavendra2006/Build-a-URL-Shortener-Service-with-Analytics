# utils.py
import string

# Define the character set: 0-9, a-z, A-Z (62 chars)
BASE62 = string.digits + string.ascii_lowercase + string.ascii_uppercase

def encode_base62(num: int) -> str:
    """Encodes a database integer ID into a short string."""
    if num == 0:
        return BASE62[0]
    
    arr = []
    base = len(BASE62)
    while num:
        num, rem = divmod(num, base)
        arr.append(BASE62[rem])
    arr.reverse()
    return ''.join(arr)