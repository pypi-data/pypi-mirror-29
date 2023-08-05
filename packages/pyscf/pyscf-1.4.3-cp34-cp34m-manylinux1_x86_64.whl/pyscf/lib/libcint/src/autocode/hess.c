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
/* <NABLA NABLA i|OVLP |j> */
static void CINTgout1e_int1e_ipipovlp(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int ix, iy, iz, n;
double *g0 = g;
double *g1 = g0  + envs->g_size * 3;
double *g2 = g1  + envs->g_size * 3;
double *g3 = g2  + envs->g_size * 3;
double s[9];
G1E_D_I(g1, g0, envs->i_l+1, envs->j_l, 0);
G1E_D_I(g2, g0, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g3, g1, envs->i_l+0, envs->j_l, 0);
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
s[0] = + g3[ix+0]*g0[iy+0]*g0[iz+0];
s[1] = + g2[ix+0]*g1[iy+0]*g0[iz+0];
s[2] = + g2[ix+0]*g0[iy+0]*g1[iz+0];
s[3] = + g1[ix+0]*g2[iy+0]*g0[iz+0];
s[4] = + g0[ix+0]*g3[iy+0]*g0[iz+0];
s[5] = + g0[ix+0]*g2[iy+0]*g1[iz+0];
s[6] = + g1[ix+0]*g0[iy+0]*g2[iz+0];
s[7] = + g0[ix+0]*g1[iy+0]*g2[iz+0];
s[8] = + g0[ix+0]*g0[iy+0]*g3[iz+0];
gout[n*9+0] += + s[0];
gout[n*9+1] += + s[3];
gout[n*9+2] += + s[6];
gout[n*9+3] += + s[1];
gout[n*9+4] += + s[4];
gout[n*9+5] += + s[7];
gout[n*9+6] += + s[2];
gout[n*9+7] += + s[5];
gout[n*9+8] += + s[8];
}}
void int1e_ipipovlp_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {2, 0, 0, 0, 2, 1, 1, 9};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_ipipovlp_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 0, 0, 0, 2, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipipovlp;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 0);
} // int1e_ipipovlp_cart
int int1e_ipipovlp_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 0, 0, 0, 2, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipipovlp;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 0);
} // int1e_ipipovlp_sph
int int1e_ipipovlp_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 0, 0, 0, 2, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipipovlp;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_sf_1e, 0);
} // int1e_ipipovlp_spinor
ALL_CINT1E(int1e_ipipovlp)
ALL_CINT1E_FORTRAN_(int1e_ipipovlp)
/* <NABLA i|OVLP |NABLA j> */
static void CINTgout1e_int1e_ipovlpip(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int ix, iy, iz, n;
double *g0 = g;
double *g1 = g0  + envs->g_size * 3;
double *g2 = g1  + envs->g_size * 3;
double *g3 = g2  + envs->g_size * 3;
double s[9];
G1E_D_J(g1, g0, envs->i_l+1, envs->j_l+0, 0);
G1E_D_I(g2, g0, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g3, g1, envs->i_l+0, envs->j_l, 0);
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
s[0] = + g3[ix+0]*g0[iy+0]*g0[iz+0];
s[1] = + g2[ix+0]*g1[iy+0]*g0[iz+0];
s[2] = + g2[ix+0]*g0[iy+0]*g1[iz+0];
s[3] = + g1[ix+0]*g2[iy+0]*g0[iz+0];
s[4] = + g0[ix+0]*g3[iy+0]*g0[iz+0];
s[5] = + g0[ix+0]*g2[iy+0]*g1[iz+0];
s[6] = + g1[ix+0]*g0[iy+0]*g2[iz+0];
s[7] = + g0[ix+0]*g1[iy+0]*g2[iz+0];
s[8] = + g0[ix+0]*g0[iy+0]*g3[iz+0];
gout[n*9+0] += + s[0];
gout[n*9+1] += + s[1];
gout[n*9+2] += + s[2];
gout[n*9+3] += + s[3];
gout[n*9+4] += + s[4];
gout[n*9+5] += + s[5];
gout[n*9+6] += + s[6];
gout[n*9+7] += + s[7];
gout[n*9+8] += + s[8];
}}
void int1e_ipovlpip_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {1, 1, 0, 0, 2, 1, 1, 9};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_ipovlpip_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 1, 0, 0, 2, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipovlpip;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 0);
} // int1e_ipovlpip_cart
int int1e_ipovlpip_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 1, 0, 0, 2, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipovlpip;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 0);
} // int1e_ipovlpip_sph
int int1e_ipovlpip_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 1, 0, 0, 2, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipovlpip;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_sf_1e, 0);
} // int1e_ipovlpip_spinor
ALL_CINT1E(int1e_ipovlpip)
ALL_CINT1E_FORTRAN_(int1e_ipovlpip)
/* <NABLA NABLA i|P DOT P |j> */
static void CINTgout1e_int1e_ipipkin(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
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
double *g8 = g7  + envs->g_size * 3;
double *g9 = g8  + envs->g_size * 3;
double *g10 = g9  + envs->g_size * 3;
double *g11 = g10  + envs->g_size * 3;
double *g12 = g11  + envs->g_size * 3;
double *g13 = g12  + envs->g_size * 3;
double *g14 = g13  + envs->g_size * 3;
double *g15 = g14  + envs->g_size * 3;
double s[81];
G1E_D_J(g1, g0, envs->i_l+2, envs->j_l+0, 0);
G1E_D_J(g2, g0, envs->i_l+2, envs->j_l+1, 0);
G1E_D_J(g3, g2, envs->i_l+2, envs->j_l+0, 0);
G1E_D_I(g4, g0, envs->i_l+1, envs->j_l, 0);
G1E_D_I(g5, g1, envs->i_l+1, envs->j_l, 0);
G1E_D_I(g6, g2, envs->i_l+1, envs->j_l, 0);
G1E_D_I(g7, g3, envs->i_l+1, envs->j_l, 0);
G1E_D_I(g8, g0, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g9, g1, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g10, g2, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g11, g3, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g12, g4, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g13, g5, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g14, g6, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g15, g7, envs->i_l+0, envs->j_l, 0);
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
s[0] = + g15[ix+0]*g0[iy+0]*g0[iz+0];
s[1] = + g14[ix+0]*g1[iy+0]*g0[iz+0];
s[2] = + g14[ix+0]*g0[iy+0]*g1[iz+0];
s[3] = + g13[ix+0]*g2[iy+0]*g0[iz+0];
s[4] = + g12[ix+0]*g3[iy+0]*g0[iz+0];
s[5] = + g12[ix+0]*g2[iy+0]*g1[iz+0];
s[6] = + g13[ix+0]*g0[iy+0]*g2[iz+0];
s[7] = + g12[ix+0]*g1[iy+0]*g2[iz+0];
s[8] = + g12[ix+0]*g0[iy+0]*g3[iz+0];
s[9] = + g11[ix+0]*g4[iy+0]*g0[iz+0];
s[10] = + g10[ix+0]*g5[iy+0]*g0[iz+0];
s[11] = + g10[ix+0]*g4[iy+0]*g1[iz+0];
s[12] = + g9[ix+0]*g6[iy+0]*g0[iz+0];
s[13] = + g8[ix+0]*g7[iy+0]*g0[iz+0];
s[14] = + g8[ix+0]*g6[iy+0]*g1[iz+0];
s[15] = + g9[ix+0]*g4[iy+0]*g2[iz+0];
s[16] = + g8[ix+0]*g5[iy+0]*g2[iz+0];
s[17] = + g8[ix+0]*g4[iy+0]*g3[iz+0];
s[18] = + g11[ix+0]*g0[iy+0]*g4[iz+0];
s[19] = + g10[ix+0]*g1[iy+0]*g4[iz+0];
s[20] = + g10[ix+0]*g0[iy+0]*g5[iz+0];
s[21] = + g9[ix+0]*g2[iy+0]*g4[iz+0];
s[22] = + g8[ix+0]*g3[iy+0]*g4[iz+0];
s[23] = + g8[ix+0]*g2[iy+0]*g5[iz+0];
s[24] = + g9[ix+0]*g0[iy+0]*g6[iz+0];
s[25] = + g8[ix+0]*g1[iy+0]*g6[iz+0];
s[26] = + g8[ix+0]*g0[iy+0]*g7[iz+0];
s[27] = + g7[ix+0]*g8[iy+0]*g0[iz+0];
s[28] = + g6[ix+0]*g9[iy+0]*g0[iz+0];
s[29] = + g6[ix+0]*g8[iy+0]*g1[iz+0];
s[30] = + g5[ix+0]*g10[iy+0]*g0[iz+0];
s[31] = + g4[ix+0]*g11[iy+0]*g0[iz+0];
s[32] = + g4[ix+0]*g10[iy+0]*g1[iz+0];
s[33] = + g5[ix+0]*g8[iy+0]*g2[iz+0];
s[34] = + g4[ix+0]*g9[iy+0]*g2[iz+0];
s[35] = + g4[ix+0]*g8[iy+0]*g3[iz+0];
s[36] = + g3[ix+0]*g12[iy+0]*g0[iz+0];
s[37] = + g2[ix+0]*g13[iy+0]*g0[iz+0];
s[38] = + g2[ix+0]*g12[iy+0]*g1[iz+0];
s[39] = + g1[ix+0]*g14[iy+0]*g0[iz+0];
s[40] = + g0[ix+0]*g15[iy+0]*g0[iz+0];
s[41] = + g0[ix+0]*g14[iy+0]*g1[iz+0];
s[42] = + g1[ix+0]*g12[iy+0]*g2[iz+0];
s[43] = + g0[ix+0]*g13[iy+0]*g2[iz+0];
s[44] = + g0[ix+0]*g12[iy+0]*g3[iz+0];
s[45] = + g3[ix+0]*g8[iy+0]*g4[iz+0];
s[46] = + g2[ix+0]*g9[iy+0]*g4[iz+0];
s[47] = + g2[ix+0]*g8[iy+0]*g5[iz+0];
s[48] = + g1[ix+0]*g10[iy+0]*g4[iz+0];
s[49] = + g0[ix+0]*g11[iy+0]*g4[iz+0];
s[50] = + g0[ix+0]*g10[iy+0]*g5[iz+0];
s[51] = + g1[ix+0]*g8[iy+0]*g6[iz+0];
s[52] = + g0[ix+0]*g9[iy+0]*g6[iz+0];
s[53] = + g0[ix+0]*g8[iy+0]*g7[iz+0];
s[54] = + g7[ix+0]*g0[iy+0]*g8[iz+0];
s[55] = + g6[ix+0]*g1[iy+0]*g8[iz+0];
s[56] = + g6[ix+0]*g0[iy+0]*g9[iz+0];
s[57] = + g5[ix+0]*g2[iy+0]*g8[iz+0];
s[58] = + g4[ix+0]*g3[iy+0]*g8[iz+0];
s[59] = + g4[ix+0]*g2[iy+0]*g9[iz+0];
s[60] = + g5[ix+0]*g0[iy+0]*g10[iz+0];
s[61] = + g4[ix+0]*g1[iy+0]*g10[iz+0];
s[62] = + g4[ix+0]*g0[iy+0]*g11[iz+0];
s[63] = + g3[ix+0]*g4[iy+0]*g8[iz+0];
s[64] = + g2[ix+0]*g5[iy+0]*g8[iz+0];
s[65] = + g2[ix+0]*g4[iy+0]*g9[iz+0];
s[66] = + g1[ix+0]*g6[iy+0]*g8[iz+0];
s[67] = + g0[ix+0]*g7[iy+0]*g8[iz+0];
s[68] = + g0[ix+0]*g6[iy+0]*g9[iz+0];
s[69] = + g1[ix+0]*g4[iy+0]*g10[iz+0];
s[70] = + g0[ix+0]*g5[iy+0]*g10[iz+0];
s[71] = + g0[ix+0]*g4[iy+0]*g11[iz+0];
s[72] = + g3[ix+0]*g0[iy+0]*g12[iz+0];
s[73] = + g2[ix+0]*g1[iy+0]*g12[iz+0];
s[74] = + g2[ix+0]*g0[iy+0]*g13[iz+0];
s[75] = + g1[ix+0]*g2[iy+0]*g12[iz+0];
s[76] = + g0[ix+0]*g3[iy+0]*g12[iz+0];
s[77] = + g0[ix+0]*g2[iy+0]*g13[iz+0];
s[78] = + g1[ix+0]*g0[iy+0]*g14[iz+0];
s[79] = + g0[ix+0]*g1[iy+0]*g14[iz+0];
s[80] = + g0[ix+0]*g0[iy+0]*g15[iz+0];
gout[n*9+0] += - s[0] - s[4] - s[8];
gout[n*9+1] += - s[27] - s[31] - s[35];
gout[n*9+2] += - s[54] - s[58] - s[62];
gout[n*9+3] += - s[9] - s[13] - s[17];
gout[n*9+4] += - s[36] - s[40] - s[44];
gout[n*9+5] += - s[63] - s[67] - s[71];
gout[n*9+6] += - s[18] - s[22] - s[26];
gout[n*9+7] += - s[45] - s[49] - s[53];
gout[n*9+8] += - s[72] - s[76] - s[80];
}}
void int1e_ipipkin_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {2, 2, 0, 0, 4, 1, 1, 9};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_ipipkin_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 2, 0, 0, 4, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipipkin;
envs.common_factor *= 0.5;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 0);
} // int1e_ipipkin_cart
int int1e_ipipkin_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 2, 0, 0, 4, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipipkin;
envs.common_factor *= 0.5;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 0);
} // int1e_ipipkin_sph
int int1e_ipipkin_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 2, 0, 0, 4, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipipkin;
envs.common_factor *= 0.5;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_sf_1e, 0);
} // int1e_ipipkin_spinor
ALL_CINT1E(int1e_ipipkin)
ALL_CINT1E_FORTRAN_(int1e_ipipkin)
/* <NABLA i|P DOT P |NABLA j> */
static void CINTgout1e_int1e_ipkinip(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
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
double *g8 = g7  + envs->g_size * 3;
double *g9 = g8  + envs->g_size * 3;
double *g10 = g9  + envs->g_size * 3;
double *g11 = g10  + envs->g_size * 3;
double *g12 = g11  + envs->g_size * 3;
double *g13 = g12  + envs->g_size * 3;
double *g14 = g13  + envs->g_size * 3;
double *g15 = g14  + envs->g_size * 3;
double s[81];
G1E_D_J(g1, g0, envs->i_l+1, envs->j_l+0, 0);
G1E_D_J(g2, g0, envs->i_l+1, envs->j_l+1, 0);
G1E_D_J(g3, g2, envs->i_l+1, envs->j_l+0, 0);
G1E_D_J(g4, g0, envs->i_l+1, envs->j_l+2, 0);
G1E_D_J(g5, g4, envs->i_l+1, envs->j_l+0, 0);
G1E_D_J(g6, g4, envs->i_l+1, envs->j_l+1, 0);
G1E_D_J(g7, g6, envs->i_l+1, envs->j_l+0, 0);
G1E_D_I(g8, g0, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g9, g1, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g10, g2, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g11, g3, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g12, g4, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g13, g5, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g14, g6, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g15, g7, envs->i_l+0, envs->j_l, 0);
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
s[0] = + g15[ix+0]*g0[iy+0]*g0[iz+0];
s[1] = + g14[ix+0]*g1[iy+0]*g0[iz+0];
s[2] = + g14[ix+0]*g0[iy+0]*g1[iz+0];
s[3] = + g13[ix+0]*g2[iy+0]*g0[iz+0];
s[4] = + g12[ix+0]*g3[iy+0]*g0[iz+0];
s[5] = + g12[ix+0]*g2[iy+0]*g1[iz+0];
s[6] = + g13[ix+0]*g0[iy+0]*g2[iz+0];
s[7] = + g12[ix+0]*g1[iy+0]*g2[iz+0];
s[8] = + g12[ix+0]*g0[iy+0]*g3[iz+0];
s[9] = + g11[ix+0]*g4[iy+0]*g0[iz+0];
s[10] = + g10[ix+0]*g5[iy+0]*g0[iz+0];
s[11] = + g10[ix+0]*g4[iy+0]*g1[iz+0];
s[12] = + g9[ix+0]*g6[iy+0]*g0[iz+0];
s[13] = + g8[ix+0]*g7[iy+0]*g0[iz+0];
s[14] = + g8[ix+0]*g6[iy+0]*g1[iz+0];
s[15] = + g9[ix+0]*g4[iy+0]*g2[iz+0];
s[16] = + g8[ix+0]*g5[iy+0]*g2[iz+0];
s[17] = + g8[ix+0]*g4[iy+0]*g3[iz+0];
s[18] = + g11[ix+0]*g0[iy+0]*g4[iz+0];
s[19] = + g10[ix+0]*g1[iy+0]*g4[iz+0];
s[20] = + g10[ix+0]*g0[iy+0]*g5[iz+0];
s[21] = + g9[ix+0]*g2[iy+0]*g4[iz+0];
s[22] = + g8[ix+0]*g3[iy+0]*g4[iz+0];
s[23] = + g8[ix+0]*g2[iy+0]*g5[iz+0];
s[24] = + g9[ix+0]*g0[iy+0]*g6[iz+0];
s[25] = + g8[ix+0]*g1[iy+0]*g6[iz+0];
s[26] = + g8[ix+0]*g0[iy+0]*g7[iz+0];
s[27] = + g7[ix+0]*g8[iy+0]*g0[iz+0];
s[28] = + g6[ix+0]*g9[iy+0]*g0[iz+0];
s[29] = + g6[ix+0]*g8[iy+0]*g1[iz+0];
s[30] = + g5[ix+0]*g10[iy+0]*g0[iz+0];
s[31] = + g4[ix+0]*g11[iy+0]*g0[iz+0];
s[32] = + g4[ix+0]*g10[iy+0]*g1[iz+0];
s[33] = + g5[ix+0]*g8[iy+0]*g2[iz+0];
s[34] = + g4[ix+0]*g9[iy+0]*g2[iz+0];
s[35] = + g4[ix+0]*g8[iy+0]*g3[iz+0];
s[36] = + g3[ix+0]*g12[iy+0]*g0[iz+0];
s[37] = + g2[ix+0]*g13[iy+0]*g0[iz+0];
s[38] = + g2[ix+0]*g12[iy+0]*g1[iz+0];
s[39] = + g1[ix+0]*g14[iy+0]*g0[iz+0];
s[40] = + g0[ix+0]*g15[iy+0]*g0[iz+0];
s[41] = + g0[ix+0]*g14[iy+0]*g1[iz+0];
s[42] = + g1[ix+0]*g12[iy+0]*g2[iz+0];
s[43] = + g0[ix+0]*g13[iy+0]*g2[iz+0];
s[44] = + g0[ix+0]*g12[iy+0]*g3[iz+0];
s[45] = + g3[ix+0]*g8[iy+0]*g4[iz+0];
s[46] = + g2[ix+0]*g9[iy+0]*g4[iz+0];
s[47] = + g2[ix+0]*g8[iy+0]*g5[iz+0];
s[48] = + g1[ix+0]*g10[iy+0]*g4[iz+0];
s[49] = + g0[ix+0]*g11[iy+0]*g4[iz+0];
s[50] = + g0[ix+0]*g10[iy+0]*g5[iz+0];
s[51] = + g1[ix+0]*g8[iy+0]*g6[iz+0];
s[52] = + g0[ix+0]*g9[iy+0]*g6[iz+0];
s[53] = + g0[ix+0]*g8[iy+0]*g7[iz+0];
s[54] = + g7[ix+0]*g0[iy+0]*g8[iz+0];
s[55] = + g6[ix+0]*g1[iy+0]*g8[iz+0];
s[56] = + g6[ix+0]*g0[iy+0]*g9[iz+0];
s[57] = + g5[ix+0]*g2[iy+0]*g8[iz+0];
s[58] = + g4[ix+0]*g3[iy+0]*g8[iz+0];
s[59] = + g4[ix+0]*g2[iy+0]*g9[iz+0];
s[60] = + g5[ix+0]*g0[iy+0]*g10[iz+0];
s[61] = + g4[ix+0]*g1[iy+0]*g10[iz+0];
s[62] = + g4[ix+0]*g0[iy+0]*g11[iz+0];
s[63] = + g3[ix+0]*g4[iy+0]*g8[iz+0];
s[64] = + g2[ix+0]*g5[iy+0]*g8[iz+0];
s[65] = + g2[ix+0]*g4[iy+0]*g9[iz+0];
s[66] = + g1[ix+0]*g6[iy+0]*g8[iz+0];
s[67] = + g0[ix+0]*g7[iy+0]*g8[iz+0];
s[68] = + g0[ix+0]*g6[iy+0]*g9[iz+0];
s[69] = + g1[ix+0]*g4[iy+0]*g10[iz+0];
s[70] = + g0[ix+0]*g5[iy+0]*g10[iz+0];
s[71] = + g0[ix+0]*g4[iy+0]*g11[iz+0];
s[72] = + g3[ix+0]*g0[iy+0]*g12[iz+0];
s[73] = + g2[ix+0]*g1[iy+0]*g12[iz+0];
s[74] = + g2[ix+0]*g0[iy+0]*g13[iz+0];
s[75] = + g1[ix+0]*g2[iy+0]*g12[iz+0];
s[76] = + g0[ix+0]*g3[iy+0]*g12[iz+0];
s[77] = + g0[ix+0]*g2[iy+0]*g13[iz+0];
s[78] = + g1[ix+0]*g0[iy+0]*g14[iz+0];
s[79] = + g0[ix+0]*g1[iy+0]*g14[iz+0];
s[80] = + g0[ix+0]*g0[iy+0]*g15[iz+0];
gout[n*9+0] += - s[0] - s[12] - s[24];
gout[n*9+1] += - s[1] - s[13] - s[25];
gout[n*9+2] += - s[2] - s[14] - s[26];
gout[n*9+3] += - s[27] - s[39] - s[51];
gout[n*9+4] += - s[28] - s[40] - s[52];
gout[n*9+5] += - s[29] - s[41] - s[53];
gout[n*9+6] += - s[54] - s[66] - s[78];
gout[n*9+7] += - s[55] - s[67] - s[79];
gout[n*9+8] += - s[56] - s[68] - s[80];
}}
void int1e_ipkinip_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {1, 3, 0, 0, 4, 1, 1, 9};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_ipkinip_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 3, 0, 0, 4, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipkinip;
envs.common_factor *= 0.5;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 0);
} // int1e_ipkinip_cart
int int1e_ipkinip_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 3, 0, 0, 4, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipkinip;
envs.common_factor *= 0.5;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 0);
} // int1e_ipkinip_sph
int int1e_ipkinip_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 3, 0, 0, 4, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipkinip;
envs.common_factor *= 0.5;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_sf_1e, 0);
} // int1e_ipkinip_spinor
ALL_CINT1E(int1e_ipkinip)
ALL_CINT1E_FORTRAN_(int1e_ipkinip)
/* <NABLA NABLA i|NUC |j> */
static void CINTgout1e_int1e_ipipnuc(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int ix, iy, iz, n;
double *g0 = g;
double *g1 = g0  + envs->g_size * 3;
double *g2 = g1  + envs->g_size * 3;
double *g3 = g2  + envs->g_size * 3;
double s[9];
G1E_D_I(g1, g0, envs->i_l+1, envs->j_l, 0);
G1E_D_I(g2, g0, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g3, g1, envs->i_l+0, envs->j_l, 0);
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
s[0] = + g3[ix+0]*g0[iy+0]*g0[iz+0];
s[1] = + g2[ix+0]*g1[iy+0]*g0[iz+0];
s[2] = + g2[ix+0]*g0[iy+0]*g1[iz+0];
s[3] = + g1[ix+0]*g2[iy+0]*g0[iz+0];
s[4] = + g0[ix+0]*g3[iy+0]*g0[iz+0];
s[5] = + g0[ix+0]*g2[iy+0]*g1[iz+0];
s[6] = + g1[ix+0]*g0[iy+0]*g2[iz+0];
s[7] = + g0[ix+0]*g1[iy+0]*g2[iz+0];
s[8] = + g0[ix+0]*g0[iy+0]*g3[iz+0];
gout[n*9+0] += + s[0];
gout[n*9+1] += + s[3];
gout[n*9+2] += + s[6];
gout[n*9+3] += + s[1];
gout[n*9+4] += + s[4];
gout[n*9+5] += + s[7];
gout[n*9+6] += + s[2];
gout[n*9+7] += + s[5];
gout[n*9+8] += + s[8];
}}
void int1e_ipipnuc_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {2, 0, 0, 0, 2, 1, 0, 9};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_ipipnuc_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 0, 0, 0, 2, 1, 0, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipipnuc;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 2);
} // int1e_ipipnuc_cart
int int1e_ipipnuc_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 0, 0, 0, 2, 1, 0, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipipnuc;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 2);
} // int1e_ipipnuc_sph
int int1e_ipipnuc_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 0, 0, 0, 2, 1, 0, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipipnuc;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_sf_1e, 2);
} // int1e_ipipnuc_spinor
ALL_CINT1E(int1e_ipipnuc)
ALL_CINT1E_FORTRAN_(int1e_ipipnuc)
/* <NABLA i|NUC |NABLA j> */
static void CINTgout1e_int1e_ipnucip(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int ix, iy, iz, n;
double *g0 = g;
double *g1 = g0  + envs->g_size * 3;
double *g2 = g1  + envs->g_size * 3;
double *g3 = g2  + envs->g_size * 3;
double s[9];
G1E_D_J(g1, g0, envs->i_l+1, envs->j_l+0, 0);
G1E_D_I(g2, g0, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g3, g1, envs->i_l+0, envs->j_l, 0);
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
s[0] = + g3[ix+0]*g0[iy+0]*g0[iz+0];
s[1] = + g2[ix+0]*g1[iy+0]*g0[iz+0];
s[2] = + g2[ix+0]*g0[iy+0]*g1[iz+0];
s[3] = + g1[ix+0]*g2[iy+0]*g0[iz+0];
s[4] = + g0[ix+0]*g3[iy+0]*g0[iz+0];
s[5] = + g0[ix+0]*g2[iy+0]*g1[iz+0];
s[6] = + g1[ix+0]*g0[iy+0]*g2[iz+0];
s[7] = + g0[ix+0]*g1[iy+0]*g2[iz+0];
s[8] = + g0[ix+0]*g0[iy+0]*g3[iz+0];
gout[n*9+0] += + s[0];
gout[n*9+1] += + s[1];
gout[n*9+2] += + s[2];
gout[n*9+3] += + s[3];
gout[n*9+4] += + s[4];
gout[n*9+5] += + s[5];
gout[n*9+6] += + s[6];
gout[n*9+7] += + s[7];
gout[n*9+8] += + s[8];
}}
void int1e_ipnucip_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {1, 1, 0, 0, 2, 1, 0, 9};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_ipnucip_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 1, 0, 0, 2, 1, 0, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipnucip;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 2);
} // int1e_ipnucip_cart
int int1e_ipnucip_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 1, 0, 0, 2, 1, 0, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipnucip;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 2);
} // int1e_ipnucip_sph
int int1e_ipnucip_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 1, 0, 0, 2, 1, 0, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipnucip;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_sf_1e, 2);
} // int1e_ipnucip_spinor
ALL_CINT1E(int1e_ipnucip)
ALL_CINT1E_FORTRAN_(int1e_ipnucip)
/* <NABLA NABLA i|RINV |j> */
static void CINTgout1e_int1e_ipiprinv(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int ix, iy, iz, n;
double *g0 = g;
double *g1 = g0  + envs->g_size * 3;
double *g2 = g1  + envs->g_size * 3;
double *g3 = g2  + envs->g_size * 3;
double s[9];
G1E_D_I(g1, g0, envs->i_l+1, envs->j_l, 0);
G1E_D_I(g2, g0, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g3, g1, envs->i_l+0, envs->j_l, 0);
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
s[0] = + g3[ix+0]*g0[iy+0]*g0[iz+0];
s[1] = + g2[ix+0]*g1[iy+0]*g0[iz+0];
s[2] = + g2[ix+0]*g0[iy+0]*g1[iz+0];
s[3] = + g1[ix+0]*g2[iy+0]*g0[iz+0];
s[4] = + g0[ix+0]*g3[iy+0]*g0[iz+0];
s[5] = + g0[ix+0]*g2[iy+0]*g1[iz+0];
s[6] = + g1[ix+0]*g0[iy+0]*g2[iz+0];
s[7] = + g0[ix+0]*g1[iy+0]*g2[iz+0];
s[8] = + g0[ix+0]*g0[iy+0]*g3[iz+0];
gout[n*9+0] += + s[0];
gout[n*9+1] += + s[3];
gout[n*9+2] += + s[6];
gout[n*9+3] += + s[1];
gout[n*9+4] += + s[4];
gout[n*9+5] += + s[7];
gout[n*9+6] += + s[2];
gout[n*9+7] += + s[5];
gout[n*9+8] += + s[8];
}}
void int1e_ipiprinv_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {2, 0, 0, 0, 2, 1, 0, 9};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_ipiprinv_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 0, 0, 0, 2, 1, 0, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipiprinv;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 1);
} // int1e_ipiprinv_cart
int int1e_ipiprinv_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 0, 0, 0, 2, 1, 0, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipiprinv;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 1);
} // int1e_ipiprinv_sph
int int1e_ipiprinv_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 0, 0, 0, 2, 1, 0, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_ipiprinv;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_sf_1e, 1);
} // int1e_ipiprinv_spinor
ALL_CINT1E(int1e_ipiprinv)
ALL_CINT1E_FORTRAN_(int1e_ipiprinv)
/* <NABLA i|RINV |NABLA j> */
static void CINTgout1e_int1e_iprinvip(double *gout, double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int ix, iy, iz, n;
double *g0 = g;
double *g1 = g0  + envs->g_size * 3;
double *g2 = g1  + envs->g_size * 3;
double *g3 = g2  + envs->g_size * 3;
double s[9];
G1E_D_J(g1, g0, envs->i_l+1, envs->j_l+0, 0);
G1E_D_I(g2, g0, envs->i_l+0, envs->j_l, 0);
G1E_D_I(g3, g1, envs->i_l+0, envs->j_l, 0);
for (n = 0; n < nf; n++) {
ix = idx[0+n*3];
iy = idx[1+n*3];
iz = idx[2+n*3];
s[0] = + g3[ix+0]*g0[iy+0]*g0[iz+0];
s[1] = + g2[ix+0]*g1[iy+0]*g0[iz+0];
s[2] = + g2[ix+0]*g0[iy+0]*g1[iz+0];
s[3] = + g1[ix+0]*g2[iy+0]*g0[iz+0];
s[4] = + g0[ix+0]*g3[iy+0]*g0[iz+0];
s[5] = + g0[ix+0]*g2[iy+0]*g1[iz+0];
s[6] = + g1[ix+0]*g0[iy+0]*g2[iz+0];
s[7] = + g0[ix+0]*g1[iy+0]*g2[iz+0];
s[8] = + g0[ix+0]*g0[iy+0]*g3[iz+0];
gout[n*9+0] += + s[0];
gout[n*9+1] += + s[1];
gout[n*9+2] += + s[2];
gout[n*9+3] += + s[3];
gout[n*9+4] += + s[4];
gout[n*9+5] += + s[5];
gout[n*9+6] += + s[6];
gout[n*9+7] += + s[7];
gout[n*9+8] += + s[8];
}}
void int1e_iprinvip_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {1, 1, 0, 0, 2, 1, 0, 9};
CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int1e_iprinvip_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 1, 0, 0, 2, 1, 0, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_iprinvip;
return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 1);
} // int1e_iprinvip_cart
int int1e_iprinvip_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 1, 0, 0, 2, 1, 0, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_iprinvip;
return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 1);
} // int1e_iprinvip_sph
int int1e_iprinvip_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 1, 0, 0, 2, 1, 0, 9};
CINTEnvVars envs;
CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout1e_int1e_iprinvip;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_sf_1e, 1);
} // int1e_iprinvip_spinor
ALL_CINT1E(int1e_iprinvip)
ALL_CINT1E_FORTRAN_(int1e_iprinvip)
/* <k NABLA NABLA i|R12 |j l> : i,j \in electron 1; k,l \in electron 2
 * = (NABLA NABLA i j|R12 |k l) */
