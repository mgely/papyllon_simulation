from os import sys, path 
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from simulationManager.papyllon_simulation import PapyllonSimulation
from scipy.optimize import fsolve
import numpy as np
from CPB_cav import JC


s = PapyllonSimulation(__file__,['wc','k','xi','wd','g0', 'Ec', 'Ej', 'd', 'N_cpb','flux','wc2'])

jc = JC(s.g0, s.wc, 8, s.Ec, s.Ej, s.d, s.N_cpb,fc2 = s.wc2,flux = -1.32523)

if s.X_name == "flux":
    flux_list = np.linspace(s.X_start,s.X_end,s.X_points)
elif s.Y_name == "flux":
    flux_list = np.linspace(s.Y_start,s.Y_end,s.Y_points)
elif s.Z_name == "flux":
    flux_list = np.linspace(s.Z_start,s.Z_end,s.Z_points)
else:
    flux_list = [s.flux]

jc = JC(s.g0, s.wc, 8, s.Ec, s.Ej, s.d, s.N_cpb,fc2 = s.wc2)
jc_parameters = {}
for f in flux_list:
    jc.cpb.set_flux(f)
    jc_parameters[str(f)] = {"g":jc.g(0,1),
                            "wq":jc.cpb.f(0,1)}

def parfunc(p):
    s.set_parameters(p)
    g = jc_parameters[str(s.flux)]["g"]
    delta = jc_parameters[str(s.flux)]["wq"]-s.wc
    xi = s.k /1.42 * 10 ** s.xi
    def equation(A):
        return A**2 - s.wc**2*xi**2 / ((s.wd**2-(s.wc-np.sign(delta)*g**2/np.sqrt(2*g**2*(A**2-1)+delta**2))**2)**2+s.k**2*s.wd**2)

    return fsolve(equation, xi)/xi
    

if __name__ == "__main__":
    s.run(parfunc)