
"""
import hashlib

def hash256(s):
    #two round of SHA256
    return hashlib.sha256(hashlib.sha256(s).digest).digest
"""
# Your last file
import hashlib

def hash256(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()
