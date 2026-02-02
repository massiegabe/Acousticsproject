from pylab import *

def rk4Int(s, dt, t, derivs, params=None):
    """
    Take a single RK4 step. 
    
    s = state
    dt = step in time
    t = current time
    derivs = function to compute state derivatives
    params = whatever you like.. passed through to derivs
    """
    f1 = derivs(s, t, params)
    f2 = derivs(s+f1*dt/2.0, t+dt/2.0, params)
    f3 = derivs(s+f2*dt/2.0, t+dt/2.0, params)
    f4 = derivs(s+f3*dt, t+dt, params)
    return s + (f1+2*f2+2*f3+f4)*dt/6.0

def dFunc(s, x, params):
    p = s[0]
    u = s[1]
    dpdx = -params['zf']*u/S(x)
    dudx = params['yf']*S(x)*p
    return array([dpdx, dudx])

def S(x):
    if (x < (L/2-a/2)) or (x > (L/2+a/2)) :
        return r
    else:
        return a
    
N=100
L=100.0
r=10.0
a=3.0*r/8.0
gamma = 1.4
P0=1.0

rho=1.0

dx = 0.1

s = array([1.0, 0.0])  # state is [p, U] close B.C. set p=1.0, U=0.0
x = 0.0

plist = [s[0]]
ulist = [s[1]]
xlist = [x]

omega = 0.035
zfactor = omega*rho
yfactor = omega/(gamma*P0)

while x<L:
    s = rk4Int(s, dx, x, dFunc, {'zf':zfactor, 'yf':yfactor})
    x += dx
    plist.append(s[0])
    ulist.append(s[1])
    xlist.append(x)

plot(xlist, plist, 'b-')
show()

    
        

