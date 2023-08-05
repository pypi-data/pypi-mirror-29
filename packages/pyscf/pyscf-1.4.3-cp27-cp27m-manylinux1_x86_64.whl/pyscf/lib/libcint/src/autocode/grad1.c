/*
 * Copyright (C) 2013-  Qiming Sun <osirpt.sun@gmail.com>
 * Description: code generated by  gen-code.cl
 */
#include <stdlib.h>
#include "cint_bas.h"
#include "cart2sph.h"
#include "g1e.h"
#include "g2e.h"
#include "optimizer.h"
#include "cint1e.h"
#include "cint2e.h"
#include "misc.h"
#include "c2f.h"
/* <NABLA i|OVLP |j> */
static void CINTgout1e_int1e_ipovlp(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int ix, iy, iz, n;
double *g0 = g;
double *g1 = g0  + envs->g_size * 3;
double s[3];
G1E_D_I(g1, g0, envs->i_l+0, envs->j_l, 0);
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
s[0] = + g1[ix+0]*g0[iy+0]*g0[iz+0];
s[1] = + g0[ix+0]*g1[iy+0]*g0[iz+0];
s[2] = + g0[ix+0]*g0[iy+0]*g1[iz+0];
gout[n*3+0] += + s[0];
gout[n*3+1] += + s[1];
gout[n*3+2] += + s[2];
}}
void int1e_ipovlp_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {1, 0, 0, 0, 1, 1, 1, 3};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_ipovlp_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 0, 1, 1, 1, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipovlp;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 0);
} // int1e_ipovlp_cart
int int1e_ipovlp_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 0, 1, 1, 1, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipovlp;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 0);
} // int1e_ipovlp_sph
int int1e_ipovlp_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 0, 1, 1, 1, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipovlp;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_sf_1e, 0);
} // int1e_ipovlp_spinor
ALL_CINT1E(int1e_ipovlp)
ALL_CINT1E_FORTRAN_(int1e_ipovlp)
/* <NABLA i|OVLP |P DOT P j> */
static void CINTgout1e_int1e_ipkin(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int ix, iy, iz, n;
double *g0 = g;
double *g1 = g0  + envs->g_size * 3;
double *g2 = g1  + envs->g_size * 3;
double *g3 = g2  + envs->g_size * 3;
double *g4 = g3  + envs->g_size * 3;
double *g5 = g4  + envs->g_size * 3;
double *g6 = g5  + envs->g_size * 3;
double *g7 = g6  + envs->g_size * 3;
double s[27];
G1E_D_J(g1, g0, envs->i_l+1, envs->j_l+0, 0);
G1E_D_J(g2, g0, envs->i_l+1, envs->j_l+1, 0);
G1E_D_J(g3, g2, envs->i_l+1, envs->j_l+0, 0);
G1E_D_I(g4, g0, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g5, g1, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g6, g2, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g7, g3, envs->i_l+0, envs->j_l, 0);
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
s[0] = + g7[ix+0]*g0[iy+0]*g0[iz+0];
s[1] = + g6[ix+0]*g1[iy+0]*g0[iz+0];
s[2] = + g6[ix+0]*g0[iy+0]*g1[iz+0];
s[3] = + g5[ix+0]*g2[iy+0]*g0[iz+0];
s[4] = + g4[ix+0]*g3[iy+0]*g0[iz+0];
s[5] = + g4[ix+0]*g2[iy+0]*g1[iz+0];
s[6] = + g5[ix+0]*g0[iy+0]*g2[iz+0];
s[7] = + g4[ix+0]*g1[iy+0]*g2[iz+0];
s[8] = + g4[ix+0]*g0[iy+0]*g3[iz+0];
s[9] = + g3[ix+0]*g4[iy+0]*g0[iz+0];
s[10] = + g2[ix+0]*g5[iy+0]*g0[iz+0];
s[11] = + g2[ix+0]*g4[iy+0]*g1[iz+0];
s[12] = + g1[ix+0]*g6[iy+0]*g0[iz+0];
s[13] = + g0[ix+0]*g7[iy+0]*g0[iz+0];
s[14] = + g0[ix+0]*g6[iy+0]*g1[iz+0];
s[15] = + g1[ix+0]*g4[iy+0]*g2[iz+0];
s[16] = + g0[ix+0]*g5[iy+0]*g2[iz+0];
s[17] = + g0[ix+0]*g4[iy+0]*g3[iz+0];
s[18] = + g3[ix+0]*g0[iy+0]*g4[iz+0];
s[19] = + g2[ix+0]*g1[iy+0]*g4[iz+0];
s[20] = + g2[ix+0]*g0[iy+0]*g5[iz+0];
s[21] = + g1[ix+0]*g2[iy+0]*g4[iz+0];
s[22] = + g0[ix+0]*g3[iy+0]*g4[iz+0];
s[23] = + g0[ix+0]*g2[iy+0]*g5[iz+0];
s[24] = + g1[ix+0]*g0[iy+0]*g6[iz+0];
s[25] = + g0[ix+0]*g1[iy+0]*g6[iz+0];
s[26] = + g0[ix+0]*g0[iy+0]*g7[iz+0];
gout[n*3+0] += - s[0] - s[4] - s[8];
gout[n*3+1] += - s[9] - s[13] - s[17];
gout[n*3+2] += - s[18] - s[22] - s[26];
}}
void int1e_ipkin_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {1, 2, 0, 0, 3, 1, 1, 3};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_ipkin_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 2, 0, 0, 3, 1, 1, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipkin;
envs.common_factor *= 0.5;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 0);
} // int1e_ipkin_cart
int int1e_ipkin_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 2, 0, 0, 3, 1, 1, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipkin;
envs.common_factor *= 0.5;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 0);
} // int1e_ipkin_sph
int int1e_ipkin_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 2, 0, 0, 3, 1, 1, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipkin;
envs.common_factor *= 0.5;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_sf_1e, 0);
} // int1e_ipkin_spinor
ALL_CINT1E(int1e_ipkin)
ALL_CINT1E_FORTRAN_(int1e_ipkin)
/* <NABLA i|NUC |j> */
static void CINTgout1e_int1e_ipnuc(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int ix, iy, iz, n;
double *g0 = g;
double *g1 = g0  + envs->g_size * 3;
double s[3];
G1E_D_I(g1, g0, envs->i_l+0, envs->j_l, 0);
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
s[0] = + g1[ix+0]*g0[iy+0]*g0[iz+0];
s[1] = + g0[ix+0]*g1[iy+0]*g0[iz+0];
s[2] = + g0[ix+0]*g0[iy+0]*g1[iz+0];
gout[n*3+0] += + s[0];
gout[n*3+1] += + s[1];
gout[n*3+2] += + s[2];
}}
void int1e_ipnuc_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {1, 0, 0, 0, 1, 1, 0, 3};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_ipnuc_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 0, 1, 1, 0, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipnuc;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 2);
} // int1e_ipnuc_cart
int int1e_ipnuc_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 0, 1, 1, 0, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipnuc;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 2);
} // int1e_ipnuc_sph
int int1e_ipnuc_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 0, 1, 1, 0, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipnuc;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_sf_1e, 2);
} // int1e_ipnuc_spinor
ALL_CINT1E(int1e_ipnuc)
ALL_CINT1E_FORTRAN_(int1e_ipnuc)
/* <NABLA i|RINV |j> */
static void CINTgout1e_int1e_iprinv(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int ix, iy, iz, n;
double *g0 = g;
double *g1 = g0  + envs->g_size * 3;
double s[3];
G1E_D_I(g1, g0, envs->i_l+0, envs->j_l, 0);
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
s[0] = + g1[ix+0]*g0[iy+0]*g0[iz+0];
s[1] = + g0[ix+0]*g1[iy+0]*g0[iz+0];
s[2] = + g0[ix+0]*g0[iy+0]*g1[iz+0];
gout[n*3+0] += + s[0];
gout[n*3+1] += + s[1];
gout[n*3+2] += + s[2];
}}
void int1e_iprinv_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {1, 0, 0, 0, 1, 1, 0, 3};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_iprinv_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 0, 1, 1, 0, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_iprinv;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 1);
} // int1e_iprinv_cart
int int1e_iprinv_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 0, 1, 1, 0, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_iprinv;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 1);
} // int1e_iprinv_sph
int int1e_iprinv_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 0, 1, 1, 0, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_iprinv;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_sf_1e, 1);
} // int1e_iprinv_spinor
ALL_CINT1E(int1e_iprinv)
ALL_CINT1E_FORTRAN_(int1e_iprinv)
/* <i|RINV |j> */
static void CINTgout1e_int1e_rinv(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int ix, iy, iz, n;
double *g0 = g;
double s[1];
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
s[0] = + g0[ix+0]*g0[iy+0]*g0[iz+0];
gout[n*1+0] += + s[0];
}}
void int1e_rinv_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {0, 0, 0, 0, 0, 1, 0, 1};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_rinv_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 0, 0, 0, 0, 1, 0, 1};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_rinv;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 1);
} // int1e_rinv_cart
int int1e_rinv_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 0, 0, 0, 0, 1, 0, 1};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_rinv;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 1);
} // int1e_rinv_sph
int int1e_rinv_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 0, 0, 0, 0, 1, 0, 1};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_rinv;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_sf_1e, 1);
} // int1e_rinv_spinor
ALL_CINT1E(int1e_rinv)
ALL_CINT1E_FORTRAN_(int1e_rinv)
/* <NABLA SIGMA DOT P i|NUC |SIGMA DOT P j> */
static void CINTgout1e_int1e_ipspnucsp(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int ix, iy, iz, n;
double *g0 = g;
double *g1 = g0  + envs->g_size * 3;
double *g2 = g1  + envs->g_size * 3;
double *g3 = g2  + envs->g_size * 3;
double *g4 = g3  + envs->g_size * 3;
double *g5 = g4  + envs->g_size * 3;
double *g6 = g5  + envs->g_size * 3;
double *g7 = g6  + envs->g_size * 3;
double s[27];
G1E_D_J(g1, g0, envs->i_l+2, envs->j_l+0, 0);
G1E_D_I(g2, g0, envs->i_l+1, envs->j_l, 0);
G1E_D_I(g3, g1, envs->i_l+1, envs->j_l, 0);
G1E_D_I(g4, g0, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g5, g1, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g6, g2, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g7, g3, envs->i_l+0, envs->j_l, 0);
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
s[0] = + g7[ix+0]*g0[iy+0]*g0[iz+0];
s[1] = + g6[ix+0]*g1[iy+0]*g0[iz+0];
s[2] = + g6[ix+0]*g0[iy+0]*g1[iz+0];
s[3] = + g5[ix+0]*g2[iy+0]*g0[iz+0];
s[4] = + g4[ix+0]*g3[iy+0]*g0[iz+0];
s[5] = + g4[ix+0]*g2[iy+0]*g1[iz+0];
s[6] = + g5[ix+0]*g0[iy+0]*g2[iz+0];
s[7] = + g4[ix+0]*g1[iy+0]*g2[iz+0];
s[8] = + g4[ix+0]*g0[iy+0]*g3[iz+0];
s[9] = + g3[ix+0]*g4[iy+0]*g0[iz+0];
s[10] = + g2[ix+0]*g5[iy+0]*g0[iz+0];
s[11] = + g2[ix+0]*g4[iy+0]*g1[iz+0];
s[12] = + g1[ix+0]*g6[iy+0]*g0[iz+0];
s[13] = + g0[ix+0]*g7[iy+0]*g0[iz+0];
s[14] = + g0[ix+0]*g6[iy+0]*g1[iz+0];
s[15] = + g1[ix+0]*g4[iy+0]*g2[iz+0];
s[16] = + g0[ix+0]*g5[iy+0]*g2[iz+0];
s[17] = + g0[ix+0]*g4[iy+0]*g3[iz+0];
s[18] = + g3[ix+0]*g0[iy+0]*g4[iz+0];
s[19] = + g2[ix+0]*g1[iy+0]*g4[iz+0];
s[20] = + g2[ix+0]*g0[iy+0]*g5[iz+0];
s[21] = + g1[ix+0]*g2[iy+0]*g4[iz+0];
s[22] = + g0[ix+0]*g3[iy+0]*g4[iz+0];
s[23] = + g0[ix+0]*g2[iy+0]*g5[iz+0];
s[24] = + g1[ix+0]*g0[iy+0]*g6[iz+0];
s[25] = + g0[ix+0]*g1[iy+0]*g6[iz+0];
s[26] = + g0[ix+0]*g0[iy+0]*g7[iz+0];
gout[n*12+0] += + s[11] - s[19];
gout[n*12+1] += + s[18] - s[2];
gout[n*12+2] += + s[1] - s[9];
gout[n*12+3] += + s[0] + s[10] + s[20];
gout[n*12+4] += + s[14] - s[22];
gout[n*12+5] += + s[21] - s[5];
gout[n*12+6] += + s[4] - s[12];
gout[n*12+7] += + s[3] + s[13] + s[23];
gout[n*12+8] += + s[17] - s[25];
gout[n*12+9] += + s[24] - s[8];
gout[n*12+10] += + s[7] - s[15];
gout[n*12+11] += + s[6] + s[16] + s[26];
}}
void int1e_ipspnucsp_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {2, 1, 0, 0, 3, 4, 0, 3};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_ipspnucsp_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 1, 0, 0, 3, 4, 0, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipspnucsp;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 2);
} // int1e_ipspnucsp_cart
int int1e_ipspnucsp_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 1, 0, 0, 3, 4, 0, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipspnucsp;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 2);
} // int1e_ipspnucsp_sph
int int1e_ipspnucsp_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 1, 0, 0, 3, 4, 0, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipspnucsp;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_si_1e, 2);
} // int1e_ipspnucsp_spinor
ALL_CINT1E(int1e_ipspnucsp)
ALL_CINT1E_FORTRAN_(int1e_ipspnucsp)
/* <NABLA SIGMA DOT P i|RINV |SIGMA DOT P j> */
static void CINTgout1e_int1e_ipsprinvsp(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int ix, iy, iz, n;
double *g0 = g;
double *g1 = g0  + envs->g_size * 3;
double *g2 = g1  + envs->g_size * 3;
double *g3 = g2  + envs->g_size * 3;
double *g4 = g3  + envs->g_size * 3;
double *g5 = g4  + envs->g_size * 3;
double *g6 = g5  + envs->g_size * 3;
double *g7 = g6  + envs->g_size * 3;
double s[27];
G1E_D_J(g1, g0, envs->i_l+2, envs->j_l+0, 0);
G1E_D_I(g2, g0, envs->i_l+1, envs->j_l, 0);
G1E_D_I(g3, g1, envs->i_l+1, envs->j_l, 0);
G1E_D_I(g4, g0, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g5, g1, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g6, g2, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g7, g3, envs->i_l+0, envs->j_l, 0);
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
s[0] = + g7[ix+0]*g0[iy+0]*g0[iz+0];
s[1] = + g6[ix+0]*g1[iy+0]*g0[iz+0];
s[2] = + g6[ix+0]*g0[iy+0]*g1[iz+0];
s[3] = + g5[ix+0]*g2[iy+0]*g0[iz+0];
s[4] = + g4[ix+0]*g3[iy+0]*g0[iz+0];
s[5] = + g4[ix+0]*g2[iy+0]*g1[iz+0];
s[6] = + g5[ix+0]*g0[iy+0]*g2[iz+0];
s[7] = + g4[ix+0]*g1[iy+0]*g2[iz+0];
s[8] = + g4[ix+0]*g0[iy+0]*g3[iz+0];
s[9] = + g3[ix+0]*g4[iy+0]*g0[iz+0];
s[10] = + g2[ix+0]*g5[iy+0]*g0[iz+0];
s[11] = + g2[ix+0]*g4[iy+0]*g1[iz+0];
s[12] = + g1[ix+0]*g6[iy+0]*g0[iz+0];
s[13] = + g0[ix+0]*g7[iy+0]*g0[iz+0];
s[14] = + g0[ix+0]*g6[iy+0]*g1[iz+0];
s[15] = + g1[ix+0]*g4[iy+0]*g2[iz+0];
s[16] = + g0[ix+0]*g5[iy+0]*g2[iz+0];
s[17] = + g0[ix+0]*g4[iy+0]*g3[iz+0];
s[18] = + g3[ix+0]*g0[iy+0]*g4[iz+0];
s[19] = + g2[ix+0]*g1[iy+0]*g4[iz+0];
s[20] = + g2[ix+0]*g0[iy+0]*g5[iz+0];
s[21] = + g1[ix+0]*g2[iy+0]*g4[iz+0];
s[22] = + g0[ix+0]*g3[iy+0]*g4[iz+0];
s[23] = + g0[ix+0]*g2[iy+0]*g5[iz+0];
s[24] = + g1[ix+0]*g0[iy+0]*g6[iz+0];
s[25] = + g0[ix+0]*g1[iy+0]*g6[iz+0];
s[26] = + g0[ix+0]*g0[iy+0]*g7[iz+0];
gout[n*12+0] += + s[11] - s[19];
gout[n*12+1] += + s[18] - s[2];
gout[n*12+2] += + s[1] - s[9];
gout[n*12+3] += + s[0] + s[10] + s[20];
gout[n*12+4] += + s[14] - s[22];
gout[n*12+5] += + s[21] - s[5];
gout[n*12+6] += + s[4] - s[12];
gout[n*12+7] += + s[3] + s[13] + s[23];
gout[n*12+8] += + s[17] - s[25];
gout[n*12+9] += + s[24] - s[8];
gout[n*12+10] += + s[7] - s[15];
gout[n*12+11] += + s[6] + s[16] + s[26];
}}
void int1e_ipsprinvsp_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {2, 1, 0, 0, 3, 4, 0, 3};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_ipsprinvsp_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 1, 0, 0, 3, 4, 0, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipsprinvsp;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 1);
} // int1e_ipsprinvsp_cart
int int1e_ipsprinvsp_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 1, 0, 0, 3, 4, 0, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipsprinvsp;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 1);
} // int1e_ipsprinvsp_sph
int int1e_ipsprinvsp_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 1, 0, 0, 3, 4, 0, 3};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipsprinvsp;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_si_1e, 1);
} // int1e_ipsprinvsp_spinor
ALL_CINT1E(int1e_ipsprinvsp)
ALL_CINT1E_FORTRAN_(int1e_ipsprinvsp)
