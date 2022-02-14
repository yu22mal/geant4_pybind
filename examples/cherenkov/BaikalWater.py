#
# Author: D.V.Naumov, dnaumov@jinr.ru
#
from __future__ import print_function
import numpy as np
import scipy.special as sp
from scipy import optimize
MeV=1
GeV=1000*MeV
keV=0.001*MeV
MeVcm = 1e11/1.97
fm = 1/(197*MeV)

class BaikalWater():
    def __init__(self):
        self.cs_scattering = np.array([20.,15.,7.8,5.8,3.6,2.0,0.83,0.43,0.16,0.121,0.074,0.0536,0.03,0.02,0.015,0.009,0.0079,0.0063,0.005,0.004,
         0.0028,0.0024,0.0018,0.0014,0.0012,0.001,9.3E-4,7.9E-4,6.3E-4,6.E-4])

        self.cs_scattering_norm = self.cs_scattering/np.sum(self.cs_scattering)
        self.cosines = np.array([
         1.,0.99996,0.99985,0.99966,0.99939,0.99905,0.99756,0.99452,0.98481,0.98,0.97,
         0.96,0.94,0.92,0.9,0.86,0.82,0.78,0.74,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.,-0.2,-0.6,-1.])

        self.absorption_inv_length = 1e2*np.array([
         3.14E-3,2.78E-3,2.42E-3,2.08E-3,1.75E-3,1.41E-3,1.21E-3,1.00E-3,9.2E-4,8.4E-4,7.6E-4,6.7E-4,5.9E-4,5.0E-4,4.2E-4,
         4.6E-4,4.9E-4,5.3E-4,5.8E-4,6.2E-4,6.7E-4,8.4E-4,1.02E-3,1.19E-3,1.36E-3,1.76E-3])

        self.scattering_inv_length = 1e2*np.array([
         0.00038,0.00037,0.00036,0.00035,0.00034,.00033,0.000315,0.00030,0.00026,0.00022,0.00019,0.00016,0.000156,
         0.000146,0.00014,0.00014,0.00014,0.00014,0.00014,0.00014,0.00014,0.000143,0.000147,.00015,0.000155,0.00016])

        self.wavelength = np.linspace(350,350+10*26,num=26)
        self.build_refraction_index()


    def print_pars(self):
        print("scattering cross-section (not normalized)")
        print(self.cs_scattering)
        print("scattering cross-section ( normalized)")
        print(self.cs_scattering_norm)
        print("with norm {0:4.3}".format(np.sum(self.cs_scattering_norm)))
        print("cosines")
        print(self.cosines)
        print("wavelength, in nm")
        print(self.wavelength)
        print("inverse absorbtion length, in 1/m")
        print(self.absorption_inv_length)
        print("inverse scattering length, in 1/m")
        print(self.scattering_inv_length)
        print("phase refraction index")
        print(self.phase_refraction_index)
        print("group refraction index")
        print(self.group_refraction_index)

    def build_refraction_index(self):
        self.coeff = np.array([1.9672,-0.59931E-2,0.24515E-4,-0.54076E-7,
                               0.66727E-10,-0.43317E-13,0.11502E-16])

        wl = self.wavelength

        self.phase_refraction_index = np.zeros(26)+0.002
        self.group_refraction_index = np.zeros(26)+0.002

        for m in range(7):
            self.phase_refraction_index+=self.coeff[m]*wl**m
            self.group_refraction_index+=self.coeff[m]*(1-m)*wl**m


        self.refraction_index_0 = np.ones(26)*self.coeff[0]
        self.refraction_index_1 = self.coeff[1]*wl*0
        self.refraction_index_2 = self.coeff[2]*wl**2*(-1)
        self.refraction_index_3 = self.coeff[3]*wl**3*(-2)
        self.refraction_index_4 = self.coeff[4]*wl**4*(-3)
        self.refraction_index_5 = self.coeff[5]*wl**5*(-4)
        self.refraction_index_6 = self.coeff[6]*wl**6*(-5)
        '''
        print(self.refraction_index_0)
        print(self.refraction_index_1)
        print(self.refraction_index_2)
        print(self.refraction_index_3)
        print(self.refraction_index_4)
        print(self.refraction_index_5)
        print(self.refraction_index_6)
        '''

    def print_for_geant4(self, array_to_print, unit=""):
    	if unit != "":
            unit = "*"+unit
    	print("{", end="")
    	for value in array_to_print: print("{0}{1}, ".format(value, unit), end="")
    	print("\b\b};")

    def convert_for_geant4(self):
    	self.energy_g4 = np.flip(1239.84193/self.wavelength)
    	self.absorption_length_g4 = np.flip(1./self.absorption_inv_length)
    	self.scattering_length_g4 = np.flip(1./self.scattering_inv_length)
    	self.refraction_index_g4 = np.flip(self.phase_refraction_index)
    	print("\n Energy (eV):  ", end="")
    	self.print_for_geant4(self.energy_g4, unit="eV")
    	print("\n Absorption length (m):  ", end="")
    	self.print_for_geant4(self.absorption_length_g4, unit="m")
    	print("\n Scattering length (m):  ", end="")
    	self.print_for_geant4(self.scattering_length_g4, unit="m")
    	print("\n Phase refraction index:  ", end="")
    	self.print_for_geant4(self.refraction_index_g4)

    def make_plots(self,cos=0,lengths=0,index=0,terms=0):
        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(12, 8))
        plt.subplots_adjust(hspace=0.4)
        if cos:
            plt.subplot(221)
            plt.semilogy(self.cosines,self.cs_scattering_norm)
            plt.grid(True)
            plt.title('Scattering probability vs cosine (normalized to one)')
            plt.gca().set_xlabel(r'$\cos\theta$')
            plt.gca().set_ylabel(r'Scattering probability')

        if lengths:
            plt.subplot(222)
            plt.plot(self.wavelength,1/self.absorption_inv_length,label='absorb')
            plt.plot(self.wavelength,1/self.scattering_inv_length,label='scatter')
            plt.title('Absorption and scattering  lengths')
            plt.gca().set_xlabel(r'$\lambda$, nm')
            plt.gca().set_ylabel(r'Interaction Length, $m$')
            plt.legend(loc='upper left')

        if index:
            plt.subplot(223)
            plt.plot(self.wavelength,self.phase_refraction_index,label='phase refraction')
            plt.plot(self.wavelength,self.group_refraction_index,label='group refraction')
            plt.title('Refraction index')
            plt.gca().set_xlabel(r'$\lambda$, nm')
            plt.gca().set_ylabel(r'n')
            plt.legend(loc='upper right')

        if terms:
            plt.subplot(224)
            plt.plot(self.wavelength,self.refraction_index_0,label=r'$C(0)$')
            plt.plot(self.wavelength,self.refraction_index_1,label=r'$C(1)\cdot \lambda$')
            plt.plot(self.wavelength,self.refraction_index_2,label=r'$C(2)\cdot \lambda^2$')
            plt.plot(self.wavelength,self.refraction_index_3,label=r'$C(3)\cdot \lambda^3$')
            plt.plot(self.wavelength,self.refraction_index_4,label=r'$C(4)\cdot \lambda^4$')
            plt.plot(self.wavelength,self.refraction_index_5,label=r'$C(5)\cdot \lambda^5$')
            plt.plot(self.wavelength,self.refraction_index_5,label=r'$C(6)\cdot \lambda^6$')
            plt.title('Each term contribution to the refraction index')
            plt.gca().set_xlabel(r'$\lambda$, nm')
            plt.gca().set_ylabel(r'n')
            plt.legend(loc='upper right')

        fig.savefig("water_optics.pdf", bbox_inches='tight')
        fig.savefig("water_optics.png", bbox_inches='tight', dpi=300)

        plt.show()

def main():
    b = BaikalWater()
    #b.print_pars()
    b.convert_for_geant4()
    b.make_plots(cos=1,lengths=1)


if __name__ == "__main__":
    main()
