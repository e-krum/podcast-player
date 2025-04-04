def validate_boolean(msg):
    while True:
        value = input(msg)
        if value.lower() == 'true': return True
        elif value.lower() == 'false': return False
        else: print('Incorrect value entered')

def validate_float(msg, lower, upper):
    while True:
        value = input(msg)
        try:
            fval = float(value)
            if fval <= upper and fval >= lower: return fval
            else: print('Input outside of indicated range')
        except: print('Incorrect input. Enter a number between within indicated range, {lower}-{upper}'.format(lower=lower, upper=upper))

def validate_int(msg, lower, upper):
    while True:
        value = input(msg)
        try:
            ival = int(value)
            if ival <= upper and ival >= lower: return ival
        except: print('Incorrect option selected. Please enter a number between {lower} and {upper}'.format(lower=lower, upper=upper))