#!python2
"""The EQFT prime test by Martin Seysen.
Implemented by Jurjen Bos 2016.
Notation ad close as possible to the article.
Note: if you count the number of field multiplications,
and you assume two tests is equivalent to 9 miller-rabin tests,
the algorithm is faster when n is more than about 100 digits.

Nobody knows if there are numbers that fail even one round,
Searching through some carmichael numbers, I found the following numbers
that only fail the cube root test (for z=x+1, which has norm 2):
4340265931, 34087042891, 37870128451, 46493311411, 48354810571, 245291853691,
494442433171, 716726903707
"""

"""About the choice of the tau list
In the routine setupTau below, we considered performance with the following
criteria.
First, let's estimate the number of steps.
If u is as below (so n**2-1=3**u*r), and s is len(tau)-1,
Martin Seysen suggests to let s grow as sqrt(u).
I'll show that this is not optimal.
First, a coarse search is done, which takes a multiplies per step,
where a is the number of multiplies to check if z**(r*3**i)==1
given z**(s*3**i>>3), and i a value in the tau list.
The coarse search can be done in log(s)/log(2) steps.
(Seysen forgot to realise a binary search is possible here!)
Second, a fine search is done, which takes b multiplies per step,
to find out which value of i between two values of tau is relevant.
Here b is the number of multiplies  check if z**(r*3**i)==1
given z**(r*3**(i-1)).             to
This search takes u/s steps.
Asymptotically, the optimal value of s is the minimum of
a*log(s)/log(2)+b*u/s which gives s = a/log(2)/s-b*u/s**2==0,
so s = u * b/a/log(2). Since (see below) a/b is 2 on average,
s would be .7*u, which is a lot more than sqrt(u).
However, since this takes much more memory, we stick with sqrt.

Now for the precise values of tau we need a and b.
(in 98% of the cases, u<5.)
The values of a and b depend on the remainder of n by powers of 2 and 3.
The value of a consists of:
- 3 squarings (6 modular multiplies)
- zero to three additional multiplies (0 if s%8==0, 1 if s%8==4, 1 or 2 if s%4==2) (0 through 6 modular multiplies)
- a norm calculation (2 modular multiplies) if n%3==1
The value of b consists of:
- a squaring and a multiply (5 modular multiplies)
- a norm (2 modular multiplies) if n%3==1
Overview of values of a and b:
n%24  1    5      7   11  13   17     19  23  Average
a     8  9,12  11,14   9  11  9,12  11,14  6     10
b     7    5      7    5   7    5      7   5      6
a/b is 1.47 in average.

In 98% of the cases, u<5. We can find the optimal value of tau exactly:
u=1: tau=[0,1]: a  (no choice)
u=2: tau=[0,2]: a+b*2/3; [0,1,2]: 4/3*a                    best: [0,1,2]
u=3: tau=[0,3]: a+b*5/3; [0,1,3]: a+b*2/3; [0,2,3]: a*4/3+b*2/3  [0,1,3]
u=4: tau=[0,4]: a+b*8/3; [0,2,4]: a+b*5/3;
u=4: tau=[0,1,4]: a+b*8/3; [0,3,4]: a*4/3+b                best: [0,3,4]
Since the last case is already pretty infrequent, we are content with
the current implementation.
"""
from math import floor, sqrt
from random import randrange

#If OPTIMIZE is true, some messy optimized code get used.
#computations are 40% faster,
#but verbose mode doesn't count all multiplications anymore
OPTIMIZE = False
class Composite(Exception): pass

