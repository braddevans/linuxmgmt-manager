def time_string_to_seconds(time_string):
    str_tim = time_string.lower()
    if str_tim.endswith("s"):
        return int(str_tim[:-1])
    elif str_tim.endswith("m"):
        return int(str_tim[:-1]) * 60
    elif str_tim.endswith("h"):
        return int(str_tim[:-1]) * 60 * 60
    elif str_tim.endswith("d"):
        return int(str_tim[:-1]) * 60 * 60 * 24
    elif str_tim.endswith("w"):
        return int(str_tim[:-1]) * 60 * 60 * 24 * 7
    else:
        return int(str_tim)