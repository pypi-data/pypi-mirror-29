/*
 * Author: Qiming Sun <osirpt.sun@gmail.com>
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <complex.h>
#include "config.h"
#include "grid_ao_drv.h"

#define MIN(X,Y)        ((X)<(Y)?(X):(Y))
#define MAX(X,Y)        ((X)>(Y)?(X):(Y))

double exp_cephes(double x);
double CINTcommon_fac_sp(int l);

void GTOnabla1(double *fx1, double *fy1, double *fz1,
               double *fx0, double *fy0, double *fz0, int l, double a)
{
        int i, n;
        double a2 = -2 * a;
        for (n = 0; n < SIMDD; n++) {
                fx1[n] = a2*fx0[SIMDD+n];
                fy1[n] = a2*fy0[SIMDD+n];
                fz1[n] = a2*fz0[SIMDD+n];
        }
        for (i = 1; i <= l; i++) {
        for (n = 0; n < SIMDD; n++) {
                fx1[i*SIMDD+n] = i*fx0[(i-1)*SIMDD+n] + a2*fx0[(i+1)*SIMDD+n];
                fy1[i*SIMDD+n] = i*fy0[(i-1)*SIMDD+n] + a2*fy0[(i+1)*SIMDD+n];
                fz1[i*SIMDD+n] = i*fz0[(i-1)*SIMDD+n] + a2*fz0[(i+1)*SIMDD+n];
        } }
}

/*
 * r - R_O = (r-R_i) + ri, ri = (x,y,z) = R_i - R_O
 */
void GTOx1(double *fx1, double *fy1, double *fz1,
           double *fx0, double *fy0, double *fz0, int l, double *ri)
{
        int i, n;
        for (i = 0; i <= l; i++) {
        for (n = 0; n < SIMDD; n++) {
                fx1[i*SIMDD+n] = ri[0] * fx0[i*SIMDD+n] + fx0[(i+1)*SIMDD+n];
                fy1[i*SIMDD+n] = ri[1] * fy0[i*SIMDD+n] + fy0[(i+1)*SIMDD+n];
                fz1[i*SIMDD+n] = ri[2] * fz0[i*SIMDD+n] + fz0[(i+1)*SIMDD+n];
        } }
}

int GTOprim_exp(double *eprim, double *coord, double *alpha, double *coeff,
                int l, int nprim, int nctr, size_t ngrids, double fac)
{
        int i, j;
        double arr, maxc;
        double logcoeff[nprim];
        double rr[ngrids];
        double *gridx = coord;
        double *gridy = coord+BLKSIZE;
        double *gridz = coord+BLKSIZE*2;
        int not0 = 0;

        // the maximum value of the coefficients for each pGTO
        for (j = 0; j < nprim; j++) {
                maxc = 0;
                for (i = 0; i < nctr; i++) {
                        maxc = MAX(maxc, fabs(coeff[i*nprim+j]));
                }
                logcoeff[j] = log(maxc);
        }

        for (i = 0; i < ngrids; i++) {
                rr[i] = gridx[i]*gridx[i] + gridy[i]*gridy[i] + gridz[i]*gridz[i];
        }

        for (j = 0; j < nprim; j++) {
                for (i = 0; i < ngrids; i++) {
                        arr = alpha[j] * rr[i];
                        if (arr-logcoeff[j] < EXPCUTOFF) {
                                eprim[j*BLKSIZE+i] = exp_cephes(-arr) * fac;
                                not0 = 1;
                        } else {
                                eprim[j*BLKSIZE+i] = 0;
                        }
                }
        }
        return not0;
}


// grid2atm[atm_id,xyz,grid_id]
static void _fill_grid2atm(double *grid2atm, double *coord, size_t bgrids, size_t ngrids,
                           int *atm, int natm, int *bas, int nbas, double *env)
{
        int atm_id;
        size_t ig;
        double *r_atm;
        for (atm_id = 0; atm_id < natm; atm_id++) {
                r_atm = env + atm[PTR_COORD+atm_id*ATM_SLOTS];
                for (ig = 0; ig < bgrids; ig++) {
                        grid2atm[0*BLKSIZE+ig] = coord[0*ngrids+ig] - r_atm[0];
                        grid2atm[1*BLKSIZE+ig] = coord[1*ngrids+ig] - r_atm[1];
                        grid2atm[2*BLKSIZE+ig] = coord[2*ngrids+ig] - r_atm[2];
                }
                grid2atm += 3*BLKSIZE;
        }
}


