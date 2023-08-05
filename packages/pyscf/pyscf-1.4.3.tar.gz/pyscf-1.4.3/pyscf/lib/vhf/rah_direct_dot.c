/*
 * ah in rah4_ ... means anti-hermitian for e1, hermitian for e2
 * ha in rha4_ ... means hermitian for e1, anti-hermitian for e2
 * aa in raa4_ ... means anti-hermitian for e1, anti-hermitian for e2
 */

#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <math.h>
#include <complex.h>
#include "fblas.h"
#include "time_rev.h"
#include "r_direct_dot.h"

#define LOCIJKL \
const int ish = shls[0]; \
const int jsh = shls[1]; \
const int ksh = shls[2]; \
const int lsh = shls[3]; \
const int istart = ao_loc[ish]; \
const int jstart = ao_loc[jsh]; \
const int kstart = ao_loc[ksh]; \
const int lstart = ao_loc[lsh]; \
const int iend = ao_loc[ish+1]; \
const int jend = ao_loc[jsh+1]; \
const int kend = ao_loc[ksh+1]; \
const int lend = ao_loc[lsh+1]; \
const int di = iend - istart; \
const int dj = jend - jstart; \
const int dk = kend - kstart; \
const int dl = lend - lstart;


// T = transpose
static void adbak_blockT(double complex *a, double complex *blk,
                         int n, int istart, int iend, int jstart, int jend)
{
        int i, j, i1, j1;
        int m = iend - istart;
        a = a + istart * n;
        for (i = istart, i1 = 0; i < iend; i++, i1++) {
                for (j = jstart, j1 = 0; j < jend; j++, j1++) {
                        a[j] += blk[j1*m+i1];
                }
                a += n;
        }
}

void CVHFrah1_ji_s1kl(double complex *eri,
                      double complex *dm, double complex *vj,
                      int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                      double *dm_cond, int nbas, double dm_atleast)
{
        CVHFrs1_ji_s1kl(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                        dm_cond, nbas, dm_atleast);
}

void CVHFrah1_lk_s1ij(double complex *eri,
                      double complex *dm, double complex *vj,
                      int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                      double *dm_cond, int nbas, double dm_atleast)
{
        CVHFrs1_lk_s1ij(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                        dm_cond, nbas, dm_atleast);
}

void CVHFrah1_jk_s1il(double complex *eri,
                      double complex *dm, double complex *vk,
                      int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                      double *dm_cond, int nbas, double dm_atleast)
{
        CVHFrs1_jk_s1il(eri, dm, vk, nao, ncomp, shls, ao_loc, tao,
                        dm_cond, nbas, dm_atleast);
}
void CVHFrah1_li_s1kj(double complex *eri,
                      double complex *dm, double complex *vk,
                      int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                      double *dm_cond, int nbas, double dm_atleast)
{
        CVHFrs1_li_s1kj(eri, dm, vk, nao, ncomp, shls, ao_loc, tao,
                        dm_cond, nbas, dm_atleast);
}

void CVHFrah2kl_ji_s2kl(double complex *eri,
                        double complex *dm, double complex *vj,
                        int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                        double *dm_cond, int nbas, double dm_atleast)
{
        CVHFrs2kl_ji_s2kl(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                          dm_cond, nbas, dm_atleast);
}
void CVHFrah2kl_lk_s1ij(double complex *eri,
                        double complex *dm, double complex *vj,
                        int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                        double *dm_cond, int nbas, double dm_atleast)
{
        CVHFrs2kl_lk_s1ij(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                          dm_cond, nbas, dm_atleast);
}

void CVHFrah2kl_jk_s1il(double complex *eri,
                        double complex *dm, double complex *vk,
                        int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                        double *dm_cond, int nbas, double dm_atleast)
{
        CVHFrs2kl_jk_s1il(eri, dm, vk, nao, ncomp, shls, ao_loc, tao,
                          dm_cond, nbas, dm_atleast);
}
void CVHFrah2kl_li_s1kj(double complex *eri,
                        double complex *dm, double complex *vk,
                        int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                        double *dm_cond, int nbas, double dm_atleast)
{
        CVHFrs2kl_li_s1kj(eri, dm, vk, nao, ncomp, shls, ao_loc, tao,
                          dm_cond, nbas, dm_atleast);
}

