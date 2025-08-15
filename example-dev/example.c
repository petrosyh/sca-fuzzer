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

#include "tiny-AES-c/aes.h"

/// ================================================================================================
/// Interfaces to SymCrypt functions, selected based on the configuration file
/// ================================================================================================
int run_test(input_t *config_ptr, input_t *iv, input_t *key, input_t *plaintext, uint8_t *output)
{
    driver_config_t *config = (driver_config_t *)config_ptr->data;

    struct AES_ctx aes = {0};

    AES_init_ctx_iv(&aes, key->data, iv->data);

    memcpy(output, plaintext->data, plaintext->size);

    AES_CBC_encrypt_buffer(&aes, output, plaintext->size);

    return 0; // unreachable
}