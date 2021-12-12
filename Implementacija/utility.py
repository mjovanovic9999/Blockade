def str_to_coordinate(val:chr)->int:
    if val.strip().isdigit():
        return int(val)
    return ord(val)-55