void CVHFrah2ij_ji_s1kl(double complex *eri,
                        double complex *dm, double complex *vj,
                        int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                        double *dm_cond, int nbas, double dm_atleast)
{
        assert(shls[0] >= shls[1]);
        if (shls[0] == shls[1]) {
                CVHFrs1_ji_s1kl(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                                dm_cond, nbas, dm_atleast);
                return;
        }
        LOCIJKL;
        int INC1 = 1;
        char TRANST = 'T';
        int dij = di * dj;
        int dkl = dk * dl;
        double complex Z0 = 0;
        double complex Z1 = 1;
        double complex sdm[dij];
        double complex svj[dkl];
        int ic;

        CVHFtimerev_ijminus(sdm, dm, tao, jstart, jend, istart, iend, nao);
        for (ic = 0; ic < ncomp; ic++) {
                memset(svj, 0, sizeof(double complex)*dkl);
                zgemv_(&TRANST, &dij, &dkl, &Z1, eri, &dij,
                       sdm, &INC1, &Z0, svj, &INC1);
                adbak_blockT(vj, svj, nao, kstart, kend, lstart, lend);
                eri += dij*dkl;
                vj += nao*nao;
        }
}
void CVHFrah2ij_lk_s2ij(double complex *eri,
                        double complex *dm, double complex *vj,
                        int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                        double *dm_cond, int nbas, double dm_atleast)
{
        assert(shls[0] >= shls[1]);
        CVHFrs1_lk_s1ij(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                        dm_cond, nbas, dm_atleast);
}

void CVHFrah2ij_jk_s1il(double complex *eri,
                        double complex *dm, double complex *vk,
                        int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                        double *dm_cond, int nbas, double dm_atleast)
{
        assert(shls[0] >= shls[1]);

        CVHFrs1_jk_s1il(eri, dm, vk, nao, ncomp, shls, ao_loc, tao,
                        dm_cond, nbas, dm_atleast);
        if (shls[0] == shls[1]) {
                return;
        }

        LOCIJKL;
        int INC1 = 1;
        char TRANST = 'T';
        int dik = di * dk;
        int djl = dj * dl;
        double complex Z1 = 1;
        double complex Z_1 = -1;
        double complex sdm[dik];
        double complex svk[djl];
        double complex *p0213 = eri + dik*djl*ncomp;
        int ic;

        CVHFtimerev_iT(sdm, dm, tao, istart, iend, kstart, kend, nao);

        for (ic = 0; ic < ncomp; ic++) {
                memset(svk, 0, sizeof(double complex)*djl);
                zgemv_(&TRANST, &dik, &djl, &Z_1, p0213, &dik,
                       sdm, &INC1, &Z1, svk, &INC1);
                CVHFtimerev_adbak_iT(svk, vk, tao, jstart, jend, lstart, lend, nao);
                eri += dik*djl;
                p0213 += dik*djl;
                vk += nao*nao;
        }
}
void CVHFrah2ij_li_s1kj(double complex *eri,
                        double complex *dm, double complex *vk,
                        int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                        double *dm_cond, int nbas, double dm_atleast)
{
        assert(shls[0] >= shls[1]);

        CVHFrs1_li_s1kj(eri, dm, vk, nao, ncomp, shls, ao_loc, tao,
                        dm_cond, nbas, dm_atleast);
        if (shls[0] == shls[1]) {
                return;
        }

        LOCIJKL;
        int INC1 = 1;
        char TRANSN = 'N';
        int dik = di * dk;
        int djl = dj * dl;
        double complex Z1 = 1;
        double complex Z_1 = -1;
        double complex sdm[djl];
        double complex svk[dik];
        double complex *p0213 = eri + dik*djl*ncomp;
        int ic;

        CVHFtimerev_j(sdm, dm, tao, lstart, lend, jstart, jend, nao);
        for (ic = 0; ic < ncomp; ic++) {
                memset(svk, 0, sizeof(double complex)*dik);
                zgemv_(&TRANSN, &dik, &djl, &Z_1, p0213, &dik,
                       sdm, &INC1, &Z1, svk, &INC1);
                CVHFtimerev_adbak_j(svk, vk, tao, kstart, kend, istart, iend, nao);
                eri += dik*djl;
                p0213 += dik*djl;
                vk += nao*nao;
        }
}

void CVHFrah4_ji_s2kl(double complex *eri,
                      double complex *dm, double complex *vj,
                      int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                      double *dm_cond, int nbas, double dm_atleast)
{
        assert(shls[0] >= shls[1]);
        assert(shls[2] >= shls[3]);
        CVHFrah2ij_ji_s1kl(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                           dm_cond, nbas, dm_atleast);
}
void CVHFrah4_lk_s2ij(double complex *eri,
                      double complex *dm, double complex *vj,
                      int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                      double *dm_cond, int nbas, double dm_atleast)
{
        assert(shls[0] >= shls[1]);
        assert(shls[2] >= shls[3]);
        CVHFrs2kl_lk_s1ij(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                          dm_cond, nbas, dm_atleast);
}

