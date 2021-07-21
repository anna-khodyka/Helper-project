def error_handler(func):
    def inner(*args):
        try:
            return func(*args)
        except:
            print(
                'Wrong input! Type exact command you want to do,"exit" to exit or "help" for list of commands.')
    return inner
