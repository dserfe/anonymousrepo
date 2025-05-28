def f(text, insert):
    whitespaces = {'\t', '\r', '\x0b', ' ', '\x0c', '\n'}
    clean = ''
    for char in text:
        if char in whitespaces:
            clean += insert
        else:
            clean += char
    return clean