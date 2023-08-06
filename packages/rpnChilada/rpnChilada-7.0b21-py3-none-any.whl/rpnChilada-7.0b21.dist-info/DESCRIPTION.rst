
rpnChilada is a command-line Reverse-Polish Notation calculator that was
first written in C in 1988 as a four-function calculator.

It was rewritten in Python 3 in 2012 and now uses the mpmath library.  It
was a Python learning exercise for me, and a fun little toy, but when I
found mpmath, it became really cool and powerful, so props to Fredrik
Johansson, who did most of the heavy lifting (http://mpmath.org).

rpnChilada gives you the whole enchilada when it comes to playing with
numbers.  You get math functions, algebra functions, combinatoric functions,
number theory functions, astronomy functions, physics functions, unit
conversions (comparable to GNU Units) and much, much more.   rpnChilada
supports lists, but not matrices.

rpnChilada comes with integrated help, which isn't complete, but has at
least a basic description of every function, and over 1200 built-in
examples.

rpnChilada also comes with an extensive test suite, which is being constantly
improved.  Many of the functions are validated against the OEIS.

Version 7 has been in the works for more than two and a half years, and the
number of operators since version 6.4 has increased by at least 200.  It also
supports user-defined persistent variables and functions.  rpnChilada also
caches lookups and certain calculations.

There are still bugs, and since it's a one-person side project, progress
is slow, but bug reports and feature requests are welcome at rickg@his.com.

Note, Windows users will want the Windows-specific wheels for pyephem and
gmpy2:

https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyephem
https://www.lfd.uci.edu/~gohlke/pythonlibs/#gmpy

rpnChilada can be launched with 'rpnChilada' or 'rpn' in the Python Scripts/
directory.

For a quick primer on rpnChilada's use, try "rpn help examples".  Please note
that the OEIS integration and geographic location functions require Internet
access.


