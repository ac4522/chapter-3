from numbers import Number


class Polynomial:

    def __init__(self, coefs):
        self.coefficients = coefs

    def degree(self):
        return len(self.coefficients) - 1

    def __str__(self):
        coefs = self.coefficients
        terms = []

        if coefs[0]:
            terms.append(str(coefs[0]))
        if self.degree() and coefs[1]:
            terms.append(f"{'' if coefs[1] == 1 else coefs[1]}x")

        terms += [f"{'' if c == 1 else c}x^{d}"
                  for d, c in enumerate(coefs[2:], start=2) if c]

        return " + ".join(reversed(terms)) or "0"

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.coefficients) + ")"

    def __eq__(self, other):

        return isinstance(other, Polynomial) and\
             self.coefficients == other.coefficients

    def __add__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a + b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + other.coefficients[common:]

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] + other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other
    

    def __sub__(self, other):

        if isinstance(other, Polynomial):
            common= min(self.degree(), other.degree())+1
            a=self.degree()-other.degree()
            coefs= tuple(a - b for a,b in zip(self.coefficients, other.coefficients))
            if a>0:
                coefs += self.coefficients[common:]
            elif a<0:
                coefs += tuple(x*-1 for x in other.coefficients[common:])
            
            return Polynomial(coefs)
        
        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] - other,)
                              + self.coefficients[1:])
        else:
            return NotImplemented

    def __rsub__(self, other):
        a=self-other
        coefs=tuple(x*-1 for x in a.coefficients)
        return Polynomial(coefs)
    
    def __mul__(self, other):
        if isinstance(other, Polynomial):
            maxdegree = self.degree() + other.degree()
            coefs = [0] * (maxdegree + 1)
            for x in range(maxdegree + 1):
                sum = 0
                for y in range(min(self.degree() + 1, x + 1)):
                    if x - y <= other.degree():
                        sum += self.coefficients[y] * other.coefficients[x - y]
                coefs[x] = sum
            return Polynomial(tuple(coefs))
        elif isinstance(other, Number):
            return Polynomial(tuple(other * x for x in self.coefficients))
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __pow__(self, power):
        if isinstance(power, Number):
            newpoly = self
            for x in range(1, power):
                newpoly = newpoly * self
            return newpoly
        else:
            return NotImplemented

    def __call__(self, num):
        if isinstance(num, Number):
            sum = 0
            for x in range(len(self.coefficients)):
                sum += self.coefficients[x] * (num**x)
            return sum
        else:
            return NotImplemented

    def dx(self):
        newpoly = Polynomial(
            tuple(
                self.coefficients[x + 1] * (x + 1)
                for x in range(len(self.coefficients) - 1)
            )
        )
        if newpoly.coefficients == ():
            newpoly.coefficients = (0,)
        return newpoly


def derivative(poly):
    return poly.dx()

