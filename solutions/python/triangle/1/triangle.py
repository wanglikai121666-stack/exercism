def equilateral(sides):
    a,b,c=sides
    return (
        a ==b and
        b ==c and
        a ==c and
        a > 0 and
        b > 0 and
        c > 0 and
        a + b >= c and
        b + c >= a and
        a + c >= b
    )


def isosceles(sides):
    a,b,c=sides
    return (
        (a ==b or
        b ==c or
        a ==c )and
        a > 0 and
        b > 0 and
        c > 0 and
        a + b >= c and
        b + c >= a and
        a + c >= b
    )


def scalene(sides):
    a,b,c=sides
    return (
        a !=b and
        b !=c and
        a !=c and
        a > 0 and
        b > 0 and
        c > 0 and
        a + b >= c and
        b + c >= a and
        a + c >= b
    )
