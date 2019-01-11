"""This module was designed to accompany the paper at [ADDRESS HERE].

The object of this module is to receive a list of possible fixed points of a
monotonic vector field (Any iterable will do; order in the list is x-order, first
coordinate is the order of the given fixed point; second coordinate is type), then
return whether or not that list of fixed point is realizable.

It also contains functions to generate all possible lists of a given size.
Don't use with n > 10; the quantity of valid grids seems to grow exponentially.

One thing to note: this module broadly uses two types of objects: lists 
(c.f. definition 3.1) and grids (c.f. definition 3.2).

The first is stored as a list of tuples; the second, as a 2D numpy array.
When using the functions, check whether it takes lists or grids as arguments."""

import numpy


def l_to_grid(l):
    """Numbers stored from bottom to top as y, and left to right as x"""
    n = len(l)
    g = numpy.arange(0, n**2).reshape(n, n)
    for i in numpy.arange(n):
        x = l[i]
        g[n - x[0]][i] = 0 - x[1]
        for o in range(n+1-x[0], n): #Below
            g[o][i] = g[o][i] + 1
        for o in range(n-x[0]): #Above
            g[o][i] = g[o][i] + 2
        for u in range(i+1, n): #Right
            g[n - x[0]][u] += 8
        for u in range(i): #Left
            g[n - x[0]][u] += 4
    for i in range(n):
        for j in range(n):
            p = n*i + j
            if g[i][j] <= 0: #We have a hole
                continue
            elif g[i][j] - p == 5: #To the left and below
                g[i][j] = 3
            elif g[i][j] - p == 6: #To the left and above
                g[i][j] = 4
            elif g[i][j] - p == 9: #To the right and below
                g[i][j] = 2
            elif g[i][j] - p == 10: #To the right and above
                g[i][j] = 1
            else:
                print "error"
    return g

def grid_to_l(g):
    """Go from grid to list notation."""
    n = g.shape[1]
    l = []
    for i in range(n):
        for j in range(1, n+1):
            if g[i][n - j] < 0:
                l.append((j, 0-g[i][n-j]))
                break
    return l

def is_valid(g):
    """Verifies that the grid g does not contain forbidden cells."""
    n = g.shape[0]
    e = True
    i = 0
    j = 0
    while e and (i < n -1):
        j = 0
        while e and (j < n -1):
            #All simple cases
            if g[i+1][j] == 1 and g[i][j + 1] == 3:
                e = False
                break
            if g[i][j] == 2 and g[i+1][j + 1] == 4:
                e = False
                break
            if g[i+ 1][j] == 2 and g[i + 1][j + 1] == 1 and g[i][j + 1] == 4 and g[i][j] == 3:
                e = False
                break
            if g[i+ 1][j] == 4 and g[i + 1][j + 1] == 3 and g[i][j + 1] == 2 and g[i][j] == 1:
                e = False
                break
            #All 1-point cases
            if ((g[i+1][j] == -1 or g[i+1][j] == -3) and g[i][j+1] == 3) or ((g[i][j + 1] == -1 or g[i][j+1] == -3) and g[i+1][j] == 1):
                e = False
                break
            if ((g[i][j] == -2 or g[i][j] == -3) and g[i+1][j+1] == 4) or ((g[i+1][j + 1] == -2 or g[i+1][j+1] == -3) and g[i][j] == 2):
                e = False
                break
            if ((g[i + 1][j + 1] == -1 and g[i][j] > 0 and g[i][j] != 2) or (g[i][j] == -1 and g[i+1][j+1] > 0 and g[i + 1][j + 1] != 4)):
                e = False
                break
            if ((g[i+1][j] == -2 and g[i][j + 1] > 0 and g[i][j + 1] != 3) or (g[i][j + 1] == -2 and g[i + 1][j] > 0 and g[i+1][j] != 1)):
                e = False
                break
            #All 2 point cases
            if ((g[i+1][j] == -1 or g[i+1][j] == -3) and (g[i][j + 1] == -1 or g[i][j + 1] == -3)):
                e = False
                break
            if ((g[i][j] == -2 or g[i][j] == -3) and (g[i+1][j + 1] == -2 or g[i+1][j + 1] == -3)):
                e = False
                break
            if (g[i][j] == -1 and g[i+1][j+1] == -1):
                e = False
                break
            if (g[i+1][j] == -2 and g[i][j + 1] == -2):
                e = False
                break
            #End of cases. Iteration
            j += 1
        i += 1
    return e