static void _dset0(double *out, size_t odim, size_t bgrids, int counts)
{
        size_t i, j;
        for (i = 0; i < counts; i++) {
                for (j = 0; j < bgrids; j++) {
                        out[i*odim+j] = 0;
                }
        }
}

static void _zset0(double complex *out, size_t odim, size_t bgrids, int counts)
{
        size_t i, j;
        for (i = 0; i < counts; i++) {
                for (j = 0; j < bgrids; j++) {
                        out[i*odim+j] = 0;
                }
        }
}

void GTOeval_sph_iter(FPtr_eval feval,  FPtr_exp fexp, double fac,
                      size_t nao, size_t ngrids, size_t bgrids,
                      int param[], int *shls_slice, int *ao_loc, double *buf,
                      double *ao, double *coord, char *non0table,
                      int *atm, int natm, int *bas, int nbas, double *env)
{
        const int ncomp = param[TENSOR];
        const int sh0 = shls_slice[0];
        const int sh1 = shls_slice[1];
        const int atmstart = bas[sh0*BAS_SLOTS+ATOM_OF];
        const int atmend = bas[(sh1-1)*BAS_SLOTS+ATOM_OF]+1;
        const int atmcount = atmend - atmstart;
        int i, k, l, np, nc, atm_id, bas_id, deg, dcart, ao_id;
        size_t di;
        double fac1;
        double *p_exp, *pcoeff, *pcoord, *pcart, *ri, *pao;
        double *grid2atm = buf; // [atm_id,xyz,grid]
        double *eprim = grid2atm + atmcount*3*BLKSIZE;
        double *cart_gto = eprim + NPRIMAX*BLKSIZE*2;

        _fill_grid2atm(grid2atm, coord, bgrids, ngrids,
                       atm+atmstart*ATM_SLOTS, atmcount, bas, nbas, env);

        for (bas_id = sh0; bas_id < sh1; bas_id++) {
                np = bas[bas_id*BAS_SLOTS+NPRIM_OF];
                nc = bas[bas_id*BAS_SLOTS+NCTR_OF ];
                l  = bas[bas_id*BAS_SLOTS+ANG_OF  ];
                deg = l * 2 + 1;
                fac1 = fac * CINTcommon_fac_sp(l);
                p_exp  = env + bas[bas_id*BAS_SLOTS+PTR_EXP];
                pcoeff = env + bas[bas_id*BAS_SLOTS+PTR_COEFF];
                atm_id = bas[bas_id*BAS_SLOTS+ATOM_OF];
                pcoord = grid2atm + (atm_id - atmstart) * 3*BLKSIZE;
                ao_id = ao_loc[bas_id] - ao_loc[sh0];
                if (non0table[bas_id] &&
                    (*fexp)(eprim, pcoord, p_exp, pcoeff, l, np, nc, bgrids, fac1)) {
                        dcart = (l+1)*(l+2)/2;
                        di = nc * dcart;
                        ri = env + atm[PTR_COORD+atm_id*ATM_SLOTS];
                        if (l <= 1) { // s, p functions
                                (*feval)(ao+ao_id*ngrids, ri, eprim, pcoord, p_exp, pcoeff,
                                         env, l, np, nc, nao, ngrids, bgrids);
                        } else {
                                (*feval)(cart_gto, ri, eprim, pcoord, p_exp, pcoeff,
                                         env, l, np, nc, di, bgrids, bgrids);
                                pcart = cart_gto;
                                for (i = 0; i < ncomp; i++) {
                                        pao = ao + (i*nao+ao_id)*ngrids;
                                        for (k = 0; k < nc; k++) {
                                                CINTc2s_ket_sph1(pao, pcart,
                                                                 ngrids, bgrids, l);
                                                pao += deg * ngrids;
                                                pcart += dcart * bgrids;
                                        }
                                }
                        }
                } else {
                        for (i = 0; i < ncomp; i++) {
                                _dset0(ao+(i*nao+ao_id)*ngrids, ngrids, bgrids, nc*deg);
                        }
                }
        }
}

