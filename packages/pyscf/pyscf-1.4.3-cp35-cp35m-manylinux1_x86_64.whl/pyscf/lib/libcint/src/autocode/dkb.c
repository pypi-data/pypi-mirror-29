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
/* <SIGMA DOT P i|OVLP |SIGMA DOT P SIGMA DOT P j> */
static void CINTgout1e_int1e_spspsp(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
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
gout[n*4+0] += - s[0] - s[12] - s[24];
gout[n*4+1] += - s[1] - s[13] - s[25];
gout[n*4+2] += - s[2] - s[14] - s[26];
gout[n*4+3] += 0;
}}
void int1e_spspsp_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {1, 2, 0, 0, 3, 4, 1, 1};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_spspsp_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 2, 0, 0, 3, 4, 1, 1};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_spspsp;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 0);
} // int1e_spspsp_cart
int int1e_spspsp_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 2, 0, 0, 3, 4, 1, 1};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_spspsp;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 0);
} // int1e_spspsp_sph
int int1e_spspsp_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 2, 0, 0, 3, 4, 1, 1};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_spspsp;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_si_1e, 0);
} // int1e_spspsp_spinor
ALL_CINT1E(int1e_spspsp)
ALL_CINT1E_FORTRAN_(int1e_spspsp)
/* <SIGMA DOT P i|NUC |j> */
static void CINTgout1e_int1e_spnuc(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
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
gout[n*4+0] += + s[0];
gout[n*4+1] += + s[1];
gout[n*4+2] += + s[2];
gout[n*4+3] += 0;
}}
void int1e_spnuc_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {1, 0, 0, 0, 1, 4, 0, 1};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_spnuc_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 0, 1, 4, 0, 1};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_spnuc;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 2);
} // int1e_spnuc_cart
int int1e_spnuc_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 0, 1, 4, 0, 1};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_spnuc;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 2);
} // int1e_spnuc_sph
int int1e_spnuc_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 0, 1, 4, 0, 1};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_spnuc;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_si_1e, 2);
} // int1e_spnuc_spinor
ALL_CINT1E(int1e_spnuc)
ALL_CINT1E_FORTRAN_(int1e_spnuc)
/* <k SIGMA DOT P i|R12 |j l> : i,j \in electron 1; k,l \in electron 2
 * = (SIGMA DOT P i j|R12 |k l) */
static void CINTgout2e_int2e_spv1(double *gout,
double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int nrys_roots = envs->nrys_roots;
int ix, iy, iz, i, n;
double *g0 = g;
double *g1 = g0 + envs->g_size * 3;
G2E_D_I(g1, g0, envs->i_l+0, envs->j_l, envs->k_l, envs->l_l);
double s[3];
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
switch (nrys_roots) {
case 1:
s[0] = + g1[ix+0]*g0[iy+0]*g0[iz+0];
s[1] = + g0[ix+0]*g1[iy+0]*g0[iz+0];
s[2] = + g0[ix+0]*g0[iy+0]*g1[iz+0];
break;
case 2:
s[0] = + g1[ix+0]*g0[iy+0]*g0[iz+0]+ g1[ix+1]*g0[iy+1]*g0[iz+1];
s[1] = + g0[ix+0]*g1[iy+0]*g0[iz+0]+ g0[ix+1]*g1[iy+1]*g0[iz+1];
s[2] = + g0[ix+0]*g0[iy+0]*g1[iz+0]+ g0[ix+1]*g0[iy+1]*g1[iz+1];
break;
case 3:
s[0] = + g1[ix+0]*g0[iy+0]*g0[iz+0]+ g1[ix+1]*g0[iy+1]*g0[iz+1]+ g1[ix+2]*g0[iy+2]*g0[iz+2];
s[1] = + g0[ix+0]*g1[iy+0]*g0[iz+0]+ g0[ix+1]*g1[iy+1]*g0[iz+1]+ g0[ix+2]*g1[iy+2]*g0[iz+2];
s[2] = + g0[ix+0]*g0[iy+0]*g1[iz+0]+ g0[ix+1]*g0[iy+1]*g1[iz+1]+ g0[ix+2]*g0[iy+2]*g1[iz+2];
break;
case 4:
s[0] = + g1[ix+0]*g0[iy+0]*g0[iz+0]+ g1[ix+1]*g0[iy+1]*g0[iz+1]+ g1[ix+2]*g0[iy+2]*g0[iz+2]+ g1[ix+3]*g0[iy+3]*g0[iz+3];
s[1] = + g0[ix+0]*g1[iy+0]*g0[iz+0]+ g0[ix+1]*g1[iy+1]*g0[iz+1]+ g0[ix+2]*g1[iy+2]*g0[iz+2]+ g0[ix+3]*g1[iy+3]*g0[iz+3];
s[2] = + g0[ix+0]*g0[iy+0]*g1[iz+0]+ g0[ix+1]*g0[iy+1]*g1[iz+1]+ g0[ix+2]*g0[iy+2]*g1[iz+2]+ g0[ix+3]*g0[iy+3]*g1[iz+3];
break;
default:
for (i = 0; i < 3; i++) { s[i] = 0; }
for (i = 0; i < nrys_roots; i++) {
s[0] += g1[ix+i] * g0[iy+i] * g0[iz+i];
s[1] += g0[ix+i] * g1[iy+i] * g0[iz+i];
s[2] += g0[ix+i] * g0[iy+i] * g1[iz+i];
} break;}
if (gout_empty) {
gout[n*4+0] = + s[0];
gout[n*4+1] = + s[1];
gout[n*4+2] = + s[2];
gout[n*4+3] = 0;
} else {
gout[n*4+0] += + s[0];
gout[n*4+1] += + s[1];
gout[n*4+2] += + s[2];
gout[n*4+3] += 0;
}}}
void int2e_spv1_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {1, 0, 0, 0, 1, 4, 1, 1};
CINTall_2e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int2e_spv1_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 0, 1, 4, 1, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_spv1;
return CINT2e_cart_drv(out, dims, &envs, opt, cache);
} // int2e_spv1_cart
int int2e_spv1_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 0, 1, 4, 1, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_spv1;
return CINT2e_spheric_drv(out, dims, &envs, opt, cache);
} // int2e_spv1_sph
int int2e_spv1_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 0, 1, 4, 1, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_spv1;
return CINT2e_spinor_drv(out, dims, &envs, opt, cache, &c2s_si_2e1, &c2s_sf_2e2);
} // int2e_spv1_spinor
ALL_CINT(int2e_spv1)
ALL_CINT_FORTRAN_(int2e_spv1)
/* <k i|R12 |SIGMA DOT P j l> : i,j \in electron 1; k,l \in electron 2
 * = (i SIGMA DOT P j|R12 |k l) */
