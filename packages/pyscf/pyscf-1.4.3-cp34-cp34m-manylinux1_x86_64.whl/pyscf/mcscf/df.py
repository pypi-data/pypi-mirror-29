#!/usr/bin/env python
#
# Author: Qiming Sun <osirpt.sun@gmail.com>
#

import sys
import time
import tempfile
import ctypes
from functools import reduce
import numpy
import h5py
from pyscf import lib
from pyscf.lib import logger
from pyscf.ao2mo import _ao2mo
from pyscf import df


def density_fit(casscf, auxbasis=None, with_df=None):
    '''Generate DF-CASSCF for given CASSCF object.  It is done by overwriting
    three CASSCF member functions:
        * casscf.ao2mo which generates MO integrals
        * casscf.get_veff which generate JK from core density matrix
        * casscf.get_jk which

    Args:
        casscf : an CASSCF object

    Kwargs:
        auxbasis : str or basis dict
            Same format to the input attribute mol.basis.  If auxbasis is
            None, auxiliary basis based on AO basis (if possible) or
            even-tempered Gaussian basis will be used.

    Returns:
        An CASSCF object with a modified J, K matrix constructor which uses density
        fitting integrals to compute J and K

    Examples:

    >>> mol = gto.M(atom='H 0 0 0; F 0 0 1', basis='ccpvdz', verbose=0)
    >>> mf = scf.RHF(mol)
    >>> mf.scf()
    >>> mc = DFCASSCF(mf, 4, 4)
    -100.05994191570504
    '''
    casscf_class = casscf.__class__

    if with_df is None:
        if (hasattr(casscf._scf, 'with_df') and
            (auxbasis is None or auxbasis == casscf._scf.with_df.auxbasis)):
            with_df = casscf._scf.with_df
        else:
            with_df = df.DF(casscf.mol)
            with_df.max_memory = casscf.max_memory
            with_df.stdout = casscf.stdout
            with_df.verbose = casscf.verbose
            with_df.auxbasis = auxbasis

    class DFCASSCF(casscf_class, _DFCASSCF):
        def __init__(self):
            self.__dict__.update(casscf.__dict__)
            #self.grad_update_dep = 0
            self.with_df = with_df
            self._keys = self._keys.union(['with_df'])

        def dump_flags(self):
            casscf_class.dump_flags(self)
            logger.info(self, 'DFCASCI/DFCASSCF: density fitting for JK matrix and 2e integral transformation')

        def ao2mo(self, mo_coeff):
            if self.with_df:
                return _ERIS(self, mo_coeff, self.with_df)
            else:
                return casscf_class.ao2mo(self, mo_coeff)

        def get_h2eff(self, mo_coeff=None):  # For CASCI
            if self.with_df:
                if mo_coeff is None:
                    mo_coeff = self.mo_coeff[:,self.ncore:self.ncore+self.ncas]
                elif mo_coeff.shape[1] != self.ncas:
                    mo_coeff = mo_coeff[:,self.ncore:self.ncore+self.ncas]
                return self.with_df.ao2mo(mo_coeff)
            else:
                return casscf_class.get_h2eff(self, mo_coeff)

# Modify get_veff for JK matrix of core density because get_h1eff calls
# self.get_veff to generate core JK
        def get_veff(self, mol=None, dm=None, hermi=1):
            if dm is None:
                mocore = self.mo_coeff[:,:self.ncore]
                dm = numpy.dot(mocore, mocore.T) * 2
            vj, vk = self.get_jk(mol, dm, hermi)
            return vj - vk * .5

# We don't modify self._scf because it changes self.h1eff function.
# We only need approximate jk for self.update_jk_in_ah
        def get_jk(self, mol, dm, hermi=1):
            if self.with_df:
                return self.with_df.get_jk(dm, hermi=hermi)
            else:
                return casscf_class.get_jk(self, mol, dm, hermi)

        def _exact_paaa(self, mo, u, out=None):
            if self.with_df:
                nmo = mo.shape[1]
                ncore = self.ncore
                ncas = self.ncas
                nocc = ncore + ncas
                mo1 = numpy.dot(mo, u)
                mo1_cas = mo1[:,ncore:nocc]
                paaa = self.with_df.ao2mo([mo1, mo1_cas, mo1_cas, mo1_cas], compact=False)
                return paaa.reshape(nmo,ncas,ncas,ncas)
            else:
                return casscf_class._exact_paaa(self, mol, u, out)

    return DFCASSCF()