void GTOeval_cart_iter(FPtr_eval feval,  FPtr_exp fexp, double fac,
                       size_t nao, size_t ngrids, size_t bgrids,
                       int param[], int *shls_slice, int *ao_loc, double *buf,
                       double *ao, double *coord, char *non0table,
                       int *atm, int natm, int *bas, int nbas, double *env)
{
        const int ncomp = param[TENSOR];
        const int sh0 = shls_slice[0];
        const int sh1 = shls_slice[1];
        const int atmstart = bas[sh0*BAS_SLOTS+ATOM_OF];
        const int atmend = bas[(sh1-1)*BAS_SLOTS+ATOM_OF]+1;
        const int atmcount = atmend - atmstart;
        int i, k, l, np, nc, atm_id, bas_id, deg, ao_id;
        double fac1;
        double *p_exp, *pcoeff, *pcoord, *pcart, *ri, *pao;
        double *grid2atm = buf; // [atm_id,xyz,grid]
        double *eprim = grid2atm + atmcount*3*BLKSIZE;

        _fill_grid2atm(grid2atm, coord, bgrids, ngrids,
                       atm+atmstart*ATM_SLOTS, atmcount, bas, nbas, env);

        for (bas_id = sh0; bas_id < sh1; bas_id++) {
                np = bas[bas_id*BAS_SLOTS+NPRIM_OF];
                nc = bas[bas_id*BAS_SLOTS+NCTR_OF ];
                l  = bas[bas_id*BAS_SLOTS+ANG_OF  ];
                deg = (l+1)*(l+2)/2;
                fac1 = fac * CINTcommon_fac_sp(l);
                p_exp  = env + bas[bas_id*BAS_SLOTS+PTR_EXP];
                pcoeff = env + bas[bas_id*BAS_SLOTS+PTR_COEFF];
                atm_id = bas[bas_id*BAS_SLOTS+ATOM_OF];
                pcoord = grid2atm + (atm_id - atmstart) * 3*BLKSIZE;
                ao_id = ao_loc[bas_id] - ao_loc[sh0];
                if (non0table[bas_id] &&
                    (*fexp)(eprim, pcoord, p_exp, pcoeff, l, np, nc, bgrids, fac1)) {
                        ri = env + atm[PTR_COORD+atm_id*ATM_SLOTS];
                        (*feval)(ao+ao_id*ngrids, ri, eprim, pcoord, p_exp, pcoeff,
                                 env, l, np, nc, nao, ngrids, bgrids);
                } else {
                        for (i = 0; i < ncomp; i++) {
                                _dset0(ao+(i*nao+ao_id)*ngrids, ngrids, bgrids, nc*deg);
                        }
                }
        }
}

