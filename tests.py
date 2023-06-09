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
    0.0 -0.0

    >>> statements = ["x = 1 ", " ", " ","print x, y"]
    >>> calculate(statements)
    1.0 0.0

    >>> statements = [" x = 0 " , " y = 5" , "print  x+++y, x, y"]
    >>> calculate(statements)
    5.0 1.0 5.0

    >>> statements = ["print++","print print"]
    >>> calculate(statements)
    1.0

    >>> statements = ["x = 5"," x += ++x", "print x"]
    >>> calculate(statements)
    11.0

    >>> statements = ["x = y = z = 1","print x, y, z"]
    >>> calculate(statements)
    1.0 1.0 1.0

    >>> statements = ["x = 1" ,"y = 5", "y -= x--","print x, y"]
    >>> calculate(statements)
    0.0 4.0

    >>> statements = ["x = 1", " /* ", " x = 2 ", " y = 3 ",  " */ ", " y = 4 ", "# print 0", "print x, y"]
    >>> calculate(statements)
    1.0 4.0

    >>> statements = ["x = 1", " /*  x = 2 ", " y = 3  */ ", " y = 4 ", "# print 0", "print x, y"]
    >>> calculate(statements)
    1.0 4.0

    >>> statements = ["print 1 && 2, 2 && 1, -5 && 1, 0 && -100"]
    >>> calculate(statements)
    1 1 1 0

    >>> statements = ["x = 1", "y = 2", "z = 0", "print x && y, x || z, x && z"]
    >>> calculate(statements)
    1 1 0

    >>> statements = ["x = 1", "y = 2", "z = 0", "print x ||=y, x, x&&=z, x"]
    >>> calculate(statements)
    1 1 0 0

    >>> statements = ["x = 1", "print !1, !x"]
    >>> calculate(statements)
    0 0

    >>> statements = ["x = 1", "y = 2", "print x>=1, x>=0, x <= y, x <= y - 1, x>= y * 2"]
    >>> calculate(statements)
    1 1 1 1 0

    >>> statements = ["print 5 > 3, 1 < 2, 3>=3, 2 <=2, 1 != 1"]
    >>> calculate(statements)
    1 1 1 1 0

    >>> statements = ["x = 1", "y = 2", "print x == 1, 100 == 0, x >= 1, 5 <= y"]
    >>> calculate(statements)
    1 0 1 0

    >>> statements = ["print  x++, 1/0, x"]
    >>> calculate(statements)
    0.0 divide by zero

    >>> statements = ["1 / 0"]
    >>> calculate(statements)
    divide by zero

    >>> statements = ["print 0 / 1 , 1 / 0"]
    >>> calculate(statements)
    0.0 divide by zero

    >>> statements = ["print 0 / 1 , 0 / 0", "print 2"]
    >>> calculate(statements)
    0.0 divide by zero

    >>> statements = ["(5 + 3)/ (2 - 2)"]
    >>> calculate(statements)
    divide by zero

    # >>> statements = ["print 3", "print (2 + 3)+((4+5 + ()))"]
    # >>> calculate(statements)
    # parse error





    """
    parsed_statements = parse_program(statements)
    evaluate_program(parsed_statements)
    return

if __name__ == "__main__":
    import doctest
    doctest.testmod()