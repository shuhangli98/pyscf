#!/usr/bin/env python
#
# Author: Samragni Banerjee <samragnibanerjee4@gmail.com>
#

'''
This example shows the use of periodic EA/IP-ADC with k-point sampling.
Also shown are molecular EA/IP-ADC Gamma-point calculations using a supercell.
'''

import numpy as np
from pyscf.pbc import gto, scf, adc, mp, cc
from pyscf import adc as mol_adc
from pyscf.pbc.tools.pbc import super_cell


cell = gto.Cell()
cell.verbose = 5
cell.unit = 'B'

#
# Helium crystal
#
cell.atom = '''
He 0.000000000000   0.000000000000   0.000000000000
He 1.685068664391   1.685068664391   1.685068664391
'''
cell.basis = [[0, (1., 1.)], [0, (.5, 1.)]]
cell.a = '''
0.000000000, 3.370137329, 3.370137329
3.370137329, 0.000000000, 3.370137329
3.370137329, 3.370137329, 0.000000000
'''
cell.space_group_symmetry = True
cell.build()

nmp = [1,2,2]
nroots_test = 2

# KRHF
kpts = cell.make_kpts(nmp)
kmf = scf.KRHF(cell, kpts=kpts, exxdiv=None).density_fit()
ekrhf = kmf.kernel()

# KADC
kadc  = adc.KRADC(kmf)

#KMP2 energy
emp2, t1, t2 = kadc.kernel_gs()
mypt = mp.KMP2(kmf)
emp2_mp, _ = mypt.kernel()
mycc = cc.KRCCSD(kmf)
mycc.keep_exxdiv = False
emp2_cc, _, _= mycc.kernel()

# None -0.009496847487719144 Init -0.00843504686024058
# Ewald -0.007788753124696426 Init -0.00706010660703776

# kpts = cell.make_kpts(nmp, with_gamma_point=True, space_group_symmetry=True)
# kmf = scf.KRHF(cell, kpts=kpts, exxdiv=None).density_fit()
# ekrhf = kmf.kernel()
# mycc_ksymm = cc.KsymAdaptedRCCSD(kmf)
# emp2_ksymm, _, _= mycc_ksymm.kernel(mbpt2=True)
print("PBC KMP2 Energy:", emp2)
print("PBC KMP2 Energy (from mp):", emp2_mp)
print("PBC KCC Energy (from cc):", emp2_cc)
# print("PBC KMP2 Energy (from ksymm cc):", emp2_ksymm)

#KMP3 energy
kadc.method = 'adc(3)'
emp3, t1, t2 = kadc.kernel_gs()
print("PBC KMP3 Energy:", emp3)

# IP-KRADC
kadc.method_type = 'ip'
kadc.method = 'adc(3)'
k_e_ip, v_e_ip, k_p_ip, k_x_ip = kadc.kernel(nroots_test,kptlist=[0])

# EA-KRADC
kadc.method_type = 'ea'
kadc.method = 'adc(3)'
k_e_ea, v_e_ea, k_p_ea, k_x_ea = kadc.kernel(nroots=nroots_test,kptlist=[0])

# Supercell
scell = super_cell(cell, nmp)

# PBC Gamma-point RHF based on supercell
mf = scf.RHF(scell, exxdiv=None).density_fit()
erhf = mf.kernel()

# Molecular ADC
myadc = mol_adc.RADC(mf)

# Molecular IP-ADC
myadc.method_type = 'ip'
myadc.method = 'adc(3)'
mol_e_ip,mol_v_ip,mol_p_ip,mol_x_ip = myadc.kernel(nroots=nroots_test*np.prod(nmp))

# Molecular EA-ADC
myadc.method_type = 'ea'
myadc.method = 'adc(3)'
mol_e_ea,mol_v_ea,mol_p_ea,mol_x_ea = myadc.kernel(nroots=nroots_test*np.prod(nmp))

print("PBC KRHF Energy:", ekrhf)
print("PBC RHF Energy :", erhf / np.prod(nmp))
print("PBC IP-ADC(3) roots:", k_e_ip)
print("Mol IP-ADC(3) roots:", mol_e_ip)
print("PBC EA-ADC(3) roots:", k_e_ea)
print("Mol EA-ADC(3) roots:", mol_e_ea)
