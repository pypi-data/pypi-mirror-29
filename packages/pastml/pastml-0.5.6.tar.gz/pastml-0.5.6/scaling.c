//
// Created by azhukova on 2/22/18.
//



#include <stdio.h>
#include "pastml.h"

int get_scaling_pow(double value) {
    return (int) (POW * LOG2 - log(value)) / LOG2;
}

int upscale_node_probs(double* array, size_t n) {
    /**
     * The rescaling is done to avoid underflow problems:
     * if a certain node probability is too small, we multiply this node probabilities by a scaling factor,
     * and keep the factor in mind to remove it from the final likelihood.
     */

    /* find the smallest non-zero probability */
    double smallest = 1.1;
    size_t i;

    for (i = 0; i < n; i++) {
        if (array[i] > 0.0 && array[i] < smallest) {
            smallest = array[i];
        }
    }

    if (smallest == 1.1) {
        return -1;
    }

    int factors = 0;

    if (smallest < LIM_P) {
        int curr_scaler_pow = get_scaling_pow(smallest);
        int piecewise_scaler_pow;
        double curr_scaler;

        factors = curr_scaler_pow;
        do {
            piecewise_scaler_pow = MIN(curr_scaler_pow, 63);
            curr_scaler = ((unsigned long long) (1) << piecewise_scaler_pow);
            for (i = 0; i < n; i++) {
                array[i] *= curr_scaler;
            }
            curr_scaler_pow -= piecewise_scaler_pow;
        } while (curr_scaler_pow != 0);
    }
    return factors;
}

void rescale(double *array, int i, int curr_scaler_pow) {
    int piecewise_scaler_pow;
    unsigned long long curr_scaler;
    do {
        piecewise_scaler_pow = MIN(curr_scaler_pow, 63);
        curr_scaler = ((unsigned long long) (1) << piecewise_scaler_pow);
        array[i] *= curr_scaler;
        curr_scaler_pow -= piecewise_scaler_pow;
    } while (curr_scaler_pow != 0);
}