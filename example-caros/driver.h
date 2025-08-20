///
/// File:
///
// Copyright (C) Microsoft Corporation
// SPDX-License-Identifier: MIT

#ifndef DRIVER_H
#define DRIVER_H

#include <stdlib.h>
#include "common.h"
#include <stdint.h>

/// ================================================================================================
/// Interfaces
/// ================================================================================================
int run_test(input_t *config_ptr, input_t *public_arr, input_t *secret_arr, input_t *idx, uint8_t *output);


#endif // DRIVER_H
