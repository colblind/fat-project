def can_cast(source, dest_type):
    try:
        dest_type(source)
        return True
    except ValueError:
        return False