static void CINTgout2e_int2e_vsp1(double *gout,
double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int nrys_roots = envs->nrys_roots;
int ix, iy, iz, i, n;
double *g0 = g;
double *g1 = g0 + envs->g_size * 3;
G2E_D_J(g1, g0, envs->i_l+0, envs->j_l+0, envs->k_l, envs->l_l);
double s[3];
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
switch (nrys_roots) {
case 1:
s[0] = + g1[ix+0]*g0[iy+0]*g0[iz+0];
s[1] = + g0[ix+0]*g1[iy+0]*g0[iz+0];
s[2] = + g0[ix+0]*g0[iy+0]*g1[iz+0];
break;
case 2:
s[0] = + g1[ix+0]*g0[iy+0]*g0[iz+0]+ g1[ix+1]*g0[iy+1]*g0[iz+1];
s[1] = + g0[ix+0]*g1[iy+0]*g0[iz+0]+ g0[ix+1]*g1[iy+1]*g0[iz+1];
s[2] = + g0[ix+0]*g0[iy+0]*g1[iz+0]+ g0[ix+1]*g0[iy+1]*g1[iz+1];
break;
case 3:
s[0] = + g1[ix+0]*g0[iy+0]*g0[iz+0]+ g1[ix+1]*g0[iy+1]*g0[iz+1]+ g1[ix+2]*g0[iy+2]*g0[iz+2];
s[1] = + g0[ix+0]*g1[iy+0]*g0[iz+0]+ g0[ix+1]*g1[iy+1]*g0[iz+1]+ g0[ix+2]*g1[iy+2]*g0[iz+2];
s[2] = + g0[ix+0]*g0[iy+0]*g1[iz+0]+ g0[ix+1]*g0[iy+1]*g1[iz+1]+ g0[ix+2]*g0[iy+2]*g1[iz+2];
break;
case 4:
s[0] = + g1[ix+0]*g0[iy+0]*g0[iz+0]+ g1[ix+1]*g0[iy+1]*g0[iz+1]+ g1[ix+2]*g0[iy+2]*g0[iz+2]+ g1[ix+3]*g0[iy+3]*g0[iz+3];
s[1] = + g0[ix+0]*g1[iy+0]*g0[iz+0]+ g0[ix+1]*g1[iy+1]*g0[iz+1]+ g0[ix+2]*g1[iy+2]*g0[iz+2]+ g0[ix+3]*g1[iy+3]*g0[iz+3];
s[2] = + g0[ix+0]*g0[iy+0]*g1[iz+0]+ g0[ix+1]*g0[iy+1]*g1[iz+1]+ g0[ix+2]*g0[iy+2]*g1[iz+2]+ g0[ix+3]*g0[iy+3]*g1[iz+3];
break;
default:
for (i = 0; i < 3; i++) { s[i] = 0; }
for (i = 0; i < nrys_roots; i++) {
s[0] += g1[ix+i] * g0[iy+i] * g0[iz+i];
s[1] += g0[ix+i] * g1[iy+i] * g0[iz+i];
s[2] += g0[ix+i] * g0[iy+i] * g1[iz+i];
} break;}
if (gout_empty) {
gout[n*4+0] = - s[0];
gout[n*4+1] = - s[1];
gout[n*4+2] = - s[2];
gout[n*4+3] = 0;
} else {
gout[n*4+0] += - s[0];
gout[n*4+1] += - s[1];
gout[n*4+2] += - s[2];
gout[n*4+3] += 0;
}}}
void int2e_vsp1_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {0, 1, 0, 0, 1, 4, 1, 1};
CINTall_2e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int2e_vsp1_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 1, 0, 0, 1, 4, 1, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_vsp1;
return CINT2e_cart_drv(out, dims, &envs, opt, cache);
} // int2e_vsp1_cart
int int2e_vsp1_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 1, 0, 0, 1, 4, 1, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_vsp1;
return CINT2e_spheric_drv(out, dims, &envs, opt, cache);
} // int2e_vsp1_sph
int int2e_vsp1_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 1, 0, 0, 1, 4, 1, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_vsp1;
return CINT2e_spinor_drv(out, dims, &envs, opt, cache, &c2s_si_2e1, &c2s_sf_2e2);
} // int2e_vsp1_spinor
ALL_CINT(int2e_vsp1)
ALL_CINT_FORTRAN_(int2e_vsp1)
/* <SIGMA DOT P k i|R12 |j SIGMA DOT P l> : i,j \in electron 1; k,l \in electron 2
 * = (i j|R12 |SIGMA DOT P k SIGMA DOT P l) */
