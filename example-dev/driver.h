///
/// File:
///
// Copyright (C) Microsoft Corporation
// SPDX-License-Identifier: MIT

#ifndef DRIVER_H
#define DRIVER_H

#include <stdlib.h>

#include "common.h"


/// ================================================================================================
/// Interfaces
/// ================================================================================================
int run_test(input_t *config_ptr, input_t *iv, input_t *key, input_t *plaintext, uint8_t *output);


#endif // DRIVER_H
