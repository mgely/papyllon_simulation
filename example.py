s = PapyllonSimulation('3D')

s.wc = 9e9
s.g = 100e6
s.delta = 1.0e9
s.k = 1e6
s.chi = s.g**2/s.delta

s.set_X( name = ,
                start = ,
                end = ,
                points = )

s.set_Y( name = ,
                start = ,
                end = ,
                points = )

s.set_Z( name = ,
                start = ,
                end = ,
                points = )


def parfunc():
    # Do stuff

if __name__ == "__main__":
    s.run(parfunc)