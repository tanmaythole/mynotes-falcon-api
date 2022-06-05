import bcrypt

def hash_password(password):
    """
    Genrate hash of password using bcrypt
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    """
    Verify the password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))