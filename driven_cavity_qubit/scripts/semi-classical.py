from ??? import PapyllonSimulation
s = PapyllonSimulation(__file__,['wc','g','delta','k','chi','xi','wd'])

def parfunc(p):
    s.set_parameters(p)

    # Simulation code
    

if __name__ == "__main__":
    s.run(parfunc)