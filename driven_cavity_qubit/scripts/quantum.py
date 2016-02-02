from os import sys, path 
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from simulationManager.papyllon_simulation import PapyllonSimulation
from scipy.optimize import fsolve
import numpy as np
from CPB_cav import JC
from qutip import *


s = PapyllonSimulation(__file__,["N_photons","wc","kappa","gamma","xi","wd","g0", "Ec", "Ej", "d", "N_cpb","flux","wc2"])

##############
# compute coupling and qubit frequency for all different fluxes
##############

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
    wq = jc_parameters[str(s.flux)]["wq"]
    xi = 10 ** s.xi * s.kappa /1.42
    # construct composite operators
    a = tensor(destroy(s.N_photons), qeye(2))
    sm = tensor(qeye(s.N_photons), sigmam())
    # Hamiltonian
    H = (wq - s.wd) * sm.dag() * sm + (s.wc - s.wd) * a.dag() * a + \
        1j * g * (a.dag() * sm - sm.dag() * a + a * sm - sm.dag() * a.dag()) + xi * (a.dag() + a)

    # Collapse operators
    C1 = np.sqrt(2 * s.kappa) * a
    C2 = np.sqrt(s.gamma) * sm

    try:
        # find steady state
        rhoss = steadystate(H, [C1, C2], method = 'power')

        # calculate expectation value
        S11 = expect(a*a.dag(), rhoss)
        
    except Exception, e:
        print "Calculation failed: "+str(e)
        return -1

    return S11
    

if __name__ == "__main__":
    s.run(parfunc)