def permutations(l):
    """Returns a list of all permutations of l.
    Bad; change to a generator."""
    if len(l) == 1:
        yield l
    else:
        t = []
        for i in range(len(l)):
            r = permutations(l[:i] + l[(i + 1):])
            for x in r:
                yield [l[i]] + x

def all_threes(perm):
    """MAKE INTO A GENERATOR"""
    n = len(perm)
    if n == 1:
        yield [1]
        yield [2]
        yield [3]
    else:
        t = all_threes(perm[1:])
        if perm[0] < perm[1]:
            for x in t:
                if x[0] in (1, 3): #The logic behind this line is that if that is the case, only a 2 before it is allowed.
                    yield [2] + x
                else: #x[0] == 2
                    yield [1] + x
                    yield [3] + x #2 is forbidden by a law derived from limit lemma.
        else: #perm[0] > perm[1]
            for x in t:
                if x[0] in (2, 3):
                    yield [1] + x
                else:
                    yield [2] + x
                    yield [3] + x

def all_threes_old(n):
    if n == 0:
        yield []
    else:
        t = all_threes_old(n-1)
        for x in t:
            for i in (1, 2, 3):
                yield [i] + x

def all_valid_old(n):
   orders = permutations(range(1, n+1))
   r = []
   for x in orders:
       types = all_threes(x)
       for y in types:
           g = l_to_grid([(x[i], y[i]) for i in range(n)])
           if is_valid(g):
               r.append(g)
#               print g
   return r

def all_valid_older(n):
    orders = permutations(range(1, n+1))
    r = []
    for x in orders:
        types = all_threes_old(n)
        for y in types:
            g = l_to_grid([(x[i], y[i]) for i in range(n)])
            if is_valid(g):
                r.append(g)
    return r

def skip(a, b):
    if b < a:
        return b
    else:
        return b + 1

def move_up(i, q):
    return [(skip(i, x[0]), x[1]) for x in q]

def possibilities(n, y, i):
    r = set([])
    M = n + 1
    m = 0
    for x in y:
        if x[0] > i and x[0]<M:
            M = x[0]
            if x[1] in (1, 3):
                r.add(1)
                r.add(3)
            else:
                r.add(2)
        elif x[0] < i and x[0] > m:
            m = x[0]
            if x[1] in (2, 3):
                r.add(2)
                r.add(3)
            else:
                r.add(1)
    return [i for i in [1, 2, 3] if i not in r]


def all_valid(n):
    """Returns all the valid lists of size n."""
    if n == 1:
        return [[(1, 1)], [(1, 2)], [(1, 3)]]
    r = []
    p = all_valid(n - 1)
    for i in range(1, n+1):
        for x in p:
            y = move_up(i, x)
            for c in possibilities(n, y, i):
                t = [(i,c)] + y
                if is_valid(l_to_grid(t)):
                    r.append(t)
    return r


def is_right_child(g_sub, g):
    l_sub = grid_to_l(g_sub)
    l = grid_to_l(g)
    u = []
    for x in l[1:]:
        if x[0] < l[0][0]:
            u.append(x)
        else:
            u.append((x[0] - 1, x[1]))
    for i in range(len(u)):
        if u[i][0] != l_sub[i][0] or u[i][1] != l_sub[i][1]:
            return False
    return True