void CVHFrah4_jk_s1il(double complex *eri,
                      double complex *dm, double complex *vk,
                      int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                      double *dm_cond, int nbas, double dm_atleast)
{
        assert(shls[0] >= shls[1]);
        assert(shls[2] >= shls[3]);

        CVHFrs2kl_jk_s1il(eri, dm, vk, nao, ncomp, shls, ao_loc, tao,
                          dm_cond, nbas, dm_atleast);
        if (shls[0] == shls[1]) {
                return;
        }

        LOCIJKL;
        int INC1 = 1;
        char TRANST = 'T';
        int djk = dj * dk;
        int dik = di * dk;
        int djl = dj * dl;
        int dijk = dik * dj;
        int n = (di+dj)*(dk+dl);
        double complex Z1 = 1;
        double complex Z_1 = -1;
        double complex sdm[n];
        double complex svk[n];
        double complex *peri = eri;
        double complex *pvk = vk;
        double complex *p0213 = eri + dik*djl*ncomp;
        int l, ic;

        // tjtikl
        CVHFtimerev_iT(sdm, dm, tao, istart, iend, kstart, kend, nao);
        for (ic = 0; ic < ncomp; ic++) {
                memset(svk, 0, sizeof(double complex)*djl);
                zgemv_(&TRANST, &dik, &djl, &Z_1, p0213, &dik,
                       sdm, &INC1, &Z1, svk, &INC1);
                CVHFtimerev_adbak_iT(svk, pvk, tao, jstart, jend, lstart, lend, nao);
                peri += dik*djl;
                p0213 += dik*djl;
                pvk += nao*nao;
        }
        if (shls[2] == shls[3]) {
                return;
        }

        // tjtitltk
        CVHFtimerev_blockT(sdm, dm, tao, istart, iend, lstart, lend, nao);
        for (ic = 0; ic < ncomp; ic++) {
                memset(svk, 0, sizeof(double complex)*djk);
                for (l = 0; l < dl; l++) {
                        zgemv_(&TRANST, &di, &djk, &Z_1, eri, &di,
                               sdm+l*di, &INC1, &Z1, svk, &INC1);
                        eri += dijk;
                }
                CVHFtimerev_adbak_blockT(svk, vk, tao, jstart, jend, kstart, kend, nao);
                vk += nao*nao;
        }
}
// should be identical to CVHFrs4_jk_s1il
void CVHFrah4_li_s1kj(double complex *eri,
                      double complex *dm, double complex *vk,
                      int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                      double *dm_cond, int nbas, double dm_atleast)
{
        assert(shls[0] >= shls[1]);
        assert(shls[2] >= shls[3]);

        CVHFrs2kl_li_s1kj(eri, dm, vk, nao, ncomp, shls, ao_loc, tao,
                          dm_cond, nbas, dm_atleast);
        if (shls[0] == shls[1]) {
                return;
        }

        LOCIJKL;
        int INC1 = 1;
        char TRANSN = 'N';
        int dil = di * dl;
        int djk = dj * dk;
        int dik = di * dk;
        int djl = dj * dl;
        int dijk = dik * dj;
        int n = (di+dj)*(dk+dl);
        double complex Z1 = 1;
        double complex Z_1 = -1;
        double complex sdm[n];
        double complex svk[n];
        double complex *peri = eri;
        double complex *pvk = vk;
        double complex *p0213 = eri + dik*djl*ncomp;
        int l, ic;

        // tjtikl
        CVHFtimerev_j(sdm, dm, tao, lstart, lend, jstart, jend, nao);
        for (ic = 0; ic < ncomp; ic++) {
                memset(svk, 0, sizeof(double complex)*dik);
                zgemv_(&TRANSN, &dik, &djl, &Z_1, p0213, &dik,
                       sdm, &INC1, &Z1, svk, &INC1);
                CVHFtimerev_adbak_j(svk, pvk, tao, kstart, kend, istart, iend, nao);
                peri += dik*djl;
                p0213 += dik*djl;
                pvk += nao*nao;
        }
        if (shls[2] == shls[3]) {
                return;
        }

        // tjtitltk
        CVHFtimerev_block(sdm, dm, tao, kstart, kend, jstart, jend, nao);
        for (ic = 0; ic < ncomp; ic++) {
                memset(svk, 0, sizeof(double complex)*dil);
                for (l = 0; l < dl; l++) {
                        zgemv_(&TRANSN, &di, &djk, &Z_1, eri, &di,
                               sdm, &INC1, &Z1, svk+l*di, &INC1);
                        eri += dijk;
                }
                CVHFtimerev_adbak_block(svk, vk, tao, lstart, lend, istart, iend, nao);
                vk += nao*nao;
        }
}