# A tag to label the derived MCSCF class
class _DFCASSCF:
    pass


def approx_hessian(casscf, auxbasis=None, with_df=None):
    '''Approximate the orbital hessian with density fitting integrals

    Note this function has no effects if the input casscf object is DF-CASSCF.
    It only modifies the orbital hessian of normal CASSCF object.

    Args:
        casscf : an CASSCF object

    Kwargs:
        auxbasis : str or basis dict
            Same format to the input attribute mol.basis.
            The default basis 'weigend+etb' means weigend-coulomb-fit basis
            for light elements and even-tempered basis for heavy elements.

    Returns:
        A CASSCF object with approximated JK contraction for orbital hessian

    Examples:

    >>> mol = gto.M(atom='H 0 0 0; F 0 0 1', basis='ccpvdz', verbose=0)
    >>> mf = scf.RHF(mol)
    >>> mf.scf()
    >>> mc = mcscf.approx_hessian(mcscf.CASSCF(mf, 4, 4))
    -100.06458716530391
    '''
    casscf_class = casscf.__class__

    if 'CASCI' in str(casscf_class):
        return casscf  # because CASCI does not need orbital optimization

    if hasattr(casscf, 'with_df') and casscf.with_df:
        return casscf

    if with_df is None:
        if (getattr(casscf._scf, 'with_df', None) and
            (auxbasis is None or auxbasis == casscf._scf.with_df.auxbasis)):
            with_df = casscf._scf.with_df
        else:
            with_df = df.DF(casscf.mol)
            with_df.max_memory = casscf.max_memory
            with_df.stdout = casscf.stdout
            with_df.verbose = casscf.verbose
            if auxbasis is not None:
                with_df.auxbasis = auxbasis

    class CASSCF(casscf_class):
        def __init__(self):
            self.__dict__.update(casscf.__dict__)
            #self.grad_update_dep = 0
            self.with_df = with_df
            self._keys = self._keys.union(['with_df'])

        def dump_flags(self):
            casscf_class.dump_flags(self)
            logger.info(self, 'CASSCF: density fitting for orbital hessian')

        def ao2mo(self, mo_coeff):
# the exact integral transformation
            eris = casscf_class.ao2mo(self, mo_coeff)

            log = logger.Logger(self.stdout, self.verbose)
# Add the approximate diagonal term for orbital hessian
            t1 = t0 = (time.clock(), time.time())
            mo = numpy.asarray(mo_coeff, order='F')
            nao, nmo = mo.shape
            ncore = self.ncore
            eris.j_pc = numpy.zeros((nmo,ncore))
            k_cp = numpy.zeros((ncore,nmo))
            fmmm = _ao2mo.libao2mo.AO2MOmmm_nr_s2_iltj
            fdrv = _ao2mo.libao2mo.AO2MOnr_e2_drv
            ftrans = _ao2mo.libao2mo.AO2MOtranse2_nr_s2
            bufs1 = numpy.empty((self.with_df.blockdim,nmo,nmo))
            for eri1 in self.with_df.loop():
                naux = eri1.shape[0]
                buf = bufs1[:naux]
                fdrv(ftrans, fmmm,
                     buf.ctypes.data_as(ctypes.c_void_p),
                     eri1.ctypes.data_as(ctypes.c_void_p),
                     mo.ctypes.data_as(ctypes.c_void_p),
                     ctypes.c_int(naux), ctypes.c_int(nao),
                     (ctypes.c_int*4)(0, nmo, 0, nmo),
                     ctypes.c_void_p(0), ctypes.c_int(0))
                bufd = numpy.einsum('kii->ki', buf)
                eris.j_pc += numpy.einsum('ki,kj->ij', bufd, bufd[:,:ncore])
                k_cp += numpy.einsum('kij,kij->ij', buf[:,:ncore], buf[:,:ncore])
                t1 = log.timer_debug1('j_pc and k_pc', *t1)
            eris.k_pc = k_cp.T.copy()
            log.timer('ao2mo density fit part', *t0)
            return eris

        def get_jk(self, mol, dm, hermi=1):
            if self.with_df:
                return self.with_df.get_jk(dm, hermi=hermi)
            else:
                return casscf_class.get_jk(self, mol, dm, hermi)

    return CASSCF()