#from my numtheory library---------------------
def _sqrt1(n):
    """square and round up or down (unspecified!) to int.
    >>> map(_sqrt1, range(10))
    [0, 1, 1, 1, 2, 2, 2, 2, 2, 3]
    >>> _sqrt1(3**1000)==3**500 #really big test
    1
    >>> for i in range(10,100,3):
    ...     for j in range(-100,100,10):
    ...         _sqrt1(3**i+j) and None
    ...
    """
    #handle easy case where n fits in float
    if n<2**50: return int(floor(sqrt(n)))
    #estimate root.
    #Leave about 50 bits, nonnegative multiple of 4
    shift = max(0,n.bit_length()-50&-4)
    rf = sqrt(float(n>>shift))
    #estimate root and stop criterion: r1 is sqrt(n) upwards
    r1 = long(rf)+1<<shift/2
    #bound is sqrt(sqrt(n)) upwards
    bound = long(sqrt(rf))<<shift/4
    #use newton-raphson: force first pass
    r2 = r1+bound
    #we know: if r is true root, this loop makes r+err to r+err**2/(2*n)
    #so this loop does the actual work
    while r2-r1>=bound: r2,r1 = r1,(r1+n/r1)>>1
    #isn't it amazing that this doesn't fail?
    assert (r1-1)**2 < n <(r1+1)**2, "Square root selftest"
    return r1

def issquare(n):
    """issquare(n) -> 1 if n is a perfect square
    >>> map(issquare, range(10))
    [False, True, False, False, True, False, False, False, False, True]
    >>> issquare(3**100)
    1
    >>> issquare(3**100+1)
    0
    """
    if n<1: return False
    #a square always ends in 001(00)* in binary: do quick@dirty check
    lastbit = -n&n
    if lastbit & 0xaaaa:
        #the last bit of n is bit 1,3,5,7,9,11,13,15: not a square
        return False
    if n&7*lastbit != lastbit: return False #if not 001 before them
    #This could be a square, check it
    return _sqrt1(n)**2==n

def jacobi(a,b):
    """Jacobi(a,b)-> Generalized Jacobi symbol
    >>> map(jacobi, range(10), [10]*10)
    [0, 1, 0, -1, 0, 0, 0, -1, 0, 1]
    """
    assert b>0
    if (a|b)&1==0: return 0 #return 0 if both even: gcd=0
    while b&1==0: b=b>>1
    #reduce a, since that doesn't change the result
    a=a%b
    toggle = 1 #output value
    while a>0:
        #b odd at this point: now make a odd
        #first remove factors of four: no toggle needed
        while not a&3: a >>=2
        if not a&1:
            #a even, divide out factor of 2
            a >>=1
            #see if output value changes
            if b&7 in [3,5]: toggle = -toggle
        #exit condition
        if a==1: return toggle
        #see output value changes for swap
        if a&b&3==3: toggle = -toggle
        #reduce for free
        a,b = b%a,a
    #if we come here, the gcd is >1
    return 0

def invmod(a,b):
    """invmod(a,b) -> c so that (a*c)%b=1
    special case of egcd
    >>> invmod(3, 10)
    7
    """
    ar,br=a%b,b
    aa,ba=1,0 #ar=aa*a+?*b;br=ba*a+?*b
    while br:
        k=ar//br
        ar,br=br,ar-k*br
        aa,ba=ba,aa-k*ba
    #we know that ar=aa*a+?*b=aa*a (mod b)
    if ar!=1: raise ValueError("Can't compute invmod(%d,%d): gcd=%d"%(a,b,ar))
    #now we know that aa*a==1 mod b
    return aa%b