static void CINTgout2e_int2e_spsp2(double *gout,
double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int nrys_roots = envs->nrys_roots;
int ix, iy, iz, i, n;
double *g0 = g;
double *g1 = g0 + envs->g_size * 3;
double *g2 = g1 + envs->g_size * 3;
double *g3 = g2 + envs->g_size * 3;
G2E_D_L(g1, g0, envs->i_l+0, envs->j_l+0, envs->k_l+1, envs->l_l+0);
G2E_D_K(g2, g0, envs->i_l+0, envs->j_l+0, envs->k_l+0, envs->l_l);
G2E_D_K(g3, g1, envs->i_l+0, envs->j_l+0, envs->k_l+0, envs->l_l);
double s[9];
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
for (i = 0; i < 9; i++) { s[i] = 0; }
for (i = 0; i < nrys_roots; i++) {
s[0] += g3[ix+i] * g0[iy+i] * g0[iz+i];
s[1] += g2[ix+i] * g1[iy+i] * g0[iz+i];
s[2] += g2[ix+i] * g0[iy+i] * g1[iz+i];
s[3] += g1[ix+i] * g2[iy+i] * g0[iz+i];
s[4] += g0[ix+i] * g3[iy+i] * g0[iz+i];
s[5] += g0[ix+i] * g2[iy+i] * g1[iz+i];
s[6] += g1[ix+i] * g0[iy+i] * g2[iz+i];
s[7] += g0[ix+i] * g1[iy+i] * g2[iz+i];
s[8] += g0[ix+i] * g0[iy+i] * g3[iz+i];
}
if (gout_empty) {
gout[n*4+0] = + s[5] - s[7];
gout[n*4+1] = + s[6] - s[2];
gout[n*4+2] = + s[1] - s[3];
gout[n*4+3] = + s[0] + s[4] + s[8];
} else {
gout[n*4+0] += + s[5] - s[7];
gout[n*4+1] += + s[6] - s[2];
gout[n*4+2] += + s[1] - s[3];
gout[n*4+3] += + s[0] + s[4] + s[8];
}}}
void int2e_spsp2_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {0, 0, 1, 1, 2, 1, 4, 1};
CINTall_2e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int2e_spsp2_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 0, 1, 1, 2, 1, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_spsp2;
return CINT2e_cart_drv(out, dims, &envs, opt, cache);
} // int2e_spsp2_cart
int int2e_spsp2_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 0, 1, 1, 2, 1, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_spsp2;
return CINT2e_spheric_drv(out, dims, &envs, opt, cache);
} // int2e_spsp2_sph
int int2e_spsp2_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 0, 1, 1, 2, 1, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_spsp2;
return CINT2e_spinor_drv(out, dims, &envs, opt, cache, &c2s_sf_2e1, &c2s_si_2e2);
} // int2e_spsp2_spinor
ALL_CINT(int2e_spsp2)
ALL_CINT_FORTRAN_(int2e_spsp2)
/* <SIGMA DOT P k SIGMA DOT P i|R12 |j l> : i,j \in electron 1; k,l \in electron 2
 * = (SIGMA DOT P i j|R12 |SIGMA DOT P k l) */