void GTOeval_spinor_iter(FPtr_eval feval, FPtr_exp fexp, void (*c2s)(), double fac,
                         size_t nao, size_t ngrids, size_t bgrids,
                         int param[], int *shls_slice, int *ao_loc, double *buf,
                         double complex *ao, double *coord, char *non0table,
                         int *atm, int natm, int *bas, int nbas, double *env)
{
        const int ncomp_e1 = param[POS_E1];
        const int ncomp = param[TENSOR];
        const int sh0 = shls_slice[0];
        const int sh1 = shls_slice[1];
        const int atmstart = bas[sh0*BAS_SLOTS+ATOM_OF];
        const int atmend = bas[(sh1-1)*BAS_SLOTS+ATOM_OF]+1;
        const int atmcount = atmend - atmstart;
        int i, k, l, np, nc, atm_id, bas_id, deg, kappa, dcart, ao_id;
        size_t off, di;
        double fac1;
        double *p_exp, *pcoeff, *pcoord, *pcart, *ri;
        double complex *aoa = ao;
        double complex *aob = ao + ncomp*nao*ngrids;
        double *grid2atm = buf; // [atm_id,xyz,grid]
        double *eprim = grid2atm + atmcount*3*BLKSIZE;
        double *cart_gto = eprim + NPRIMAX*BLKSIZE*2;

        _fill_grid2atm(grid2atm, coord, bgrids, ngrids,
                       atm+atmstart*ATM_SLOTS, atmcount, bas, nbas, env);

        for (bas_id = sh0; bas_id < sh1; bas_id++) {
                np = bas[bas_id*BAS_SLOTS+NPRIM_OF];
                nc = bas[bas_id*BAS_SLOTS+NCTR_OF ];
                l  = bas[bas_id*BAS_SLOTS+ANG_OF  ];
                deg = CINTlen_spinor(bas_id, bas);
                fac1 = fac * CINTcommon_fac_sp(l);
                p_exp  = env + bas[bas_id*BAS_SLOTS+PTR_EXP];
                pcoeff = env + bas[bas_id*BAS_SLOTS+PTR_COEFF];
                atm_id = bas[bas_id*BAS_SLOTS+ATOM_OF];
                pcoord = grid2atm + (atm_id - atmstart) * 3*BLKSIZE;
                ao_id = ao_loc[bas_id] - ao_loc[sh0];
                if (non0table[bas_id] &&
                    (*fexp)(eprim, pcoord, p_exp, pcoeff, l, np, nc, bgrids, fac1)) {
                        kappa = bas[bas_id*BAS_SLOTS+KAPPA_OF];
                        dcart = (l+1)*(l+2)/2;
                        di = nc * dcart;
                        ri = env + atm[PTR_COORD+atm_id*ATM_SLOTS];
                        (*feval)(cart_gto, ri, eprim, pcoord, p_exp, pcoeff,
                                 env, l, np, nc, di, bgrids, bgrids);
                        for (i = 0; i < ncomp; i++) {
                                pcart = cart_gto + i * di*bgrids*ncomp_e1;
                                off = (i*nao+ao_id)*ngrids;
                                (*c2s)(aoa+off, aob+off, pcart,
                                       ngrids, bgrids, nc, kappa, l);
                        }
                } else {
                        for (i = 0; i < ncomp; i++) {
                                off = (i*nao+ao_id)*ngrids;
                                _zset0(aoa+off, ngrids, bgrids, nc*deg);
                                _zset0(aob+off, ngrids, bgrids, nc*deg);
                        }
                }
        }
}

int GTOshloc_by_atom(int *shloc, int *shls_slice, int *ao_loc, int *atm, int *bas)
{
        const int sh0 = shls_slice[0];
        const int sh1 = shls_slice[1];
        int ish, nshblk, lastatm;
        shloc[0] = sh0;
        nshblk = 1;
        lastatm = bas[BAS_SLOTS*sh0+ATOM_OF];
        for (ish = sh0; ish < sh1; ish++) {
                if (lastatm != bas[BAS_SLOTS*ish+ATOM_OF]) {
                        lastatm = bas[BAS_SLOTS*ish+ATOM_OF];
                        shloc[nshblk] = ish;
                        nshblk++;
                }
        }
        shloc[nshblk] = sh1;
        return nshblk;
}

/*
 * non0table[ngrids/blksize,natm] is the T/F table for ao values to
 * screen the ao evaluation for each shell
 */
