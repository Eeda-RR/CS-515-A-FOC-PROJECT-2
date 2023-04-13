from utils import parse_program,evaluate_program

def calculate(statements):
    """
    >>> statements = ["x = 3", " y = 5", "z = 2 + x * y ", " z2 = (2 + x) * y", "print x, y, z, z2"]
    >>> calculate(statements)
    3.0 5.0 17.0 25.0

    >>> statements = ["pi = 3.14159", " r = 2", " area = pi * r^2","print area "]
    >>> calculate(statements)
    12.56636

    >>> statements = ["print 5 - 1 - 1 -1"]
    >>> calculate(statements)
    2.0

    >>> statements = ["print ((5 - 1) - 1) -1"]
    >>> calculate(statements)
    2.0

    >>> statements = ["print 2 ^ 2 ^ 2"]
    >>> calculate(statements)
    16.0

    >>> statements = ["1 / 0"]
    >>> calculate(statements)
    divide by zero

    >>> statements = ["print 0 / 1 , 1 / 0"]
    >>> calculate(statements)
    0.0 divide by zero

    >>> statements = ["print 0 / 1 , 0 / 0"]
    >>> calculate(statements)
    0.0 divide by zero

    >>> statements = ["(5 + 3)/ (2 - 2)"]
    >>> calculate(statements)
    divide by zero

    >>> statements = ["x = 5",  "y = -x++","print x, y"]
    >>> calculate(statements)
    6.0 -5.0

    >>> statements = ["x = 10", "y = ++x * -2","print x, y"]
    >>> calculate(statements)
    11.0 -22.0

    >>> statements = ["x = 5", "y = 10 / x * 2","print x, y"]
    >>> calculate(statements)
    5.0 4.0

    >>> statements = ["x = 5 ", "y = 10 * x / 2 % 3","print x, y"]
    >>> calculate(statements)
    5.0 1.0

    >>> statements = ["x = 5 ", "y = 10 + x++ - --x","print x, y"]
    >>> calculate(statements)
    5.0 10.0

    >>> statements = ["x = 5 ", "y = ++x + x-- - --x","print x, y"]
    >>> calculate(statements)
    4.0 8.0

    >>> statements = ["x = 1 ","print -(-(x)), y"]
    >>> calculate(statements)
    1.0 0.0

    >>> statements = ["print x, -y"]
    >>> calculate(statements)
    0.0 0.0

    >>> statements = ["x = 1 ", " ", " ","print x, y"]
    >>> calculate(statements)
    1.0 0.0

    >>> statements = [" x = 0 " , " y = 5" , "print  x+++y, x, y"]
    >>> calculate(statements)
    5.0 1.0 5.0

    >>> statements = ["print  x++, 1/0, x"]
    >>> calculate(statements)
    0.0 divide by zero 1.0


    """
    parsed_statements = parse_program(statements)
    evaluate_program(parsed_statements)
    return

if __name__ == "__main__":
    import doctest
    doctest.testmod()