static void CINTgout2e_int2e_spv1spv2(double *gout,
double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int nrys_roots = envs->nrys_roots;
int ix, iy, iz, i, n;
double *g0 = g;
double *g1 = g0 + envs->g_size * 3;
double *g2 = g1 + envs->g_size * 3;
double *g3 = g2 + envs->g_size * 3;
G2E_D_K(g1, g0, envs->i_l+1, envs->j_l+0, envs->k_l+0, envs->l_l);
G2E_D_I(g2, g0, envs->i_l+0, envs->j_l, envs->k_l, envs->l_l);
G2E_D_I(g3, g1, envs->i_l+0, envs->j_l, envs->k_l, envs->l_l);
double s[9];
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
for (i = 0; i < 9; i++) { s[i] = 0; }
for (i = 0; i < nrys_roots; i++) {
s[0] += g3[ix+i] * g0[iy+i] * g0[iz+i];
s[1] += g2[ix+i] * g1[iy+i] * g0[iz+i];
s[2] += g2[ix+i] * g0[iy+i] * g1[iz+i];
s[3] += g1[ix+i] * g2[iy+i] * g0[iz+i];
s[4] += g0[ix+i] * g3[iy+i] * g0[iz+i];
s[5] += g0[ix+i] * g2[iy+i] * g1[iz+i];
s[6] += g1[ix+i] * g0[iy+i] * g2[iz+i];
s[7] += g0[ix+i] * g1[iy+i] * g2[iz+i];
s[8] += g0[ix+i] * g0[iy+i] * g3[iz+i];
}
if (gout_empty) {
gout[n*16+0] = + s[0];
gout[n*16+1] = + s[3];
gout[n*16+2] = + s[6];
gout[n*16+3] = 0;
gout[n*16+4] = + s[1];
gout[n*16+5] = + s[4];
gout[n*16+6] = + s[7];
gout[n*16+7] = 0;
gout[n*16+8] = + s[2];
gout[n*16+9] = + s[5];
gout[n*16+10] = + s[8];
gout[n*16+11] = 0;
gout[n*16+12] = 0;
gout[n*16+13] = 0;
gout[n*16+14] = 0;
gout[n*16+15] = 0;
} else {
gout[n*16+0] += + s[0];
gout[n*16+1] += + s[3];
gout[n*16+2] += + s[6];
gout[n*16+3] += 0;
gout[n*16+4] += + s[1];
gout[n*16+5] += + s[4];
gout[n*16+6] += + s[7];
gout[n*16+7] += 0;
gout[n*16+8] += + s[2];
gout[n*16+9] += + s[5];
gout[n*16+10] += + s[8];
gout[n*16+11] += 0;
gout[n*16+12] += 0;
gout[n*16+13] += 0;
gout[n*16+14] += 0;
gout[n*16+15] += 0;
}}}
void int2e_spv1spv2_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {1, 0, 1, 0, 2, 4, 4, 1};
CINTall_2e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int2e_spv1spv2_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 1, 0, 2, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_spv1spv2;
return CINT2e_cart_drv(out, dims, &envs, opt, cache);
} // int2e_spv1spv2_cart
int int2e_spv1spv2_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 1, 0, 2, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_spv1spv2;
return CINT2e_spheric_drv(out, dims, &envs, opt, cache);
} // int2e_spv1spv2_sph
int int2e_spv1spv2_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 1, 0, 2, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_spv1spv2;
return CINT2e_spinor_drv(out, dims, &envs, opt, cache, &c2s_si_2e1, &c2s_si_2e2);
} // int2e_spv1spv2_spinor
ALL_CINT(int2e_spv1spv2)
ALL_CINT_FORTRAN_(int2e_spv1spv2)
/* <SIGMA DOT P k i|R12 |SIGMA DOT P j l> : i,j \in electron 1; k,l \in electron 2
 * = (i SIGMA DOT P j|R12 |SIGMA DOT P k l) */
static void CINTgout2e_int2e_vsp1spv2(double *gout,
double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int nrys_roots = envs->nrys_roots;
int ix, iy, iz, i, n;
double *g0 = g;
double *g1 = g0 + envs->g_size * 3;
double *g2 = g1 + envs->g_size * 3;
double *g3 = g2 + envs->g_size * 3;
G2E_D_K(g1, g0, envs->i_l+0, envs->j_l+1, envs->k_l+0, envs->l_l);
G2E_D_J(g2, g0, envs->i_l+0, envs->j_l+0, envs->k_l, envs->l_l);
G2E_D_J(g3, g1, envs->i_l+0, envs->j_l+0, envs->k_l, envs->l_l);
double s[9];
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
for (i = 0; i < 9; i++) { s[i] = 0; }
for (i = 0; i < nrys_roots; i++) {
s[0] += g3[ix+i] * g0[iy+i] * g0[iz+i];
s[1] += g2[ix+i] * g1[iy+i] * g0[iz+i];
s[2] += g2[ix+i] * g0[iy+i] * g1[iz+i];
s[3] += g1[ix+i] * g2[iy+i] * g0[iz+i];
s[4] += g0[ix+i] * g3[iy+i] * g0[iz+i];
s[5] += g0[ix+i] * g2[iy+i] * g1[iz+i];
s[6] += g1[ix+i] * g0[iy+i] * g2[iz+i];
s[7] += g0[ix+i] * g1[iy+i] * g2[iz+i];
s[8] += g0[ix+i] * g0[iy+i] * g3[iz+i];
}
if (gout_empty) {
gout[n*16+0] = - s[0];
gout[n*16+1] = - s[3];
gout[n*16+2] = - s[6];
gout[n*16+3] = 0;
gout[n*16+4] = - s[1];
gout[n*16+5] = - s[4];
gout[n*16+6] = - s[7];
gout[n*16+7] = 0;
gout[n*16+8] = - s[2];
gout[n*16+9] = - s[5];
gout[n*16+10] = - s[8];
gout[n*16+11] = 0;
gout[n*16+12] = 0;
gout[n*16+13] = 0;
gout[n*16+14] = 0;
gout[n*16+15] = 0;
} else {
gout[n*16+0] += - s[0];
gout[n*16+1] += - s[3];
gout[n*16+2] += - s[6];
gout[n*16+3] += 0;
gout[n*16+4] += - s[1];
gout[n*16+5] += - s[4];
gout[n*16+6] += - s[7];
gout[n*16+7] += 0;
gout[n*16+8] += - s[2];
gout[n*16+9] += - s[5];
gout[n*16+10] += - s[8];
gout[n*16+11] += 0;
gout[n*16+12] += 0;
gout[n*16+13] += 0;
gout[n*16+14] += 0;
gout[n*16+15] += 0;
}}}
void int2e_vsp1spv2_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {0, 1, 1, 0, 2, 4, 4, 1};
CINTall_2e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int2e_vsp1spv2_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 1, 1, 0, 2, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_vsp1spv2;
return CINT2e_cart_drv(out, dims, &envs, opt, cache);
} // int2e_vsp1spv2_cart
int int2e_vsp1spv2_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 1, 1, 0, 2, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_vsp1spv2;
return CINT2e_spheric_drv(out, dims, &envs, opt, cache);
} // int2e_vsp1spv2_sph
int int2e_vsp1spv2_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 1, 1, 0, 2, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_vsp1spv2;
return CINT2e_spinor_drv(out, dims, &envs, opt, cache, &c2s_si_2e1, &c2s_si_2e2);
} // int2e_vsp1spv2_spinor
ALL_CINT(int2e_vsp1spv2)
ALL_CINT_FORTRAN_(int2e_vsp1spv2)
/* <k SIGMA DOT P i|R12 |j SIGMA DOT P l> : i,j \in electron 1; k,l \in electron 2
 * = (SIGMA DOT P i j|R12 |k SIGMA DOT P l) */