void GTOeval_loop(void (*fiter)(), FPtr_eval feval, FPtr_exp fexp, double fac,
                  int ngrids, int param[], int *shls_slice, int *ao_loc,
                  double *ao, double *coord, char *non0table,
                  int *atm, int natm, int *bas, int nbas, double *env)
{
        int shloc[shls_slice[1]-shls_slice[0]+1];
        const int nshblk = GTOshloc_by_atom(shloc, shls_slice, ao_loc, atm, bas);
        const int nblk = (ngrids+BLKSIZE-1) / BLKSIZE;
        const size_t Ngrids = ngrids;

#pragma omp parallel default(none) \
        shared(fiter, feval, fexp, fac, param, ao_loc, shls_slice, ngrids, \
               ao, coord, non0table, atm, natm, bas, nbas, env, shloc)
{
        const int sh0 = shls_slice[0];
        const int sh1 = shls_slice[1];
        const size_t nao = ao_loc[sh1] - ao_loc[sh0];
        int ip, ib, k, iloc, ish;
        size_t aoff, bgrids;
        int ncart = NCTR_CART * param[TENSOR] * param[POS_E1];
        double *buf = malloc(sizeof(double) * BLKSIZE*(NPRIMAX*2+ncart));
#pragma omp for schedule(static)
        for (k = 0; k < nblk*nshblk; k++) {
                iloc = k / nblk;
                ish = shloc[iloc];
                aoff = ao_loc[ish] - ao_loc[sh0];
                ib = k - iloc * nblk;
                ip = ib * BLKSIZE;
                bgrids = MIN(ngrids-ip, BLKSIZE);
                (*fiter)(feval, fexp, fac, nao, Ngrids, bgrids,
                         param, shloc+iloc, ao_loc, buf, ao+aoff*Ngrids+ip,
                         coord+ip, non0table+ib*nbas,
                         atm, natm, bas, nbas, env);
        }
        free(buf);
}
}

void GTOeval_sph_drv(FPtr_eval feval, FPtr_exp fexp, double fac, int ngrids,
                     int param[], int *shls_slice, int *ao_loc,
                     double *ao, double *coord, char *non0table,
                     int *atm, int natm, int *bas, int nbas, double *env)
{
        GTOeval_loop(GTOeval_sph_iter, feval, fexp, fac, ngrids,
                     param, shls_slice, ao_loc,
                     ao, coord, non0table, atm, natm, bas, nbas, env);
}

void GTOeval_cart_drv(FPtr_eval feval, FPtr_exp fexp, double fac, int ngrids,
                      int param[], int *shls_slice, int *ao_loc,
                      double *ao, double *coord, char *non0table,
                      int *atm, int natm, int *bas, int nbas, double *env)
{
        GTOeval_loop(GTOeval_cart_iter, feval, fexp, fac, ngrids,
                     param, shls_slice, ao_loc,
                     ao, coord, non0table, atm, natm, bas, nbas, env);
}

void GTOeval_spinor_drv(FPtr_eval feval, FPtr_exp fexp, void (*c2s)(), double fac,
                        int ngrids, int param[], int *shls_slice, int *ao_loc,
                        double complex *ao, double *coord, char *non0table,
                        int *atm, int natm, int *bas, int nbas, double *env)
{
        int shloc[shls_slice[1]-shls_slice[0]+1];
        const int nshblk = GTOshloc_by_atom(shloc, shls_slice, ao_loc, atm, bas);
        const int nblk = (ngrids+BLKSIZE-1) / BLKSIZE;
        const size_t Ngrids = ngrids;

#pragma omp parallel default(none) \
        shared(feval, fexp, c2s, fac, ngrids, param, ao_loc, shls_slice, \
               ao, coord, non0table, atm, natm, bas, nbas, env, shloc)
{
        const int sh0 = shls_slice[0];
        const int sh1 = shls_slice[1];
        const size_t nao = ao_loc[sh1] - ao_loc[sh0];
        int ip, ib, k, iloc, ish;
        size_t aoff, bgrids;
        int ncart = NCTR_CART * param[TENSOR] * param[POS_E1];
        double *buf = malloc(sizeof(double) * BLKSIZE*(NPRIMAX*2+ncart));
#pragma omp for schedule(static)
        for (k = 0; k < nblk*nshblk; k++) {
                iloc = k / nblk;
                ish = shloc[iloc];
                aoff = ao_loc[ish] - ao_loc[sh0];
                ib = k - iloc * nblk;
                ip = ib * BLKSIZE;
                bgrids = MIN(ngrids-ip, BLKSIZE);
                GTOeval_spinor_iter(feval, fexp, c2s, fac,
                                    nao, Ngrids, bgrids,
                                    param, shloc+iloc, ao_loc, buf, ao+aoff*Ngrids+ip,
                                    coord+ip, non0table+ib*nbas,
                                    atm, natm, bas, nbas, env);
        }
        free(buf);
}
}

