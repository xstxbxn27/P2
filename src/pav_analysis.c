#include <math.h>
#include "pav_analysis.h"

float hamming_window(int n, int M) {
    return (float) 0.54 - 0.46*cos((2*M_PI*n)/(M-1));
}

float compute_power_window(const float *x, unsigned int N, const float *w) {
    float pot_num = 1e-12; //Para evitar indeterminación
    float pot_den = 1e-12;
    for(unsigned int n=0; n < N; n++){
        pot_num += (x[n]*w[n])*(x[n]*w[n]);
        pot_den += w[n]*w[n];
    }
    return 10*log10(pot_num/pot_den);
}


float compute_power(const float *x, unsigned int N) {
    float res = 1e-12; 
    for(unsigned int i=0;i<N;i++) {
        res += x[i]*x[i];
    }
    return (10*log10(res/N));
}

float compute_am(const float *x, unsigned int N) {
    float res = 0;
    for(unsigned int i=0;i<N;i++) {
        res += fabs(x[i]);
    }
    return res/N;
}

float compute_zcr(const float *x, unsigned int N, float fm) {
    int cont = 0;
    for(unsigned int i=1;i<N;i++) {
        if(x[i]*x[i-1]<0) { 
            //Si el resultado de la multiplicación es negativo, entonces tienen el signo distinto.
            cont++;
        }
    }
    return (fm/2.0)*(1.0/(N-1.0))*cont;
}