#----------------------------------
def R(n, c):
    """Make a class of numbers in Z(x)/(n, x**2-c)
    >>> ring = R(7, -1)
    >>> ring(1,2)**24
    -1
    """
    class Ring:
        """Modular number ax+b"""
        def __init__(self, a, b=None):
            if b is None: a,b = 0,a
            self.a,self.b = a%n,b%n
        @classmethod
        def random(cls):
            return cls(randrange(1000), randrange(1000))
        @classmethod
        def randomNonSquare(cls):
            """Make a random nonsquare element"""
            while True:
                z = cls.random()
                if jacobi(z.norm(), cls.n)==-1: return z
        def __repr__(self):
            a,b = self
            if a>n>>1: a -= n
            if b>n>>1: b -= n
            if a==0: return repr(b)
            return '{:d}x{:+d}'.format(a, b)
        def __str__(self):
            return 'Ring({0.a},{0.b})'.format(self)
        def __iter__(self):
            yield self.a
            yield self.b
        def __neg__(self):
            return self.__class__(-self.a, -self.b)
        def norm(self):
            return self.b**2-c*self.a**2
        def conj(self):
            return self.__class__(-self.a, self.b)
        def __add__(self, other):
            if isinstance(other, (int, long)):
                return self.__class__(self.a, self.b+other)
            return self.__class__(self.a+other.a, self.b+other.b)
        def __sub__(self, other):
            if isinstance(other, (int, long)): other = Ring(other)
            return self.__class__(self.a-other.a, self.b+other.b)
        def __mul__(self, other):
            if isinstance(other, (int, long)):
                return self.__class__(self.a*other, self.b*other)
            #use 3 (or 2 for squaring) big multiplies
            #note: big multiplies for 512 bits are about 10* small ones
            m1 = other.a*self.b
            m2 = m1 if other is self else self.a*other.b
            return self.__class__(m1+m2,
                (c*other.a+other.b)*(self.a+self.b)-c*m1-m2)
        if c==-1:
            #optimisation of multiplication in this frequent case
            def __mul__(self, other):
                if isinstance(other, (int, long)):
                    return self.__class__(self.a*other, self.b*other)
                m1 = other.a*self.b
                m2 = m1 if other is self else self.a*other.b
                return self.__class__(m1+m2,
                    (other.b-other.a)*(self.a+self.b)+m1-m2)
        def inv(self):
            try: return self.conj()*invmod(self.norm(), n)
            except ValueError: raise Composite('Inverse')
        def __pow__(self, exp):
            result = self if exp&1 else self.__class__(1)
            factor = self
            exp >>= 1
            while exp:
                factor *= factor
                if exp&1: result *= factor
                exp >>= 1
            return result
        if OPTIMIZE:
            def __pow__(self, exp):
                resulta, resultb = (self.a, self.b) if exp&1 else (0,1)
                factora, factorb = self.a, self.b
                exp >>= 1
                while exp:
                    m1 = factora*factorb
                    factora, factorb = (2*m1%n,
                        ((c*factora+factorb)*(factora+factorb)-(c+1)*m1)%n)
                    if exp&1:
                        m1 = factora*resultb
                        m2 = resulta*factorb
                        resulta, resultb = ((m1+m2)%n,
                            ((c*factora+factorb)*(resulta+resultb)-c*m1-m2)%n)
                    exp >>= 1
                return self.__class__(resulta, resultb)
        def __eq__(self, other):
            if isinstance(other, (int, long)): other = Ring(other)
            return self.a==other.a and self.b==other.b

        def __ne__(self, other): return not self==other

    #for easy access
    Ring.n = n
    Ring.c = c
    return Ring

def MR2(n):
    """Initialize prime testing.
    >>> for p in 23, 29, 41:
    ...     c, eps = MR2(p)
    ...     assert jacobi(c, p)==-1
    ...     ring = R(p, c)
    ...     eps = ring(*eps)
    ...     assert eps**4==-1
    """
    if n&3==3:
        alpha = pow(2, n>>2, n)
        #this tests 2*alpha**2 in (1,n-1), a bit faster
        if pow(alpha,2,n)-(n-1>>1) not in (0,1):
            raise Composite('MR')
        return -1, (alpha, alpha)
    if n&7==5:
        alpha = pow(2, n>>2, n)
        if pow(alpha,2,n)!=n-1:
            raise Composite('MR')
        if alpha&1==0: alpha -= n
        return 2, (1+alpha>>1, 0)
    if n&7==1:
        if issquare(n): raise Composite('Square')
        c = 3
        while  jacobi(c, n)==1:
            c += 4 if c%6==1 else 2
        alpha = pow(c, n>>3, n)
        if pow(alpha, 4, n)!=n-1:
            raise Composite('MR')
        return c, (0, alpha)
    raise Composite('Even')

