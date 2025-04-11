def validate_boolean(msg):
    while True:
        value = input(msg)
        print()
        if value.lower().strip() in ('true', 't', 'yes', 'y'): return True
        elif value.lower().strip() in ('false', 'f', 'no', 'n'): return False
        else: print('Invalid value entered')

def validate_float(msg, lower, upper):
    while True:
        value = input(msg)
        print()
        try:
            fval = float(value.strip())
            if fval <= upper and fval >= lower: return fval
            else: print('Input outside of indicated range')
        except: print('Incorrect input. Enter a number between within indicated range, {lower}-{upper}'.format(lower=lower, upper=upper))

def validate_int(msg, lower, upper):
    while True:
        value = input(msg)
        print()
        try:
            ival = int(value.strip())
            if ival <= upper and ival >= lower: return ival
            else: print('Input outside of indicated range')
        except: print('Incorrect option selected. Please enter a number between {lower} and {upper}'.format(lower=lower, upper=upper))