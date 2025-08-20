///
/// File: runner.c
///
// Copyright (C) Microsoft Corporation
// SPDX-License-Identifier: MIT

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "common.h"
#include "driver.h"

/// ================================================================================================
/// Interfaces to SymCrypt functions, selected based on the configuration file
/// ================================================================================================
int run_test(input_t *config_ptr, input_t *idx, input_t *public_arr, input_t *secret_arr, uint8_t *output)
{
    // Convert input_t to actual arrays
    uint8_t idx_val = idx->data[0];
    uint8_t public_array[4];
    uint8_t secret_array[4];
    memcpy(public_array, public_arr->data, 4);
    memcpy(secret_array, secret_arr->data, 4);
    // Inline magic_func implementation
    output[0] = 0;
    if (idx_val < 4) {
        secret_array[idx_val] = secret_array[0];  // Side-channel: memory access pattern depends on idx
        //uint64_t x = ;
        if (public_array[0]) {                                  // Side-channel: branch depends on public data
            output[0] = 1;
        }
    }
    return 0; // unreachable
}