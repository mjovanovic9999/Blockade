def str_to_coordinate(val: chr) -> int:
    if val.strip().isdigit():
        return int(val)
    return ord(val)-55


def int_to_table_coordinate(int: int) -> str:
    coordinates = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return coordinates[int % len(coordinates)]