static void CINTgout2e_int2e_spv1vsp2(double *gout,
double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int nrys_roots = envs->nrys_roots;
int ix, iy, iz, i, n;
double *g0 = g;
double *g1 = g0 + envs->g_size * 3;
double *g2 = g1 + envs->g_size * 3;
double *g3 = g2 + envs->g_size * 3;
G2E_D_L(g1, g0, envs->i_l+1, envs->j_l+0, envs->k_l+0, envs->l_l+0);
G2E_D_I(g2, g0, envs->i_l+0, envs->j_l, envs->k_l, envs->l_l);
G2E_D_I(g3, g1, envs->i_l+0, envs->j_l, envs->k_l, envs->l_l);
double s[9];
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
for (i = 0; i < 9; i++) { s[i] = 0; }
for (i = 0; i < nrys_roots; i++) {
s[0] += g3[ix+i] * g0[iy+i] * g0[iz+i];
s[1] += g2[ix+i] * g1[iy+i] * g0[iz+i];
s[2] += g2[ix+i] * g0[iy+i] * g1[iz+i];
s[3] += g1[ix+i] * g2[iy+i] * g0[iz+i];
s[4] += g0[ix+i] * g3[iy+i] * g0[iz+i];
s[5] += g0[ix+i] * g2[iy+i] * g1[iz+i];
s[6] += g1[ix+i] * g0[iy+i] * g2[iz+i];
s[7] += g0[ix+i] * g1[iy+i] * g2[iz+i];
s[8] += g0[ix+i] * g0[iy+i] * g3[iz+i];
}
if (gout_empty) {
gout[n*16+0] = - s[0];
gout[n*16+1] = - s[3];
gout[n*16+2] = - s[6];
gout[n*16+3] = 0;
gout[n*16+4] = - s[1];
gout[n*16+5] = - s[4];
gout[n*16+6] = - s[7];
gout[n*16+7] = 0;
gout[n*16+8] = - s[2];
gout[n*16+9] = - s[5];
gout[n*16+10] = - s[8];
gout[n*16+11] = 0;
gout[n*16+12] = 0;
gout[n*16+13] = 0;
gout[n*16+14] = 0;
gout[n*16+15] = 0;
} else {
gout[n*16+0] += - s[0];
gout[n*16+1] += - s[3];
gout[n*16+2] += - s[6];
gout[n*16+3] += 0;
gout[n*16+4] += - s[1];
gout[n*16+5] += - s[4];
gout[n*16+6] += - s[7];
gout[n*16+7] += 0;
gout[n*16+8] += - s[2];
gout[n*16+9] += - s[5];
gout[n*16+10] += - s[8];
gout[n*16+11] += 0;
gout[n*16+12] += 0;
gout[n*16+13] += 0;
gout[n*16+14] += 0;
gout[n*16+15] += 0;
}}}
void int2e_spv1vsp2_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {1, 0, 0, 1, 2, 4, 4, 1};
CINTall_2e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int2e_spv1vsp2_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 1, 2, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_spv1vsp2;
return CINT2e_cart_drv(out, dims, &envs, opt, cache);
} // int2e_spv1vsp2_cart
int int2e_spv1vsp2_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 1, 2, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_spv1vsp2;
return CINT2e_spheric_drv(out, dims, &envs, opt, cache);
} // int2e_spv1vsp2_sph
int int2e_spv1vsp2_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 0, 1, 2, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_spv1vsp2;
return CINT2e_spinor_drv(out, dims, &envs, opt, cache, &c2s_si_2e1, &c2s_si_2e2);
} // int2e_spv1vsp2_spinor
ALL_CINT(int2e_spv1vsp2)
ALL_CINT_FORTRAN_(int2e_spv1vsp2)
/* <k i|R12 |SIGMA DOT P j SIGMA DOT P l> : i,j \in electron 1; k,l \in electron 2
 * = (i SIGMA DOT P j|R12 |k SIGMA DOT P l) */
