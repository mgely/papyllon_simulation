from qutip import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin

class CPB(object):
    def __init__(self, Ec, Ej, d, N):
        self.Ec = Ec
        self.Ej = Ej
        self.d = d
        self.N = N

        self.flux = 0.
        self.Ng = 0.

        self.H = None
        self.ee = None

    	self.compute_hamiltonian()
    	self.diagonalize()

    def set_flux(self, flux):
    	self.flux = flux
    	self.compute_hamiltonian()
    	self.diagonalize()

    def set_Ng(self, Ng):
    	self.Ng = Ng
    	self.compute_hamiltonian()
    	self.diagonalize()


    def compute_hamiltonian(self):
        dim = 2 * self.N + 1
        Hc = 4 * self.Ec * (num(dim,offset = - self.N)-self.Ng)**2
        Hj = - self.Ej * np.cos(np.pi * self.flux) / 2 * sum((fock(dim,i+1)*fock(dim,i).dag() +\
            fock(dim,i)*fock(dim,i+1).dag() for i in xrange(dim-1)))

        # Asymetric junction
        if self.d != 0.:
            Hj += - 1j * self.d * self.Ej * np.sin(np.pi * self.flux) / 2 * sum(( - fock(dim,i+1)*fock(dim,i).dag() +\
            fock(dim,i)*fock(dim,i+1).dag() for i in xrange(dim-1)))

        self.H =  Hc + Hj


    def diagonalize(self):
    	diag = self.H.eigenstates()
        self.ee = diag[0]
        self.es = [diag[1][i] for i in xrange(len(diag[0]))]


    def f(self,i,f):
        return self.ee[f]-self.ee[i]


    def plot_frequency_Ng(self,Ng_max, flux, points, levels):
        self.flux = flux
        Nglist = np.linspace(-Ng_max,Ng_max,points)
        energies = np.zeros((points,2*self.N+1))    
        i = 0
        for Ng in Nglist:
            self.set_Ng(Ng)
            energies[i,:] = self.ee
            i += 1
        
        for i in xrange(1,levels):
            plt.plot(Nglist, energies[:,i]-energies[:,0])
            
        plt.xlabel('gate charge')
        plt.ylabel('transition frequency (0 to exited states)')
        plt.show()
        
    def plot_frequency_flux(self,Ng, flux_max, points, levels):
        self.Ng = Ng
        fluxlist = np.linspace(-flux_max,flux_max,points)
        energies = np.zeros((points,2*self.N+1))    
        i = 0
        for flux in fluxlist:
            self.set_flux(flux)
            energies[i,:] = self.ee
            i += 1
        
        for i in xrange(1,levels):
            plt.plot(fluxlist, energies[:,i]-energies[:,0])
            
        plt.xlabel('flux')
        plt.ylabel('transition frequency (0 to exited states)')
        plt.show()




class JC(object):
    def __init__(self, g0, fc, N_photons, Ec, Ej, d, N_cpb, rwa = False, second_mode = True, N_photons_second_mode = 3, flux = 0., fc2 = None):   
        self.cpb = CPB(Ec, Ej, d, N_cpb)
        self.fc2 = fc2
        if fc2 == None:
            self.fc2 = np.sqrt(3)*fc
        self.N_photons_second_mode = N_photons_second_mode     
        self.second_mode = second_mode
        self.rwa = rwa
        self.H = None
        self.N_photons = N_photons
        self.fc = fc
        self.g0 = g0 
        self.rabi_flux = 0.
        self.set_g_scaling_factor() 

        self.set_flux(flux)

    def set_g_scaling_factor(self):

        self.g_scaling_factor = 1.

        def to_minimize(flux):
            self.cpb.set_flux(float(flux))
            return abs(self.cpb.f(0,1) - self.fc)

        self.rabi_flux = fmin(to_minimize, 
                  x0 = 0.55, 
                  disp = False)[0]

        self.set_flux(self.rabi_flux)
        self.g_scaling_factor = self.g(0,1) / self.g0

    def compute_hamiltonian(self):
        g = basis(3, 0)
        e = basis(3, 1)
        f = basis(3, 2)
        id_q = qeye(3)

        a = destroy(self.N_photons)
        id_c = qeye(self.N_photons)

        g01 = self.g(0,1)
        g12 = self.g(1,2)

        self.H =    self.fc * tensor(a.dag()*a, id_q) +\
                    self.cpb.f(0,1) * tensor(id_c, e*e.dag()) +\
                    self.cpb.f(0,2) * tensor(id_c, f*f.dag()) +\
                    g01 * (tensor(a.dag(), g*e.dag()) + tensor(a, e*g.dag())) +\
                    g12 * (tensor(a.dag(), e*f.dag()) + tensor(a, f*e.dag()))

        if not self.rwa:
            self.H +=   g01 * (tensor(a, g*e.dag()) + tensor(a.dag(), e*g.dag())) +\
                        g12 * (tensor(a, e*f.dag()) + tensor(a.dag(), f*e.dag()))

        if self.second_mode:
            a2 = destroy(self.N_photons_second_mode)
            id_c2 = qeye(self.N_photons_second_mode)
            sqr3 = np.sqrt(3)

            self.H =    tensor(self.H, id_c2)

            self.H +=   self.fc2 * tensor(id_c, id_q, a2.dag()*a2) +\
                        sqr3*g01 * (tensor(id_c, g*e.dag(), a2.dag()) + tensor(id_c, e*g.dag(), a2)) +\
                        sqr3*g12 * (tensor(id_c, e*f.dag(), a2.dag()) + tensor(id_c, f*e.dag(), a2))

            if not self.rwa:
                self.H +=   sqr3*g01 * (tensor(id_c, g*e.dag(), a2) + tensor(id_c, e*g.dag(), a2.dag())) +\
                            sqr3*g12 * (tensor(id_c, e*f.dag(), a2) + tensor(id_c, f*e.dag(), a2.dag()))


    def diagonalize(self):
        diag = self.H.eigenstates()
        self.ee = diag[0]
        self.es = [diag[1][i].data for i in xrange(len(diag[0]))]

    def set_flux(self,flux):
        self.cpb.set_flux(flux)
        self.compute_hamiltonian()
        self.diagonalize()

    def g(self,i,f):

        init = self.cpb.es[i]
        final = self.cpb.es[f]
        g =  self.g0 * init.dag() * num(2 * self.cpb.N + 1,offset = - self.cpb.N) * final
        g /= self.g_scaling_factor
        return np.absolute(g[0][0][0])

    def cpb_f(self,i,j):
        return self.ee[self.N_photons*j]-self.ee[self.N_photons*i]


    def plot_frequency_flux(self,Ng, flux_max, points, axis):
        self.cpb.Ng = Ng
        fluxlist = np.linspace(-flux_max,flux_max,points)
        energies = np.zeros((points,3*self.N_photons))    
        i = 0
        for flux in fluxlist:
            self.set_flux(flux)
            energies[i,:] = self.ee
            i += 1
        
        for i in xrange(len(energies[0,:])):
            plt.plot(fluxlist, energies[:,i]-energies[:,0])
            
        plt.xlabel('flux')
        plt.ylabel('transition frequency (0 to exited states)')
        plt.axis(axis)
        plt.show()

    def f(self, i, j):
        return self.ee[j]-self.ee[i]