static void CINTgout2e_int2e_ipip1(double *gout,
double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int nrys_roots = envs->nrys_roots;
int ix, iy, iz, i, n;
double *g0 = g;
double *g1 = g0 + envs->g_size * 3;
double *g2 = g1 + envs->g_size * 3;
double *g3 = g2 + envs->g_size * 3;
G2E_D_I(g1, g0, envs->i_l+1, envs->j_l, envs->k_l, envs->l_l);
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
gout[n*9+0] = + s[0];
gout[n*9+1] = + s[3];
gout[n*9+2] = + s[6];
gout[n*9+3] = + s[1];
gout[n*9+4] = + s[4];
gout[n*9+5] = + s[7];
gout[n*9+6] = + s[2];
gout[n*9+7] = + s[5];
gout[n*9+8] = + s[8];
} else {
gout[n*9+0] += + s[0];
gout[n*9+1] += + s[3];
gout[n*9+2] += + s[6];
gout[n*9+3] += + s[1];
gout[n*9+4] += + s[4];
gout[n*9+5] += + s[7];
gout[n*9+6] += + s[2];
gout[n*9+7] += + s[5];
gout[n*9+8] += + s[8];
}}}
void int2e_ipip1_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {2, 0, 0, 0, 2, 1, 1, 9};
CINTall_2e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int2e_ipip1_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 0, 0, 0, 2, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_ipip1;
return CINT2e_cart_drv(out, dims, &envs, opt, cache);
} // int2e_ipip1_cart
int int2e_ipip1_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 0, 0, 0, 2, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_ipip1;
return CINT2e_spheric_drv(out, dims, &envs, opt, cache);
} // int2e_ipip1_sph
int int2e_ipip1_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {2, 0, 0, 0, 2, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_ipip1;
return CINT2e_spinor_drv(out, dims, &envs, opt, cache, &c2s_sf_2e1, &c2s_sf_2e2);
} // int2e_ipip1_spinor
ALL_CINT(int2e_ipip1)
ALL_CINT_FORTRAN_(int2e_ipip1)
/* <k NABLA i|R12 |NABLA j l> : i,j \in electron 1; k,l \in electron 2
 * = (NABLA i NABLA j|R12 |k l) */
