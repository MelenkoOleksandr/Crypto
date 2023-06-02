import random
import hashlib


def generate_keys(p, q):
    # Choose a random private key s
    s = random.randint(1, q - 1)

    # Calculate the public key v
    gamma = find_gamma(p, q)
    v = pow(gamma, s, p)

    return s, v


def find_gamma(p, q):
    # Find an integer gamma such that gamma*q = 1 (mod p)
    for gamma in range(2, p):
        if pow(gamma, q, p) == 1:
            return gamma
    raise ValueError("Unable to find gamma")


def sign_message(p, q, s, message):
    gamma = find_gamma(p, q)

    # To choose random integer r: r = random.randint(1, q - 1)
    r = 6

    # Compute x = gamma^r (mod p)
    x = pow(gamma, r, p)

    # Attach the message M with x and compute the hash value e
    concatenated = str(message) + str(x)
    e = int(hashlib.sha256(concatenated.encode()).hexdigest(), 16)

    # Compute y = (r + s*e) (mod q)
    y = (r + s * e) % q

    return y, e


def verify_signature(p, q, v, message, y, e):
    gamma = find_gamma(p, q)

    # Compute x' = (gamma^y * v^e) (mod p)
    x_prime = pow(gamma, y, p) * pow(v, e, p) % p

    # Compute the hash value H(M || x')
    concatenated = str(message) + str(x_prime)
    hashed_value = int(hashlib.sha256(concatenated.encode()).hexdigest(), 16)

    return hashed_value == e


# Example usage
p = 29  # Prime number
q = 7   # Prime factor of p-1

# Sender's side
# For random keys: sender_private_key, sender_public_key = generate_keys(p, q)
sender_private_key = 5
sender_public_key = 16
message = "Hello, world!"
signature = sign_message(p, q, sender_private_key, message)
print("Signature:", signature)

# Receiver's side
valid_signature = verify_signature(
    p, q, sender_public_key, message, *signature)

print("Valid Signature:", valid_signature)