class PrimeTester:
    """Structure the mess of computations needed to perform the SQFT3 test.
    >>> n = 101
    >>> c, eps8 = MR2(n)
    >>> ring = R(n, c)
    >>> pt = PrimeTester(ring, ring(*eps8))
    >>> for i in range(3): pt.round(ring.randomNonSquare())
    """
    def __init__(self, ring, eps8):
        """sets up values of r, s, u, and the tau mapping
        and the values eps8, eps8**r and eps3 (starting as 1)
        so that you can call round()
        """
        self.ring = ring
        self.n = ring.n
        self.nOffset = {1:-1, 2:1}[self.n%3]
        self.u, self.s = self.split3power(self.n+self.nOffset)
        #note: n**2-1 = (n+nOffset)*(n-nOffset) so r/s = n-nOffset
        self.r = self.s*(self.n-self.nOffset)
        self.eps8, self.eps3 = eps8, None
        #tau is independent of z
        self.setupTau()

    @staticmethod
    def split3power(n):
        """Return u,r so that n=3**u*r and r not divisible by 3.
        >>> PrimeTester.split3power(2700)
        (3, 100)
        """
        u,r = 0,n
        while r%3==0: u,r = u+1, r//3
        return u,r

    @staticmethod
    def eightPower(x, xa8, a, b):
        """Compute x**(a*b>>3), minimizing multiplications
        by making use of xa8 = x**(a>>3)
        The trick is this observation:
        (a+b)>>3 = (a>>3)+(b>>3) + (a&7)+(b&7)>>3
        Note that the last term is 0 if (a&7)+(b&7)<8, else 1
        so if we have xa8 = x**(a>>3) and xb8 = x**(b>>3), we compute
        xab8 = x**(a+b>>3) as: xab8 = xa8*xb8; if (a&7)+(b&7)>=8: xab8 *= x
        (if a==8, this check can be simplified to a&4)
        """
        #this is shaped like the __pow__ above
        #keeping only the lower three bits of the exponents
        #invariant: if x**(result>>3)==result8, then result7 = result&7
        factor8, factor7 = xa8, a&7
        if b&1:
            result8,result7 = factor8,factor7
        else:
            result8, result7 = x.__class__(1), 0
        b >>= 1
        while b:
            #square factor8
            factor8 **= 2
            if factor7>3: factor8 *= x
            factor7 = factor7*2&7
            if b&1:
                #do the multiply
                result8 *= factor8
                if result7+factor7>=8: result8 *= x
                result7 = result7+factor7&7
            b >>= 1
        return result8

    if OPTIMIZE:
        @staticmethod
        def eightPower(x, xa8, a, b):
            """Compute x**(a*b>>3), minimizing multiplications
            by making use of xa8 = x**(a>>3)
            The trick is this observation:
            (a+b)>>3 = (a>>3)+(b>>3) + (a&7)+(b&7)>>3
            Note that the last term is 0 if (a&7)+(b&7)<8, else 1
            so if we have xa8 = x**(a>>3) and xb8 = x**(b>>3), we compute
            xab8 = x**(a+b>>3) as: xab8 = xa8*xb8; if (a&7)+(b&7)>=8: xab8 *= x
            (if a==8, this check can be simplified to a&4)
            """
            #this is shaped like the __pow__ above
            #keeping only the lower three bits of the exponents
            #invariant: if x**(result>>3)==result8, then result7 = result&7
            factora, factorb, factor7 = xa8.a, xa8.b, a&7
            if b&1:
                resulta, resultb, result7 = xa8.a, xa8.b, a&7
            else:
                resulta, resultb, result7 = 0, 1, 0
            b >>= 1
            n, c, xa, xb = x.n, x.c, x.a, x.b
            while b:
                #square factor8
                m1 = factora*factorb%n
                factora, factorb = (2*m1%n,
                    ((c*factora+factorb)*(factora+factorb)-(c+1)*m1)%n)
                if factor7>3:
                    #additional multiply
                    m1 = xa*factorb%n
                    m2 = factora*xb%n
                    factora, factorb = ((m1+m2)%n,
                        ((c*xa+xb)*(factora+factorb)-c*m1-m2)%n)
                factor7 = factor7*2&7
                if b&1:
                    #do the multiply
                    m1 = factora*resultb%n
                    m2 = resulta*factorb%n
                    resulta, resultb = ((m1+m2)%n,
                        ((c*factora+factorb)*(resulta+resultb)-c*m1-m2)%n)
                    if result7+factor7>=8:
                        #additional multiply
                        m1 = xa*resultb%n
                        m2 = resulta*xb%n
                        resulta, resultb = ((m1+m2)%n,
                            ((c*xa+xb)*(resulta+resultb)-c*m1-m2)%n)
                    result7 = result7+factor7&7
                b >>= 1
            return x.__class__(resulta, resultb)

    def setupTau(self):
        """Select intermediate points for coarse search.
        We search in values z**(s*3**i) for i in range(u+1)
        Tau is the array that indicates the "coarse" values of i.
        Memory usage is linear in len(tau),
        while speed of the search is linear in 1/(len(tau).
        For choice of tau: see above.
        >>> pt = PrimeTester(R(7,-1),None)
        >>> for u in range(1,5):
        ...   pt.u = u
        ...   pt.setupTau()
        ...   print(pt.tau)
        [0, 1]
        [0, 2]
        [0, 1, 3]
        [0, 2, 4]
        """
        #Choose f on the high side, make sure e>0
        u = self.u
        f = int(floor(sqrt(u+2)))
        g = u%f
        if g: self.tau = [0]+range(g, u+f, f)
        else: self.tau = range(0, u+f, f)

    def setupChain(self):
        """Build the chain of z**(3**tau(i)*s>>3)
        >>> pt = PrimeTester(R(1459,-1),None); pt.z = pt.ring(1,2)
        >>> pt.setupChain()
        >>> pt.t
        [1, 4x+3, 476x-543, 359x+225]

        s is 2, and tau is [0,2,4,6], so we have powers 2//8,18//8,162//8,1458//8
        >>> pt.z**0, pt.z**2, pt.z**20, pt.z**182
        (1, 4x+3, 476x-543, 359x+225)
        """
        self.t = t = [self.z**(self.s>>3)]
        z, s, tau = self.z, self.s, self.tau
        for i in range(len(tau)-1):
            t.append(self.eightPower(z, t[-1], 3**tau[i]*s, 3**(tau[i+1]-tau[i])))

    def z3powTauS(self, i):
        """Compute z**(3**tau(i)*s) given i
        >>> pt = PrimeTester(R(1459,-1),None); pt.z = pt.ring(1,2)
        >>> pt.setupChain()
        >>> pt.z3powTauS(2)==pt.z**162
        True
        >>> pt.z3powTauS(3)==pt.z**1458
        True
        """
        return self.eightPower(self.z, self.t[i], 3**self.tau[i]*self.s, 8)

    def checkZ3powRis1fromS(self, z3powerIS):
        """Given z**(3**i*s), decide if z**(3**i*r)==1
        This assumes that z**n==z.conj()
        """
        n = self.n
        if n%3==1: return z3powerIS.norm()%n==1
        elif n%3==2: return z3powerIS.a==0
        else: raise Composite("Divisible by 3")

    def getZ3powRfromS(self, z3powerIS):
        """Given z**(3**i*s), compute z**(3**i*r)
        Always returns a ring element, to simplify further computations.
        """
        n = self.n
        if n%3==1: return self.ring(z3powerIS.norm())
        elif n%3==2: return z3powerIS.inv()*z3powerIS.conj()
        else: raise Composite("Divisible by 3")

    def coarseSearch(self):
        """Given z**(n**2-1)==1,
        find lowest i with z**(3**tau(i)*r)==1
        Uses binary search (small improvement to Seysen).
        Returns i, and z**(3**tau(i-1)*s) if lo>0.
        Note that although the value of i is almost always len(tau)-1,
        we still do a binary search, since we have to compute z3tauLo1s
        anyway, and it doesn't reduce the average case by a lot,
        while it reduces worst case by many multiplications.
        """
        #invariant: all values<lo are !=1, all values >=hi are =1
        #z**r!=1 implies z**(r*3**tau[0])!=1
        #z**(n**2-1)==1 implies z**(r*3**tau[-1])==1
        lo, hi = 0, len(self.tau)-1
        #keep z**(3**tau(lo-1)*s) in z3tauLo1s
        z3tauLo1s = None
        while lo<hi:
            mid = lo+hi>>1
            z3taumids = self.z3powTauS(mid)
            if self.checkZ3powRis1fromS(z3taumids):
                hi = mid
            else:
                lo = mid+1
                z3tauLo1s = z3taumids
        #now we know that z**(r*3**tau[lo])==1 and z**(r*3**tau[lo-1])!=1
        return lo, z3tauLo1s

    def fineSearch(self,i,j,z3powerI1s):
        """Given i,j with z**(3**(i-1)*r)!=1 and z**(3**j*r)==1,
        find minimal value k with i<=k<=j so that z**(3**k*r)==1
        and return z**(3**(k-1)*s)
        Also expects to get the value of z**(3**(i-1)*s)
        """
        while i+1<j:
            z3powerIs = z3powerI1s**3
            if self.checkZ3powRis1fromS(z3powerIs):
                break
            i +=1
            z3powerI1s = z3powerIs
        return z3powerI1s

    def checkZn(self):
        """Return z**(n>>8) and check if z**n = z.conj()
        """
        #since t[i]==z**(3**tau[i]*s>>3) and tau[-1]==u,
        #we have t[-1]==z**(n+nOffset>>3),
        #which is almost always equal to z**(n>>3)
        zn8 = self.t[-1]
        #except when n%24=23, then it is z**((n>>3)+1)
        if self.n%24==23: zn8 *= self.z.inv()
        #now check
        zn = self.eightPower(self.z, zn8, self.n, 8)
        if zn!=self.z.conj(): raise Composite("zn!=zconj")
        return zn8

    def checkZnn18(self, zn8):
        """Check if z**(n**2-1>>3) is an eighth root.
        zn8 is supposed to be z**(n>>3)
        """
        #Compute z**(n**2-1>>3) to see if it is +-eps(3)
        #Note that since n = (n&7)+(n&~7), we can write
        #n**2-1>>3 = n**2>>3 = (n&~7)*n+(n&7)*n>>3 = (n>>3)*n + (n*(n&7)>>3)
        z, n = self.z, self.n
        znn18 = zn8.conj()                           #(n>>3)*n
        znn18 *= self.eightPower(z, zn8, n, n&7)     #n*(n&7)>>3
        #check if znn18 is one of eps, -eps, eps**3, -eps**3
        #postpone computing eps**3 to only if needed
        eps = self.eps8
        if znn18 not in (eps, -eps):
            epsCubed = eps**3
            if znn18 not in (epsCubed, -epsCubed):
                raise Composite("znn18!=eps")

    def round(self, z):
        """Setup the chain for given z, and test everything
        May find and store a cube root of 1 in the process
        """
        self.z = z
        self.setupChain()
        zn8 = self.checkZn()
        self.checkZnn18(zn8)
        onePos, z3tauLo1s = self.coarseSearch()
        #now we know that z**(r*3**tau[onePos])==1 and z**(r*3**tau[onePos-1])!=1
        #if onePos is zero, z**r==1 so there's nothing to check further
        if onePos:
            #we know the first one is between tau[onePos-1] and tau[onePos]
            #and we got z**(3**tau[onePos-1]*s)
            valueBeforeOne = self.fineSearch(
                self.tau[onePos-1], self.tau[onePos], z3tauLo1s)
            #construct cube root from valueBeforeOne
            valueBeforeOne = self.getZ3powRfromS(valueBeforeOne)
            if self.eps3 is None:
                #check cyclotomic polynomial
                if valueBeforeOne**2+valueBeforeOne!=-1:
                    raise Composite("Cube root")
                self.eps3 = valueBeforeOne
            elif valueBeforeOne==self.eps3:
                #correct cube root, save two multiplies for check
                pass
            elif valueBeforeOne!=self.eps3**2:
                #Wonder if this statement ever will be executed...
                raise Composite("Second cube root")

