def decode_utf8(any_var) -> any:
    """Декодирование любой стандартной структуры"""
    par_type = type(any_var)
    if par_type in [bytearray, bytes]:
        any_var = any_var.decode("utf-8")
    elif par_type is dict:
        any_var = {k: decode_utf8(v) for k, v in any_var.items()}
    elif par_type is list:
        any_var = [decode_utf8(x) for x in any_var]
    elif par_type in (str, int, float) or any_var is None:
        pass  # Действия не требуются
    else:
        print(f"undef structure: {par_type}")

    return any_var
