def check(value, limit):
    if type(value) not in (int, float):
        return "TYPE"
    if not 0 <= value <= limit:
        return "RANGE"
    return "OK"