def display(g):
    """Print a sequence of grids."""
    for x in g:
        print l_to_grid(x)
        print '++++++++++++++++++++++++++++++++++++++'

def l_to_tikz(l, x_offset=0, y_offset=0, naked = False):
    return g_to_tikz(l_to_grid(l), x_offset, y_offset, naked);

def g_to_tikz(g, x_offset=0, y_offset=0, naked = False):
    """Transform a grid into LaTeX, invoking the TIKZ package."""
    R = 0.18
    CROSS_LENGTH = 0.2
    ARROW_LENGTH = 0.2
    ARROW_SHADING = "thick"
    n = g.shape[1];
    s = "\\begin{tikzpicture}\n"
    s += "\\draw [help lines] ("+ str(x_offset) + ", " + str(y_offset) + ") grid (" + str(x_offset + n-1) + ", " + str(y_offset + n-1) + ');\n'
    for I in range(n):
        for J in range(n):
            j = n - 1 - I
            i = J
            v = g[I][J]
            start = '(' + str(i + x_offset) + ', ' + str(j + y_offset) + ')'
            if v > 0:
                if naked:
                    continue
                else:
                    end = '(' + str(x_offset + i + int(v == 1 or v == 4)*2*ARROW_LENGTH - ARROW_LENGTH) + ', ' + str(y_offset + j + int(v == 1 or v == 2)*2*ARROW_LENGTH - ARROW_LENGTH) + ')';
                    s += '\\draw [->, ' + ARROW_SHADING + '] ' + start + ' -- ' + end + ';\n'
            else:
                if v == -1 or v == -3:
                    fill = "white"
                else:
                    fill = "black"
                s += '\draw [fill=' + fill + ', thick] ' + start + ' circle [radius = ' + str(R) + '];\n'
                if v == -3:
                    ld = '(' + str(x_offset + i - CROSS_LENGTH) + ', ' + str(y_offset + j - CROSS_LENGTH) + ')';
                    rd = '(' + str(x_offset + i + CROSS_LENGTH) + ', ' + str(y_offset + j - CROSS_LENGTH) + ')';
                    lu = '(' + str(x_offset + i - CROSS_LENGTH) + ', ' + str(y_offset + j + CROSS_LENGTH) + ')';
                    ru = '(' + str(x_offset + i + CROSS_LENGTH) + ', ' + str(y_offset + j + CROSS_LENGTH) + ')';
                    s += '\\draw [thick] ' + ld + ' -- ' + ru + ';\n'
                    s += '\\draw [thick] ' + lu + ' -- ' + rd + ';\n'
    s += "\\end{tikzpicture}\n"
    return s

def reflect_main(l):
    l2 = range(len(l))
    for i in range(len(l)):
        l2[l[i][0] - 1] = (i + 1, l[i][1])
    return l2

def reflect_zero(l):
    n = len(l)
    l2 = range(len(l))
    for i in range(len(l)):
        l2[n -1 - i] = (n + 1 - l[i][0], l[i][1])
    return l2

def reflect_secondary(l):
    n = len(l)
    l2 = range(len(l))
    for i in range(len(l)):
        l2[n -l[i][0]] = (n - i, l[i][1])
    return l2

def transform(i):
    """Correctly transform the index of the fixed point."""
    if i == 3:
        return 3
    else:
        return 3 - i

def reflect_special(l):
    n = len(l)
    return [(n + 1 - x[0], transform(x[1])) for x in l]

def permute(l):
	"""Returns all the group transformations of l."""
	u = [l]
	u2 = u + [reflect_special(x) for x in u]
	u3 = u2 + [reflect_main(x) for x in u2]
	u4 = u3 + [reflect_zero(x) for x in u3]
	return u4
	
def all_unique(n):
	"""Returns all the grids of size n, not including group transformations."""
	l = all_valid(n)
	l2 = []
	for x in l:
		if all([y not in l2 for y in permute(x)]):
			l2.append(x)
	return l2