static void CINTgout2e_int2e_vsp1vsp2(double *gout,
double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int nrys_roots = envs->nrys_roots;
int ix, iy, iz, i, n;
double *g0 = g;
double *g1 = g0 + envs->g_size * 3;
double *g2 = g1 + envs->g_size * 3;
double *g3 = g2 + envs->g_size * 3;
G2E_D_L(g1, g0, envs->i_l+0, envs->j_l+1, envs->k_l+0, envs->l_l+0);
G2E_D_J(g2, g0, envs->i_l+0, envs->j_l+0, envs->k_l, envs->l_l);
G2E_D_J(g3, g1, envs->i_l+0, envs->j_l+0, envs->k_l, envs->l_l);
double s[9];
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
for (i = 0; i < 9; i++) { s[i] = 0; }
for (i = 0; i < nrys_roots; i++) {
s[0] += g3[ix+i] * g0[iy+i] * g0[iz+i];
s[1] += g2[ix+i] * g1[iy+i] * g0[iz+i];
s[2] += g2[ix+i] * g0[iy+i] * g1[iz+i];
s[3] += g1[ix+i] * g2[iy+i] * g0[iz+i];
s[4] += g0[ix+i] * g3[iy+i] * g0[iz+i];
s[5] += g0[ix+i] * g2[iy+i] * g1[iz+i];
s[6] += g1[ix+i] * g0[iy+i] * g2[iz+i];
s[7] += g0[ix+i] * g1[iy+i] * g2[iz+i];
s[8] += g0[ix+i] * g0[iy+i] * g3[iz+i];
}
if (gout_empty) {
gout[n*16+0] = + s[0];
gout[n*16+1] = + s[3];
gout[n*16+2] = + s[6];
gout[n*16+3] = 0;
gout[n*16+4] = + s[1];
gout[n*16+5] = + s[4];
gout[n*16+6] = + s[7];
gout[n*16+7] = 0;
gout[n*16+8] = + s[2];
gout[n*16+9] = + s[5];
gout[n*16+10] = + s[8];
gout[n*16+11] = 0;
gout[n*16+12] = 0;
gout[n*16+13] = 0;
gout[n*16+14] = 0;
gout[n*16+15] = 0;
} else {
gout[n*16+0] += + s[0];
gout[n*16+1] += + s[3];
gout[n*16+2] += + s[6];
gout[n*16+3] += 0;
gout[n*16+4] += + s[1];
gout[n*16+5] += + s[4];
gout[n*16+6] += + s[7];
gout[n*16+7] += 0;
gout[n*16+8] += + s[2];
gout[n*16+9] += + s[5];
gout[n*16+10] += + s[8];
gout[n*16+11] += 0;
gout[n*16+12] += 0;
gout[n*16+13] += 0;
gout[n*16+14] += 0;
gout[n*16+15] += 0;
}}}
void int2e_vsp1vsp2_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {0, 1, 0, 1, 2, 4, 4, 1};
CINTall_2e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int2e_vsp1vsp2_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 1, 0, 1, 2, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_vsp1vsp2;
return CINT2e_cart_drv(out, dims, &envs, opt, cache);
} // int2e_vsp1vsp2_cart
int int2e_vsp1vsp2_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 1, 0, 1, 2, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_vsp1vsp2;
return CINT2e_spheric_drv(out, dims, &envs, opt, cache);
} // int2e_vsp1vsp2_sph
int int2e_vsp1vsp2_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 1, 0, 1, 2, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_vsp1vsp2;
return CINT2e_spinor_drv(out, dims, &envs, opt, cache, &c2s_si_2e1, &c2s_si_2e2);
} // int2e_vsp1vsp2_spinor
ALL_CINT(int2e_vsp1vsp2)
ALL_CINT_FORTRAN_(int2e_vsp1vsp2)
/* <SIGMA DOT P k SIGMA DOT P i|R12 |j SIGMA DOT P l> : i,j \in electron 1; k,l \in electron 2
 * = (SIGMA DOT P i j|R12 |SIGMA DOT P k SIGMA DOT P l) */
