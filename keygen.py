"""Simple random key generation.

See:
http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python/23728630#23728630
"""

import random
import string

def gen_key(size = 32):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

# Example: just pass the desired length
print gen_key(256)
