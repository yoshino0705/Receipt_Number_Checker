def numerical(character):
    try:
        int(character)
        return True
    except ValueError:
        return False
        
def filter_inputs(text):
    return ''.join([t for t in text if numerical(t)])