class _ERIS(object):
    def __init__(self, casscf, mo, with_df):
        import gc
        gc.collect()
        log = logger.Logger(casscf.stdout, casscf.verbose)

        mol = casscf.mol
        nao, nmo = mo.shape
        ncore = casscf.ncore
        ncas = casscf.ncas
        nocc = ncore + ncas
        naoaux = with_df.get_naoaux()

        mem_incore, mem_outcore, mem_basic = _mem_usage(ncore, ncas, nmo)
        mem_now = lib.current_memory()[0]
        max_memory = max(3000, casscf.max_memory*.9-mem_now)
        if max_memory < mem_basic:
            log.warn('Calculation needs %d MB memory, over CASSCF.max_memory (%d MB) limit',
                     (mem_basic+mem_now)/.9, casscf.max_memory)

        t1 = t0 = (time.clock(), time.time())
        self.feri = lib.H5TmpFile()
        self.ppaa = self.feri.create_dataset('ppaa', (nmo,nmo,ncas,ncas), 'f8')
        self.papa = self.feri.create_dataset('papa', (nmo,ncas,nmo,ncas), 'f8')
        self.j_pc = numpy.zeros((nmo,ncore))
        k_cp = numpy.zeros((ncore,nmo))

        mo = numpy.asarray(mo, order='F')
        _tmpfile1 = tempfile.NamedTemporaryFile(dir=lib.param.TMPDIR)
        fxpp = h5py.File(_tmpfile1.name)
        bufpa = numpy.empty((naoaux,nmo,ncas))
        bufs1 = numpy.empty((with_df.blockdim,nmo,nmo))
        fmmm = _ao2mo.libao2mo.AO2MOmmm_nr_s2_iltj
        fdrv = _ao2mo.libao2mo.AO2MOnr_e2_drv
        ftrans = _ao2mo.libao2mo.AO2MOtranse2_nr_s2
        fxpp_keys = []
        b0 = 0
        for k, eri1 in enumerate(with_df.loop()):
            naux = eri1.shape[0]
            bufpp = bufs1[:naux]
            fdrv(ftrans, fmmm,
                 bufpp.ctypes.data_as(ctypes.c_void_p),
                 eri1.ctypes.data_as(ctypes.c_void_p),
                 mo.ctypes.data_as(ctypes.c_void_p),
                 ctypes.c_int(naux), ctypes.c_int(nao),
                 (ctypes.c_int*4)(0, nmo, 0, nmo),
                 ctypes.c_void_p(0), ctypes.c_int(0))
            fxpp_keys.append([str(k), b0, b0+naux])
            fxpp[str(k)] = bufpp.transpose(1,2,0)
            bufpa[b0:b0+naux] = bufpp[:,:,ncore:nocc]
            bufd = numpy.einsum('kii->ki', bufpp)
            self.j_pc += numpy.einsum('ki,kj->ij', bufd, bufd[:,:ncore])
            k_cp += numpy.einsum('kij,kij->ij', bufpp[:,:ncore], bufpp[:,:ncore])
            b0 += naux
            t1 = log.timer_debug1('j_pc and k_pc', *t1)
        self.k_pc = k_cp.T.copy()
        bufs1 = bufpp = None
        t1 = log.timer('density fitting ao2mo pass1', *t0)

        mem_now = lib.current_memory()[0]
        nblk = int(max(8, min(nmo, ((max_memory-mem_now)*1e6/8-bufpa.size)/(ncas**2*nmo))))
        bufs1 = numpy.empty((nblk,ncas,nmo,ncas))
        dgemm = lib.numpy_helper._dgemm
        for p0, p1 in prange(0, nmo, nblk):
            #tmp = numpy.dot(bufpa[:,p0:p1].reshape(naoaux,-1).T,
            #                bufpa.reshape(naoaux,-1))
            tmp = bufs1[:p1-p0]
            dgemm('T', 'N', (p1-p0)*ncas, nmo*ncas, naoaux,
                  bufpa.reshape(naoaux,-1), bufpa.reshape(naoaux,-1),
                  tmp.reshape(-1,nmo*ncas), 1, 0, p0*ncas, 0, 0)
            self.papa[p0:p1] = tmp.reshape(p1-p0,ncas,nmo,ncas)
        bufaa = bufpa[:,ncore:nocc,:].copy().reshape(-1,ncas**2)
        bufs1 = bufpa = None
        t1 = log.timer('density fitting papa pass2', *t1)

        mem_now = lib.current_memory()[0]
        nblk = int(max(8, min(nmo, (max_memory-mem_now)*1e6/8/(nmo*naoaux+ncas**2*nmo))))
        bufs1 = numpy.empty((nblk,nmo,naoaux))
        bufs2 = numpy.empty((nblk,nmo,ncas,ncas))
        for p0, p1 in prange(0, nmo, nblk):
            nrow = p1 - p0
            buf = bufs1[:nrow]
            tmp = bufs2[:nrow].reshape(-1,ncas**2)
            for key, col0, col1 in fxpp_keys:
                buf[:nrow,:,col0:col1] = fxpp[key][p0:p1]
            lib.dot(buf.reshape(-1,naoaux), bufaa, 1, tmp)
            self.ppaa[p0:p1] = tmp.reshape(p1-p0,nmo,ncas,ncas)
        bufs1 = bufs2 = buf = None
        t1 = log.timer('density fitting ppaa pass2', *t1)

        fxpp.close()
        self.feri.flush()

        dm_core = numpy.dot(mo[:,:ncore], mo[:,:ncore].T)
        vj, vk = casscf.get_jk(mol, dm_core)
        self.vhf_c = reduce(numpy.dot, (mo.T, vj*2-vk, mo))
        t0 = log.timer('density fitting ao2mo', *t0)