def isprime(n, iterations=3):
    """The full EQFT3 test.
    >>> isprime(41221)
    True
    """
    #Trial divisions and small primes: needed according to Seysen
    if n<1: raise ValueError("isprime(n): n must be >0")
    #primes, 2, 3, 5 and divisors 2 and 3
    if n<7: return n in (2, 3, 5)
    if n%6 not in (1,5): return False
    #primes 5..199
    d = 5
    while d<200:
        if n%d==0: return False
        d += 4-d%6//2
        if d*d>n: return True
    #The real test
    try:
        c, eps8 = MR2(n)
        ring = R(n, c)
        pt = PrimeTester(ring, ring(*eps8))
        for i in range(iterations): pt.round(ring.randomNonSquare())
    except Composite: return False
    return True

#test/demo code
class VerbosePrimeTester(PrimeTester):
    """Show calculations and count multiplies.
    """
    def __init__(self, ring, eps8):
        PrimeTester.__init__(self, ring, eps8)
        if self.s<10**50:
            print( "Write n as %d*3**%d%+d"%(self.s, self.u, -self.nOffset) )
        else:
            print( "Write n as s*3**%d%+d"%(self.u, -self.nOffset) )
    def setupTau(self):
        result = PrimeTester.setupTau(self)
        print( "Tau:", ','.join(map(str, self.tau)) )
    def setupChain(self):
        startCount = self.ring.counter
        PrimeTester.setupChain(self)
        print( "Setting up chain z**(s*3**i>>3): %d multiplies"%(
            self.ring.counter-startCount) )
        if self.n*self.u<10**50: print( "Exponents of chain:", ','.join(
            str(self.s*3**i>>3) for i in self.tau))
    def z3powTauS(self, i):
        startCount = self.ring.counter
        result = PrimeTester.z3powTauS(self, i)
        print( "   Computing z**(s*3**%d): %d multiplies"%(
            self.tau[i], self.ring.counter-startCount) )
        return result
    def checkZ3powRis1fromS(self, z3powerIS):
        startCount = self.ring.counter
        result = PrimeTester.checkZ3powRis1fromS(self, z3powerIS)
        print( "   Corresponding r power is %s1: %d multiplies"%(
            "" if result else "not ",
            self.ring.counter-startCount) )
        return result
    def getZ3powRfromS(self, z3powerIS):
        startCount = self.ring.counter
        try: return PrimeTester.getZ3powRfromS(self, z3powerIS)
        finally: print( "   Converting s power to r power: %d multiplies"%(
            self.ring.counter-startCount) )
    def coarseSearch(self):
        startCount = self.ring.counter
        print( "Coarse search for first z**(r*3**tau[i])==1 in 0<= i <%d"%(
            len(self.tau)) )
        result = PrimeTester.coarseSearch(self)
        if result[0]:
            print( "First 1 in z**(r*3**i) in %d<i<=%d (subtotal %d multiplies)"%(
                self.tau[result[0]-1], self.tau[result[0]],
                self.ring.counter-startCount) )
            #if result[0]: print( "   Also computed z**(s*3**%d)"%(result[0]-1) )
        else:
            print( "First 1 occurs immediately at z**r (subtotal %d multiplies)"%(
                self.ring.counter-startCount) )
        return result
    def fineSearch(self,i,j,z3powerI1s):
        startCount = self.ring.counter
        print( "Finding value before first 1 in %d..%d (5 multiplies per step)"%(
            i+1, j) )
        result = PrimeTester.fineSearch(self,i,j,z3powerI1s)
        print( "Found value before 1 in (subtotal %d multiplies)"%(
            self.ring.counter-startCount) )
        return result
    def checkZn(self):
        startCount = self.ring.counter
        try: return PrimeTester.checkZn(self)
        finally: print( "Checking z**r==r.conj(): %d multiplies"%(
            self.ring.counter-startCount) )
    def checkZnn18(self, zn8):
        startCount = self.ring.counter
        try: return PrimeTester.checkZnn18(self, zn8)
        finally:
            print( "Checking z**(n**2-1>>3) is +-eps, +-eps**3: %d multiplies"%(
                self.ring.counter-startCount) )
    def round(self, z):
        startCount = self.ring.counter
        oldeps3 = self.eps3
        try:
            PrimeTester.round(self, z)
        finally:
            if self.eps3 is None:
                print( "Final round check, no cube root" )
            elif oldeps3 is None:
                print( "Final check, found cube root (2 multiplies)" )
            else:
                print( "Final check, checked cube root (0 or 2 multiplies)" )
            print ( "Subtotal for this round: %d"%(
                self.ring.counter-startCount) )

