def check_divide_by_zero(message="Cannot divided by zero"):
    def decorate(main_func):
        def validate(a, b):
            if b ==0:
                raise ValueError(message)
            print(f"Validated {a} can divied by {b}")
            main_func(a, b)
        return validate
    return decorate


@check_divide_by_zero()
def divide(divided: int, divisor: int):
    return divided / divisor

divide(11,0)

