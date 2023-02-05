import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory
import time, numpy as np

model = ConcreteModel()

model.x = pyo.Var(range(1,6), within= Integers, bounds=(0,None))
model.y = pyo.Var(bounds=(0,None))

x = model.x
y = model.y

model.c1 = pyo.Constraint( expr =  sum([ x[i]for i in range(1,6)])+y<=20 )
model.c2 = pyo.ConstraintList()

for i in range(1,6):
    model.c2.add( expr= x[i]+y >=15 )
model.c3= pyo.Constraint( expr =  sum([x[i]*i for i in range(1,6)])>=10 )
model.c4 = pyo.Constraint( expr = x[5]+2*y>=30 )

model.obj = pyo.Objective( expr = sum([x[i] for i in range(1,6)])+y, sense=minimize)

begin = time.time()

opt = SolverFactory('gurobi')
opt.solve(model)

delta_t = time.time()-begin

model.pprint()

print('total time:', np.round(delta_t,2))

for i in range(1,6):
    print('x[%i] = %i' % (i, pyo.value(x[i])))


print('y = %.2f' % pyo.value(y))
print('Obj = ', pyo.value(model.obj))

