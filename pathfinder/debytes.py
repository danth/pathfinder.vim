def debytes(string):
    """
    Decode string if it is a bytes object.

    This is necessary since Neovim, correctly, gives strings as a str, but regular
    Vim leaves them encoded as bytes.
    """
    try:
        return string.decode()
    except AttributeError:
        return string