static void CINTgout2e_int2e_spv1spsp2(double *gout,
double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int nrys_roots = envs->nrys_roots;
int ix, iy, iz, i, n;
double *g0 = g;
double *g1 = g0 + envs->g_size * 3;
double *g2 = g1 + envs->g_size * 3;
double *g3 = g2 + envs->g_size * 3;
double *g4 = g3 + envs->g_size * 3;
double *g5 = g4 + envs->g_size * 3;
double *g6 = g5 + envs->g_size * 3;
double *g7 = g6 + envs->g_size * 3;
G2E_D_L(g1, g0, envs->i_l+1, envs->j_l+0, envs->k_l+1, envs->l_l+0);
G2E_D_K(g2, g0, envs->i_l+1, envs->j_l+0, envs->k_l+0, envs->l_l);
G2E_D_K(g3, g1, envs->i_l+1, envs->j_l+0, envs->k_l+0, envs->l_l);
G2E_D_I(g4, g0, envs->i_l+0, envs->j_l, envs->k_l, envs->l_l);
G2E_D_I(g5, g1, envs->i_l+0, envs->j_l, envs->k_l, envs->l_l);
G2E_D_I(g6, g2, envs->i_l+0, envs->j_l, envs->k_l, envs->l_l);
G2E_D_I(g7, g3, envs->i_l+0, envs->j_l, envs->k_l, envs->l_l);
double s[27];
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
for (i = 0; i < 27; i++) { s[i] = 0; }
for (i = 0; i < nrys_roots; i++) {
s[0] += g7[ix+i] * g0[iy+i] * g0[iz+i];
s[1] += g6[ix+i] * g1[iy+i] * g0[iz+i];
s[2] += g6[ix+i] * g0[iy+i] * g1[iz+i];
s[3] += g5[ix+i] * g2[iy+i] * g0[iz+i];
s[4] += g4[ix+i] * g3[iy+i] * g0[iz+i];
s[5] += g4[ix+i] * g2[iy+i] * g1[iz+i];
s[6] += g5[ix+i] * g0[iy+i] * g2[iz+i];
s[7] += g4[ix+i] * g1[iy+i] * g2[iz+i];
s[8] += g4[ix+i] * g0[iy+i] * g3[iz+i];
s[9] += g3[ix+i] * g4[iy+i] * g0[iz+i];
s[10] += g2[ix+i] * g5[iy+i] * g0[iz+i];
s[11] += g2[ix+i] * g4[iy+i] * g1[iz+i];
s[12] += g1[ix+i] * g6[iy+i] * g0[iz+i];
s[13] += g0[ix+i] * g7[iy+i] * g0[iz+i];
s[14] += g0[ix+i] * g6[iy+i] * g1[iz+i];
s[15] += g1[ix+i] * g4[iy+i] * g2[iz+i];
s[16] += g0[ix+i] * g5[iy+i] * g2[iz+i];
s[17] += g0[ix+i] * g4[iy+i] * g3[iz+i];
s[18] += g3[ix+i] * g0[iy+i] * g4[iz+i];
s[19] += g2[ix+i] * g1[iy+i] * g4[iz+i];
s[20] += g2[ix+i] * g0[iy+i] * g5[iz+i];
s[21] += g1[ix+i] * g2[iy+i] * g4[iz+i];
s[22] += g0[ix+i] * g3[iy+i] * g4[iz+i];
s[23] += g0[ix+i] * g2[iy+i] * g5[iz+i];
s[24] += g1[ix+i] * g0[iy+i] * g6[iz+i];
s[25] += g0[ix+i] * g1[iy+i] * g6[iz+i];
s[26] += g0[ix+i] * g0[iy+i] * g7[iz+i];
}
if (gout_empty) {
gout[n*16+0] = + s[5] - s[7];
gout[n*16+1] = + s[14] - s[16];
gout[n*16+2] = + s[23] - s[25];
gout[n*16+3] = 0;
gout[n*16+4] = + s[6] - s[2];
gout[n*16+5] = + s[15] - s[11];
gout[n*16+6] = + s[24] - s[20];
gout[n*16+7] = 0;
gout[n*16+8] = + s[1] - s[3];
gout[n*16+9] = + s[10] - s[12];
gout[n*16+10] = + s[19] - s[21];
gout[n*16+11] = 0;
gout[n*16+12] = + s[0] + s[4] + s[8];
gout[n*16+13] = + s[9] + s[13] + s[17];
gout[n*16+14] = + s[18] + s[22] + s[26];
gout[n*16+15] = 0;
} else {
gout[n*16+0] += + s[5] - s[7];
gout[n*16+1] += + s[14] - s[16];
gout[n*16+2] += + s[23] - s[25];
gout[n*16+3] += 0;
gout[n*16+4] += + s[6] - s[2];
gout[n*16+5] += + s[15] - s[11];
gout[n*16+6] += + s[24] - s[20];
gout[n*16+7] += 0;
gout[n*16+8] += + s[1] - s[3];
gout[n*16+9] += + s[10] - s[12];
gout[n*16+10] += + s[19] - s[21];
gout[n*16+11] += 0;
gout[n*16+12] += + s[0] + s[4] + s[8];
gout[n*16+13] += + s[9] + s[13] + s[17];
gout[n*16+14] += + s[18] + s[22] + s[26];
gout[n*16+15] += 0;
}}}
void int2e_spv1spsp2_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {1, 0, 1, 1, 3, 4, 4, 1};
CINTall_2e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int2e_spv1spsp2_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 1, 1, 3, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_spv1spsp2;
return CINT2e_cart_drv(out, dims, &envs, opt, cache);
} // int2e_spv1spsp2_cart
int int2e_spv1spsp2_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 1, 1, 3, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_spv1spsp2;
return CINT2e_spheric_drv(out, dims, &envs, opt, cache);
} // int2e_spv1spsp2_sph
int int2e_spv1spsp2_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 1, 1, 3, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_spv1spsp2;
return CINT2e_spinor_drv(out, dims, &envs, opt, cache, &c2s_si_2e1, &c2s_si_2e2);
} // int2e_spv1spsp2_spinor
ALL_CINT(int2e_spv1spsp2)
ALL_CINT_FORTRAN_(int2e_spv1spsp2)
/* <SIGMA DOT P k i|R12 |SIGMA DOT P j SIGMA DOT P l> : i,j \in electron 1; k,l \in electron 2
 * = (i SIGMA DOT P j|R12 |SIGMA DOT P k SIGMA DOT P l) */