def verboseTest(n, iterations=2, showMultiplies=False, forcez=None):
    """Like isprime(), but verbose
    Skips check for primes 5..199
    showMultiplies shows "n" for every norm computation,
    and "*" for every quadratic field multiply,
    and "s" for every square.
    """
    if n%6 not in (1,5): return False
    try:
        multiplies = n.bit_length()+sum(map(int,bin(n)[2:]))-2
        print( "Miller-Rabin test with base 2: %d multiplies"%(multiplies) )
        c, eps8 = MR2(n)
        ring = R(n, c)
        class countingRing(ring):
            counter = multiplies
            def __mul__(self, other):
                #count field multiplication
                if self!=1 and other!=1:
                    self.__class__.counter += 2+(self is not other)
                    if showMultiplies: print('s' if self is other else '*'),
                return ring.__mul__(self, other)
            def norm(self):
                self.__class__.counter += 2
                if showMultiplies: print( 'n', end='' )
                return ring.norm(self)
        pt = VerbosePrimeTester(countingRing, countingRing(*eps8))
        for i in range(iterations):
            print( )
            startCount = countingRing.counter
            z = countingRing.randomNonSquare()
            if forcez: z = countingRing(*forcez)
            print( "making z: %r: %d multiplies"%(
                z, countingRing.counter-startCount) )
            pt.round(z)
    except Composite, e:
        print( "I found number is not prime:", e.args[0] )
        return False
    finally:
        try: print( "Total multiplications:", countingRing.counter )
        except UnboundLocalError: pass
    return True

