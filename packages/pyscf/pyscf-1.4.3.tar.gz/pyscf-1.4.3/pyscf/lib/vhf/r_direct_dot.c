/*
 *
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
#define DMCOND(i,j)     dm_cond[shls[i]*nbas+shls[j]]

static void get_block(double complex *a, double complex *blk,
                      int n, int istart, int iend, int jstart, int jend)
{
        int i, j, k;
        a = a + istart * n;
        for (i = istart, k = 0; i < iend; i++) {
                for (j = jstart; j < jend; j++, k++) {
                        blk[k] = a[j];
                }
                a += n;
        }
}
static void adbak_block(double complex *a, double complex *blk,
                        int n, int istart, int iend, int jstart, int jend)
{
        int i, j, k;
        a = a + istart * n;
        for (i = istart, k = 0; i < iend; i++) {
                for (j = jstart; j < jend; j++, k++) {
                        a[j] += blk[k];
                }
                a += n;
        }
}
// T = transpose
static void get_blockT(double complex *a, double complex *blk,
                       int n, int istart, int iend, int jstart, int jend)
{
        int i, j, i1, j1;
        int m = iend - istart;
        a = a + istart * n;
        for (i = istart, i1 = 0; i < iend; i++, i1++) {
                for (j = jstart, j1 = 0; j < jend; j++, j1++) {
                        blk[j1*m+i1] = a[j];
                }
                a += n;
        }
}
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

void CVHFrs1_ji_s1kl(double complex *eri,
                     double complex *dm, double complex *vj,
                     int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                     double *dm_cond, int nbas, double dm_atleast)
{
        if (dm_cond && DMCOND(1,0) < dm_atleast) { return; }
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

        get_block(dm, sdm, nao, jstart, jend, istart, iend);
        for (ic = 0; ic < ncomp; ic++) {
                memset(svj, 0, sizeof(double complex)*dkl);
                zgemv_(&TRANST, &dij, &dkl, &Z1, eri, &dij,
                       sdm, &INC1, &Z0, svj, &INC1);
                adbak_blockT(vj, svj, nao, kstart, kend, lstart, lend);
                eri += dij*dkl;
                vj += nao*nao;
        }
}

void CVHFrs1_lk_s1ij(double complex *eri,
                     double complex *dm, double complex *vj,
                     int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                     double *dm_cond, int nbas, double dm_atleast)
{
        if (dm_cond && DMCOND(3,2) < dm_atleast) { return; }
        LOCIJKL;
        int INC1 = 1;
        char TRANSN = 'N';
        int dij = di * dj;
        int dkl = dk * dl;
        double complex Z0 = 0;
        double complex Z1 = 1;
        double complex sdm[dkl];
        double complex svj[dij];
        int ic;

        get_block(dm, sdm, nao, lstart, lend, kstart, kend);
        for (ic = 0; ic < ncomp; ic++) {
                memset(svj, 0, sizeof(double complex)*dij);
                zgemv_(&TRANSN, &dij, &dkl, &Z1, eri, &dij,
                       sdm, &INC1, &Z0, svj, &INC1);
                adbak_blockT(vj, svj, nao, istart, iend, jstart, jend);
                eri += dij*dkl;
                vj += nao*nao;
        }
}

void CVHFrs1_jk_s1il(double complex *eri,
                     double complex *dm, double complex *vk,
                     int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                     double *dm_cond, int nbas, double dm_atleast)
{
        if (dm_cond && DMCOND(1,2) < dm_atleast) { return; }
        LOCIJKL;
        int INC1 = 1;
        char TRANSN = 'N';
        int djk = dk * dj;
        int dil = di * dl;
        int dijk = djk * di;
        double complex Z1 = 1;
        double complex sdm[djk];
        double complex svk[dil];
        int l, ic;

        get_blockT(dm, sdm, nao, jstart, jend, kstart, kend);
        for (ic = 0; ic < ncomp; ic++) {
                memset(svk, 0, sizeof(double complex)*dil);
                for (l = 0; l < dl; l++) {
                        zgemv_(&TRANSN, &di, &djk, &Z1, eri, &di,
                               sdm, &INC1, &Z1, svk+l*di, &INC1);
                        eri += dijk;
                }
                adbak_blockT(vk, svk, nao, istart, iend, lstart, lend);
                vk += nao*nao;
        }
}
void CVHFrs1_li_s1kj(double complex *eri,
                     double complex *dm, double complex *vk,
                     int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                     double *dm_cond, int nbas, double dm_atleast)
{
        if (dm_cond && DMCOND(3,0) < dm_atleast) { return; }
        LOCIJKL;
        int INC1 = 1;
        char TRANST = 'T';
        int djk = dk * dj;
        int dijk = djk * di;
        double complex Z1 = 1;
        double complex svk[djk];
        int l, l0, ic;

        for (ic = 0; ic < ncomp; ic++) {
                memset(svk, 0, sizeof(double complex)*djk);
                for (l = 0, l0 = lstart; l < dl; l++, l0++) {
                        zgemv_(&TRANST, &di, &djk, &Z1, eri, &di,
                               dm+l0*nao+istart, &INC1, &Z1, svk, &INC1);
                        eri += dijk;
                }
                adbak_block(vk, svk, nao, kstart, kend, jstart, jend);
                vk += nao*nao;
        }
}

void CVHFrs2ij_ji_s1kl(double complex *eri,
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
        if (dm_cond && DMCOND(1,0)+DMCOND(0,1) < dm_atleast) { return; }
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

        CVHFtimerev_ijplus(sdm, dm, tao, jstart, jend, istart, iend, nao);
        for (ic = 0; ic < ncomp; ic++) {
                memset(svj, 0, sizeof(double complex)*dkl);
                zgemv_(&TRANST, &dij, &dkl, &Z1, eri, &dij,
                       sdm, &INC1, &Z0, svj, &INC1);
                adbak_blockT(vj, svj, nao, kstart, kend, lstart, lend);
                eri += dij*dkl;
                vj += nao*nao;
        }
}
void CVHFrs2ij_lk_s2ij(double complex *eri,
                       double complex *dm, double complex *vj,
                       int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                       double *dm_cond, int nbas, double dm_atleast)
{
        assert(shls[0] >= shls[1]);
        CVHFrs1_lk_s1ij(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                        dm_cond, nbas, dm_atleast);
}

void CVHFrs2ij_jk_s1il(double complex *eri,
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
        if (dm_cond && DMCOND(0,2) < dm_atleast) { return; }

        LOCIJKL;
        int INC1 = 1;
        char TRANST = 'T';
        int dik = di * dk;
        int djl = dj * dl;
        double complex Z1 = 1;
        double complex sdm[dik];
        double complex svk[djl];
        double complex *p0213 = eri + dik*djl*ncomp;
        int ic;

        CVHFtimerev_iT(sdm, dm, tao, istart, iend, kstart, kend, nao);
        for (ic = 0; ic < ncomp; ic++) {
                memset(svk, 0, sizeof(double complex)*djl);
                zgemv_(&TRANST, &dik, &djl, &Z1, p0213, &dik,
                       sdm, &INC1, &Z1, svk, &INC1);
                CVHFtimerev_adbak_iT(svk, vk, tao, jstart, jend, lstart, lend, nao);
                eri += dik*djl;
                p0213 += dik*djl;
                vk += nao*nao;
        }
}
void CVHFrs2ij_li_s1kj(double complex *eri,
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
        if (dm_cond && DMCOND(3,1) < dm_atleast) { return; }

        LOCIJKL;
        int INC1 = 1;
        char TRANSN = 'N';
        int dik = di * dk;
        int djl = dj * dl;
        double complex Z1 = 1;
        double complex sdm[djl];
        double complex svk[dik];
        double complex *p0213 = eri + dik*djl*ncomp;
        int ic;

        CVHFtimerev_j(sdm, dm, tao, lstart, lend, jstart, jend, nao);
        for (ic = 0; ic < ncomp; ic++) {
                memset(svk, 0, sizeof(double complex)*dik);
                zgemv_(&TRANSN, &dik, &djl, &Z1, p0213, &dik,
                       sdm, &INC1, &Z1, svk, &INC1);
                CVHFtimerev_adbak_j(svk, vk, tao, kstart, kend, istart, iend, nao);
                eri += dik*djl;
                p0213 += dik*djl;
                vk += nao*nao;
        }
}

void CVHFrs2kl_ji_s2kl(double complex *eri,
                       double complex *dm, double complex *vj,
                       int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                       double *dm_cond, int nbas, double dm_atleast)
{
        assert(shls[2] >= shls[3]);
        CVHFrs1_ji_s1kl(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                        dm_cond, nbas, dm_atleast);
}
void CVHFrs2kl_lk_s1ij(double complex *eri,
                       double complex *dm, double complex *vj,
                       int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                       double *dm_cond, int nbas, double dm_atleast)
{
        assert(shls[2] >= shls[3]);
        if (shls[2] == shls[3]) {
                CVHFrs1_lk_s1ij(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                                dm_cond, nbas, dm_atleast);
                return;
        }
        if (dm_cond && DMCOND(2,3)+DMCOND(3,2) < dm_atleast) { return; }

        LOCIJKL;
        int INC1 = 1;
        char TRANSN = 'N';
        int dij = di * dj;
        int dkl = dk * dl;
        double complex Z0 = 0;
        double complex Z1 = 1;
        double complex sdm[dkl];
        double complex svj[dij];
        int ic;

        CVHFtimerev_ijplus(sdm, dm, tao, lstart, lend, kstart, kend, nao);
        for (ic = 0; ic < ncomp; ic++) {
                memset(svj, 0, sizeof(double complex)*dij);
                zgemv_(&TRANSN, &dij, &dkl, &Z1, eri, &dij,
                       sdm, &INC1, &Z0, svj, &INC1);
                adbak_blockT(vj, svj, nao, istart, iend, jstart, jend);
                eri += dij*dkl;
                vj += nao*nao;
        }
}

void CVHFrs2kl_jk_s1il(double complex *eri,
                       double complex *dm, double complex *vk,
                       int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                       double *dm_cond, int nbas, double dm_atleast)
{
        assert(shls[2] >= shls[3]);

        CVHFrs1_jk_s1il(eri, dm, vk, nao, ncomp, shls, ao_loc, tao,
                        dm_cond, nbas, dm_atleast);
        if (shls[2] == shls[3]) {
                return;
        }
        if (dm_cond && DMCOND(1,3) < dm_atleast) { return; }

        LOCIJKL;
        int INC1 = 1;
        char TRANSN = 'N';
        int dik = di * dk;
        int djl = dj * dl;
        double complex Z1 = 1;
        double complex sdm[djl];
        double complex svk[dik];
        double complex *p0213 = eri + dik*djl*ncomp;
        int ic;

        CVHFtimerev_jT(sdm, dm, tao, jstart, jend, lstart, lend, nao);
        for (ic = 0; ic < ncomp; ic++) {
                memset(svk, 0, sizeof(double complex)*dik);
                zgemv_(&TRANSN, &dik, &djl, &Z1, p0213, &dik,
                       sdm, &INC1, &Z1, svk, &INC1);
                CVHFtimerev_adbak_jT(svk, vk, tao, istart, iend, kstart, kend, nao);
                eri += dik*djl;
                p0213 += dik*djl;
                vk += nao*nao;
        }
}
void CVHFrs2kl_li_s1kj(double complex *eri,
                       double complex *dm, double complex *vk,
                       int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                       double *dm_cond, int nbas, double dm_atleast)
{
        assert(shls[2] >= shls[3]);

        CVHFrs1_li_s1kj(eri, dm, vk, nao, ncomp, shls, ao_loc, tao,
                        dm_cond, nbas, dm_atleast);
        if (shls[2] == shls[3]) {
                return;
        }
        if (dm_cond && DMCOND(2,0) < dm_atleast) { return; }

        LOCIJKL;
        int INC1 = 1;
        char TRANST = 'T';
        int dik = di * dk;
        int djl = dj * dl;
        double complex Z1 = 1;
        double complex sdm[dik];
        double complex svk[djl];
        double complex *p0213 = eri + dik*djl*ncomp;
        int ic;

        CVHFtimerev_i(sdm, dm, tao, kstart, kend, istart, iend, nao);
        for (ic = 0; ic < ncomp; ic++) {
                memset(svk, 0, sizeof(double complex)*dl*dj);
                zgemv_(&TRANST, &dik, &djl, &Z1, p0213, &dik,
                       sdm, &INC1, &Z1, svk, &INC1);
                CVHFtimerev_adbak_i(svk, vk, tao, lstart, lend, jstart, jend, nao);
                eri += dik*djl;
                p0213 += dik*djl;
                vk += nao*nao;
        }
}

void CVHFrs4_ji_s2kl(double complex *eri,
                     double complex *dm, double complex *vj,
                     int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                     double *dm_cond, int nbas, double dm_atleast)
{
        assert(shls[0] >= shls[1]);
        assert(shls[2] >= shls[3]);
        CVHFrs2ij_ji_s1kl(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                          dm_cond, nbas, dm_atleast);
}
void CVHFrs4_lk_s2ij(double complex *eri,
                     double complex *dm, double complex *vj,
                     int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                     double *dm_cond, int nbas, double dm_atleast)
{
        assert(shls[0] >= shls[1]);
        assert(shls[2] >= shls[3]);
        CVHFrs2kl_lk_s1ij(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                          dm_cond, nbas, dm_atleast);
}

void CVHFrs4_jk_s1il(double complex *eri,
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
        double complex sdm[n];
        double complex svk[n];
        double complex *peri = eri;
        double complex *pvk = vk;
        double complex *p0213 = eri + dik*djl*ncomp;
        int l, ic;

        // tjtikl
        if (!dm_cond || DMCOND(0,2) > dm_atleast) {
                CVHFtimerev_iT(sdm, dm, tao, istart, iend, kstart, kend, nao);
                for (ic = 0; ic < ncomp; ic++) {
                        memset(svk, 0, sizeof(double complex)*djl);
                        zgemv_(&TRANST, &dik, &djl, &Z1, p0213, &dik,
                               sdm, &INC1, &Z1, svk, &INC1);
                        CVHFtimerev_adbak_iT(svk, pvk, tao, jstart, jend,
                                             lstart, lend, nao);
                        peri += dik*djl;
                        p0213 += dik*djl;
                        pvk += nao*nao;
                }
        }
        if (shls[2] == shls[3]) {
                return;
        }

        // tjtitltk
        if (!dm_cond || DMCOND(0,3) > dm_atleast) {
                CVHFtimerev_blockT(sdm, dm, tao, istart, iend, lstart, lend, nao);
                for (ic = 0; ic < ncomp; ic++) {
                        memset(svk, 0, sizeof(double complex)*djk);
                        for (l = 0; l < dl; l++) {
                                zgemv_(&TRANST, &di, &djk, &Z1, eri, &di,
                                       sdm+l*di, &INC1, &Z1, svk, &INC1);
                                eri += dijk;
                        }
                        CVHFtimerev_adbak_blockT(svk, vk, tao, jstart, jend,
                                                 kstart, kend, nao);
                        vk += nao*nao;
                }
        }
}
// should be identical to CVHFrs4_jk_s1il
void CVHFrs4_li_s1kj(double complex *eri,
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
        double complex sdm[n];
        double complex svk[n];
        double complex *peri = eri;
        double complex *pvk = vk;
        double complex *p0213 = eri + dik*djl*ncomp;
        int l, ic;

        // tjtikl
        if (!dm_cond || DMCOND(3,1) > dm_atleast) {
                CVHFtimerev_j(sdm, dm, tao, lstart, lend, jstart, jend, nao);
                for (ic = 0; ic < ncomp; ic++) {
                        memset(svk, 0, sizeof(double complex)*dik);
                        zgemv_(&TRANSN, &dik, &djl, &Z1, p0213, &dik,
                               sdm, &INC1, &Z1, svk, &INC1);
                        CVHFtimerev_adbak_j(svk, pvk, tao, kstart, kend,
                                            istart, iend, nao);
                        peri += dik*djl;
                        p0213 += dik*djl;
                        pvk += nao*nao;
                }
        }
        if (shls[2] == shls[3]) {
                return;
        }

        // tjtitltk
        if (!dm_cond || DMCOND(2,1) > dm_atleast) {
                CVHFtimerev_block(sdm, dm, tao, kstart, kend, jstart, jend,nao);
                for (ic = 0; ic < ncomp; ic++) {
                        memset(svk, 0, sizeof(double complex)*dil);
                        for (l = 0; l < dl; l++) {
                                zgemv_(&TRANSN, &di, &djk, &Z1, eri, &di,
                                       sdm, &INC1, &Z1, svk+l*di, &INC1);
                                eri += dijk;
                        }
                        CVHFtimerev_adbak_block(svk, vk, tao, lstart, lend,
                                                istart, iend, nao);
                        vk += nao*nao;
                }
        }
}

void CVHFrs8_ji_s2kl(double complex *eri,
                     double complex *dm, double complex *vj,
                     int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                     double *dm_cond, int nbas, double dm_atleast)
{
        CVHFrs4_ji_s2kl(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                        dm_cond, nbas, dm_atleast);
        if ((shls[0] != shls[2]) || (shls[1] != shls[3])) {
                CVHFrs4_lk_s2ij(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                                dm_cond, nbas, dm_atleast);
        }
}
void CVHFrs8_lk_s2ij(double complex *eri,
                     double complex *dm, double complex *vj,
                     int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                     double *dm_cond, int nbas, double dm_atleast)
{
        CVHFrs4_lk_s2ij(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                        dm_cond, nbas, dm_atleast);
        if ((shls[0] != shls[2]) || (shls[1] != shls[3])) {
                CVHFrs4_ji_s2kl(eri, dm, vj, nao, ncomp, shls, ao_loc, tao,
                                dm_cond, nbas, dm_atleast);
        }
}

void CVHFrs8_jk_s1il(double complex *eri,
                     double complex *dm, double complex *vk,
                     int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                     double *dm_cond, int nbas, double dm_atleast)
{
        CVHFrs4_jk_s1il(eri, dm, vk, nao, ncomp, shls, ao_loc, tao,
                        dm_cond, nbas, dm_atleast);
        if ((shls[0] != shls[2]) || (shls[1] != shls[3])) {
                CVHFrs4_li_s1kj(eri, dm, vk, nao, ncomp, shls, ao_loc, tao,
                                dm_cond, nbas, dm_atleast);
        }
}
void CVHFrs8_li_s1kj(double complex *eri,
                     double complex *dm, double complex *vk,
                     int nao, int ncomp, int *shls, int *ao_loc, int *tao,
                     double *dm_cond, int nbas, double dm_atleast)
{
        CVHFrs4_li_s1kj(eri, dm, vk, nao, ncomp, shls, ao_loc, tao,
                        dm_cond, nbas, dm_atleast);
        if ((shls[0] != shls[2]) || (shls[1] != shls[3])) {
                CVHFrs4_jk_s1il(eri, dm, vk, nao, ncomp, shls, ao_loc, tao,
                                dm_cond, nbas, dm_atleast);
        }
}