def _mem_usage(ncore, ncas, nmo):
    nvir = nmo - ncore
    outcore = basic = ncas**2*nmo**2*2 * 8/1e6
    incore = outcore + (ncore+ncas)*nmo**3*4/1e6
    if outcore > 10000:
        sys.stderr.write('Be careful with the virtual memorty address space `ulimit -v`\n')
    return incore, outcore, basic

def prange(start, end, step):
    for i in range(start, end, step):
        yield i, min(i+step, end)


if __name__ == '__main__':
    from pyscf import gto
    from pyscf import scf
    from pyscf import mcscf
    from pyscf.mcscf import addons

    mol = gto.Mole()
    mol.atom = [
        ['O', ( 0., 0.    , 0.   )],
        ['H', ( 0., -0.757, 0.587)],
        ['H', ( 0., 0.757 , 0.587)],]
    mol.basis = {'H': 'cc-pvdz',
                 'O': 'cc-pvdz',}
    mol.build()

    m = scf.RHF(mol)
    ehf = m.scf()
    mc = approx_hessian(mcscf.CASSCF(m, 6, 4))
    mc.verbose = 4
    mo = addons.sort_mo(mc, m.mo_coeff, (3,4,6,7,8,9), 1)
    emc = mc.kernel(mo)[0]
    print(ehf, emc, emc-ehf)
    #-76.0267656731 -76.0873922924 -0.0606266193028
    print(emc - -76.0873923174, emc - -76.0926176464)

    mc = approx_hessian(mcscf.CASSCF(m, 6, (3,1)))
    mc.verbose = 4
    emc = mc.mc2step(mo)[0]
    print(emc - -75.7155632535814)

    mf = scf.density_fit(m)
    mf.kernel()
    #mc = density_fit(mcscf.CASSCF(mf, 6, 4))
    #mc = mcscf.CASSCF(mf, 6, 4)
    mc = mcscf.DFCASSCF(mf, 6, 4)
    mc.verbose = 4
    mo = addons.sort_mo(mc, mc.mo_coeff, (3,4,6,7,8,9), 1)
    emc = mc.kernel(mo)[0]
    print(emc, 'ref = -76.0917567904955', emc - -76.0917567904955)
    mc.with_dep4 = True
    mc.max_cycle_micro = 10
    emc = mc.kernel(mo)[0]
    print(emc, 'ref = -76.0917567904955', emc - -76.0917567904955)

    #mc = density_fit(mcscf.CASCI(mf, 6, 4))
    #mc = mcscf.CASCI(mf, 6, 4)
    mc = mcscf.DFCASCI(mf, 6, 4)
    mo = addons.sort_mo(mc, mc.mo_coeff, (3,4,6,7,8,9), 1)
    emc = mc.kernel(mo)[0]
    print(emc, 'ref = -76.0476686258461', emc - -76.0476686258461)