static void CINTgout2e_int2e_ipvip1(double *gout,
double *g, int *idx, CINTEnvVars *envs, int gout_empty) {
int nf = envs->nf;
int nrys_roots = envs->nrys_roots;
int ix, iy, iz, i, n;
double *g0 = g;
double *g1 = g0 + envs->g_size * 3;
double *g2 = g1 + envs->g_size * 3;
double *g3 = g2 + envs->g_size * 3;
G2E_D_J(g1, g0, envs->i_l+1, envs->j_l+0, envs->k_l, envs->l_l);
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
gout[n*9+0] = + s[0];
gout[n*9+1] = + s[1];
gout[n*9+2] = + s[2];
gout[n*9+3] = + s[3];
gout[n*9+4] = + s[4];
gout[n*9+5] = + s[5];
gout[n*9+6] = + s[6];
gout[n*9+7] = + s[7];
gout[n*9+8] = + s[8];
} else {
gout[n*9+0] += + s[0];
gout[n*9+1] += + s[1];
gout[n*9+2] += + s[2];
gout[n*9+3] += + s[3];
gout[n*9+4] += + s[4];
gout[n*9+5] += + s[5];
gout[n*9+6] += + s[6];
gout[n*9+7] += + s[7];
gout[n*9+8] += + s[8];
}}}
void int2e_ipvip1_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {1, 1, 0, 0, 2, 1, 1, 9};
CINTall_2e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int2e_ipvip1_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 1, 0, 0, 2, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_ipvip1;
return CINT2e_cart_drv(out, dims, &envs, opt, cache);
} // int2e_ipvip1_cart
int int2e_ipvip1_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 1, 0, 0, 2, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_ipvip1;
return CINT2e_spheric_drv(out, dims, &envs, opt, cache);
} // int2e_ipvip1_sph
int int2e_ipvip1_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 1, 0, 0, 2, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_ipvip1;
return CINT2e_spinor_drv(out, dims, &envs, opt, cache, &c2s_sf_2e1, &c2s_sf_2e2);
} // int2e_ipvip1_spinor
ALL_CINT(int2e_ipvip1)
ALL_CINT_FORTRAN_(int2e_ipvip1)
/* <NABLA k NABLA i|R12 |j l> : i,j \in electron 1; k,l \in electron 2
 * = (NABLA i j|R12 |NABLA k l) */
