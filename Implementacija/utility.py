def read_int_from_range_and_prefered(what_to_read: str, low: int, high: int, prefered: int) -> int:
    if low == high:
        return low  # da l tako??
    if low > high:
        pom = low
        low = high
        high = pom
    if prefered < low or prefered > high:
        return False
    while True:
        pom = input(what_to_read+"["+str(prefered)+"]: ")
        if pom == "" or pom == " ":
            pom = prefered
            break
        if pom.strip().isdigit():
            pom = int(pom)
            if pom >= low and pom <= high:
                break
            print("You must enter number between "+str(low)+" and "+str(high))
        else:
            print("You must enter whole number")
    return pom


def read_yes_no_prefered(question: str, prefered_yes: bool) -> bool:
    allowed_answers = ["Y", "YES", "YE", " ", "", "NO", "N"]
    val = None
    while val not in allowed_answers:
        val = input(question+"[YES/no]: " if prefered_yes else "[yes/NO]: ")
        val = str.upper(val)
    return True if val in allowed_answers[:5] else False


def read_pawn_position(what_player: str, table_columns: int, table_rows: int, prefered_column: int, prefered_row: int, busy_positions) -> tuple[int, int]:
    column = read_int_from_range_and_prefered(
        what_player+" start column", 0, table_columns, prefered_column if table_columns > prefered_column else table_columns)
    row = read_int_from_range_and_prefered(
        what_player+" start row", 0, table_rows, prefered_row if table_rows > prefered_row else table_rows)
    print(busy_positions)
    return (column, row) if (column, row) not in busy_positions else print("Enter again") or read_pawn_position(what_player, table_columns, table_rows, prefered_column, prefered_row, busy_positions)
