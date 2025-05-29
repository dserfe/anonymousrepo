def f(text, width):
    result = ''
    lines = text.split('\n')
    for l in lines:
        result += l.center(width)
        result += '\n'
    result = result[:-1]
    return result