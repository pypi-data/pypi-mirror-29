# Stepping in multi-line statements is broken.
x = 1; y = 2; z = 3; q = 10
def five(): return 5
x = five()+1; y= five() + 2; a = 4
z = x + y + a