static void CINTgout2e_int2e_vsp1spsp2(double *gout,
double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int nrys_roots = envs->nrys_roots;
int ix, iy, iz, i, n;
double *g0 = g;
double *g1 = g0 + envs->g_size * 3;
double *g2 = g1 + envs->g_size * 3;
double *g3 = g2 + envs->g_size * 3;
double *g4 = g3 + envs->g_size * 3;
double *g5 = g4 + envs->g_size * 3;
double *g6 = g5 + envs->g_size * 3;
double *g7 = g6 + envs->g_size * 3;
G2E_D_L(g1, g0, envs->i_l+0, envs->j_l+1, envs->k_l+1, envs->l_l+0);
G2E_D_K(g2, g0, envs->i_l+0, envs->j_l+1, envs->k_l+0, envs->l_l);
G2E_D_K(g3, g1, envs->i_l+0, envs->j_l+1, envs->k_l+0, envs->l_l);
G2E_D_J(g4, g0, envs->i_l+0, envs->j_l+0, envs->k_l, envs->l_l);
G2E_D_J(g5, g1, envs->i_l+0, envs->j_l+0, envs->k_l, envs->l_l);
G2E_D_J(g6, g2, envs->i_l+0, envs->j_l+0, envs->k_l, envs->l_l);
G2E_D_J(g7, g3, envs->i_l+0, envs->j_l+0, envs->k_l, envs->l_l);
double s[27];
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
for (i = 0; i < 27; i++) { s[i] = 0; }
for (i = 0; i < nrys_roots; i++) {
s[0] += g7[ix+i] * g0[iy+i] * g0[iz+i];
s[1] += g6[ix+i] * g1[iy+i] * g0[iz+i];
s[2] += g6[ix+i] * g0[iy+i] * g1[iz+i];
s[3] += g5[ix+i] * g2[iy+i] * g0[iz+i];
s[4] += g4[ix+i] * g3[iy+i] * g0[iz+i];
s[5] += g4[ix+i] * g2[iy+i] * g1[iz+i];
s[6] += g5[ix+i] * g0[iy+i] * g2[iz+i];
s[7] += g4[ix+i] * g1[iy+i] * g2[iz+i];
s[8] += g4[ix+i] * g0[iy+i] * g3[iz+i];
s[9] += g3[ix+i] * g4[iy+i] * g0[iz+i];
s[10] += g2[ix+i] * g5[iy+i] * g0[iz+i];
s[11] += g2[ix+i] * g4[iy+i] * g1[iz+i];
s[12] += g1[ix+i] * g6[iy+i] * g0[iz+i];
s[13] += g0[ix+i] * g7[iy+i] * g0[iz+i];
s[14] += g0[ix+i] * g6[iy+i] * g1[iz+i];
s[15] += g1[ix+i] * g4[iy+i] * g2[iz+i];
s[16] += g0[ix+i] * g5[iy+i] * g2[iz+i];
s[17] += g0[ix+i] * g4[iy+i] * g3[iz+i];
s[18] += g3[ix+i] * g0[iy+i] * g4[iz+i];
s[19] += g2[ix+i] * g1[iy+i] * g4[iz+i];
s[20] += g2[ix+i] * g0[iy+i] * g5[iz+i];
s[21] += g1[ix+i] * g2[iy+i] * g4[iz+i];
s[22] += g0[ix+i] * g3[iy+i] * g4[iz+i];
s[23] += g0[ix+i] * g2[iy+i] * g5[iz+i];
s[24] += g1[ix+i] * g0[iy+i] * g6[iz+i];
s[25] += g0[ix+i] * g1[iy+i] * g6[iz+i];
s[26] += g0[ix+i] * g0[iy+i] * g7[iz+i];
}
if (gout_empty) {
gout[n*16+0] = - s[5] + s[7];
gout[n*16+1] = - s[14] + s[16];
gout[n*16+2] = - s[23] + s[25];
gout[n*16+3] = 0;
gout[n*16+4] = - s[6] + s[2];
gout[n*16+5] = - s[15] + s[11];
gout[n*16+6] = - s[24] + s[20];
gout[n*16+7] = 0;
gout[n*16+8] = - s[1] + s[3];
gout[n*16+9] = - s[10] + s[12];
gout[n*16+10] = - s[19] + s[21];
gout[n*16+11] = 0;
gout[n*16+12] = - s[0] - s[4] - s[8];
gout[n*16+13] = - s[9] - s[13] - s[17];
gout[n*16+14] = - s[18] - s[22] - s[26];
gout[n*16+15] = 0;
} else {
gout[n*16+0] += - s[5] + s[7];
gout[n*16+1] += - s[14] + s[16];
gout[n*16+2] += - s[23] + s[25];
gout[n*16+3] += 0;
gout[n*16+4] += - s[6] + s[2];
gout[n*16+5] += - s[15] + s[11];
gout[n*16+6] += - s[24] + s[20];
gout[n*16+7] += 0;
gout[n*16+8] += - s[1] + s[3];
gout[n*16+9] += - s[10] + s[12];
gout[n*16+10] += - s[19] + s[21];
gout[n*16+11] += 0;
gout[n*16+12] += - s[0] - s[4] - s[8];
gout[n*16+13] += - s[9] - s[13] - s[17];
gout[n*16+14] += - s[18] - s[22] - s[26];
gout[n*16+15] += 0;
}}}
void int2e_vsp1spsp2_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {0, 1, 1, 1, 3, 4, 4, 1};
CINTall_2e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int2e_vsp1spsp2_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 1, 1, 1, 3, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_vsp1spsp2;
return CINT2e_cart_drv(out, dims, &envs, opt, cache);
} // int2e_vsp1spsp2_cart
int int2e_vsp1spsp2_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 1, 1, 1, 3, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_vsp1spsp2;
return CINT2e_spheric_drv(out, dims, &envs, opt, cache);
} // int2e_vsp1spsp2_sph
int int2e_vsp1spsp2_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {0, 1, 1, 1, 3, 4, 4, 1};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_vsp1spsp2;
return CINT2e_spinor_drv(out, dims, &envs, opt, cache, &c2s_si_2e1, &c2s_si_2e2);
} // int2e_vsp1spsp2_spinor
ALL_CINT(int2e_vsp1spsp2)
ALL_CINT_FORTRAN_(int2e_vsp1spsp2)