static void CINTgout2e_int2e_ip1ip2(double *gout,
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
gout[n*9+0] = + s[0];
gout[n*9+1] = + s[1];
gout[n*9+2] = + s[2];
gout[n*9+3] = + s[3];
gout[n*9+4] = + s[4];
gout[n*9+5] = + s[5];
gout[n*9+6] = + s[6];
gout[n*9+7] = + s[7];
gout[n*9+8] = + s[8];
} else {
gout[n*9+0] += + s[0];
gout[n*9+1] += + s[1];
gout[n*9+2] += + s[2];
gout[n*9+3] += + s[3];
gout[n*9+4] += + s[4];
gout[n*9+5] += + s[5];
gout[n*9+6] += + s[6];
gout[n*9+7] += + s[7];
gout[n*9+8] += + s[8];
}}}
void int2e_ip1ip2_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env) {
int ng[] = {1, 0, 1, 0, 2, 1, 1, 9};
CINTall_2e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
int int2e_ip1ip2_cart(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 1, 0, 2, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_ip1ip2;
return CINT2e_cart_drv(out, dims, &envs, opt, cache);
} // int2e_ip1ip2_cart
int int2e_ip1ip2_sph(double *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 1, 0, 2, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_ip1ip2;
return CINT2e_spheric_drv(out, dims, &envs, opt, cache);
} // int2e_ip1ip2_sph
int int2e_ip1ip2_spinor(double complex *out, int *dims, int *shls,
int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt, double *cache) {
int ng[] = {1, 0, 1, 0, 2, 1, 1, 9};
CINTEnvVars envs;
CINTinit_int2e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
envs.f_gout = &CINTgout2e_int2e_ip1ip2;
return CINT2e_spinor_drv(out, dims, &envs, opt, cache, &c2s_sf_2e1, &c2s_sf_2e2);
} // int2e_ip1ip2_spinor
ALL_CINT(int2e_ip1ip2)
ALL_CINT_FORTRAN_(int2e_ip1ip2)
