def digest(hasher, data):
    hasher.update(data)
    return hasher.digest()


def hexdigest(hasher, data):
    hasher.update(data)
    return hasher.hexdigest()


STRING_TESTS = [
    b'Hello World!',
    # 한국어
    b'\xed\x95\x9c\xea\xb5\xad\xec\x96\xb4',
    # räksmörgås
    b'r\xc3\xa4ksm\xc3\xb6rg\xc3\xa5s',
    # même
    b'm\xc3\xaame',
]
