from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from simulationManager.papyllon_simulation import PapyllonSimulation

s = PapyllonSimulation(__file__,['wc','g','delta','k','chi','xi','wd'])

def parfunc(p):
    s.set_parameters(p)

    return 1
    

if __name__ == "__main__":
    s.run(parfunc)