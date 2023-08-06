import rpnGlobals as g

import rpnNumberTheory
import rpnMath

sum = 0

g.dataPath = 'rpndata'

for i in range( 1, 10001 ):
    result = rpnNumberTheory.getEulerPhi( i * i )

    if rpnMath.isPower( result, 3 ):
       sum += i

print( sum )