def ng():
    from random import getrandbits
    while True:
        n = getrandbits(32)*3**5
        yield n-1
        yield n+1

def ng3():
    yield 3277
    yield 29341
    yield 104653
    yield 172369
    yield 314821
    yield 104653
    yield 172369
    yield 800605
    yield 873181
    yield 1509709
    yield 2909197
    yield 5256091
    yield 18443701
    yield 22075579
    yield 133800661
    yield 702683101
    yield 1680929605501
    yield 92503267006501
    yield 212710032843751

def findStrangeNumbers(ng):
    """Try lots of numbers, and run splitTestParts
    on the pseudoprimes.
    """
    import user, numtheory
    while True:
        for n in ng:
            try: c, eps8 = MR2(n)
            except Composite: continue
            if not numtheory.isprime(n): break
        else: break
        #we hebben een composiet getal dat de MR2 overleeft
        print( n )
        for i in range(5): splitTestParts(n)

def splitTestParts(n, z=None):
    c, eps8 = MR2(n)
    ring = R(n, c)
    pt = PrimeTester(ring, ring(*eps8))
    pt.z = z or pt.ring.randomNonSquare()
    pt.setupChain()
    #this fails for 973241
    try: zn8 = pt.checkZn()
    except Composite: pass
    else: print( "Fail a:", n )
    try: pt.checkZnn18(pt.z**(n>>8))
    except Composite: pass
    #this fails for ???
    else: print( "Fail b:", n )
    onePos, z3tauLo1s = pt.coarseSearch()
    if onePos:
        #coarseSearch uses the assumption that z**n==z.conj
        #this results that onePos can be wrong
        #fails for 1509709
        if pt.z**pt.r==1:
            print( "Partial fail:", n )
        #and we got z**(3**tau[onePos-1]*s)
        valueBeforeOne = pt.fineSearch(
            pt.tau[onePos-1], pt.tau[onePos], z3tauLo1s)
        #construct cube root from valueBeforeOne
        valueBeforeOne = pt.getZ3powRfromS(valueBeforeOne)
        #check cyclotomic polynomial (pseudoprime: 665281, 5256091, 6787327)
        if valueBeforeOne**2+valueBeforeOne==-1:
            print( "Fail c:", n )

def makeTestPrime(size, factors3, sign):
    """Find a prime of approximately the given number of bits
    with the at least given number of factors of 3.
    Set sign=1 to make n+1 divible by 3, -1 othersize.
    """
    r = randrange(1<<size-1, 1<<size)
    r = r-r%3**factors3-1
    while not isprime(r): r += 3**factors3
    return r
if __name__=='__main__':
    import doctest
    doctest.testmod()
