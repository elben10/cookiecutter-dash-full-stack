def get_error_message(errors, key):
    for elem in errors:
        if key in elem["loc"]:
            return elem["msg"].capitalize()