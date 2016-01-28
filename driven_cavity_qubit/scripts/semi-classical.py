from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from simulationManager.papyllon_simulation import PapyllonSimulation
from scipy.optimize import fsolve
import numpy as np

s = PapyllonSimulation(__file__,['wc','g','delta','k','xi','wd'])

def parfunc(p):
    s.set_parameters(p)
    xi = s.k /1.42 * 10 ** s.xi
    def equation(A):
        return A**2 - s.wc**2*xi**2 / ((s.wd**2-(s.wc+s.g**2/np.sqrt(2*s.g**2*(A**2-1)+s.delta**2))**2)**2+s.k**2*s.wd**2)

    return fsolve(equation, xi)/xi
    

if __name__ == "__main__":
    s.run(parfunc)