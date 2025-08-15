///
/// File: common.h
///       Common header file for fuzzing drivers, establishing interfaces and types
///
// Copyright (C) Microsoft Corporation
// SPDX-License-Identifier: MIT

#ifndef DRIVER_COMMON_H
#define DRIVER_COMMON_H

#include <stdint.h>
#include <stdlib.h>

/// ================================================================================================
/// Custom Types
/// ================================================================================================
typedef enum : char {
    FUZZ_MODE_CONFIDENTIALITY = 0, // Confidentiality mode
    FUZZ_MODE_INTEGRITY,           // Integrity mode
    FUZZ_MODE_INVALID              // Invalid mode
} fuzzing_mode_t;

typedef struct {
    unsigned char priv_ratio : 8;     ///< Ratio of public to private data in the input
                                      /// E.g., if the value is 0x01, it means that
                                      /// 1/256 of the input is private. Then, if the
                                      /// input is 1024 bytes, the first 4 bytes are private
                                      /// data, and the rest is public data.
    unsigned char cypher_type : 4;    ///< Type of cypher (e.g., AES, DSA)
    unsigned char emulation_mode : 4; ///< Emulation mode for CPU features
    uint64_t unused : 48;             ///< Unused bits for future expansion
    uint64_t cypher_rnd; ///< Source of randomness for selecting cypher-specific parameters
} __attribute__((packed)) driver_config_t;

typedef struct {
    const uint8_t *data;
    size_t size;
} input_t;

#define _IN
#define _OUT

/// ================================================================================================
/// Constants
/// ================================================================================================
#define MIN_PLAINTEXT_SIZE (16)
#define MAX_PLAINTEXT_SIZE (1024 * 1024)
#define KEY_SIZE           (16)
#define IV_SIZE            (16)
#define CONF_SIZE          (sizeof(driver_config_t))

#define MIN_TOTAL_SIZE (MIN_PLAINTEXT_SIZE + KEY_SIZE + IV_SIZE + CONF_SIZE)
#define MAX_TOTAL_SIZE (MAX_PLAINTEXT_SIZE + KEY_SIZE + IV_SIZE + CONF_SIZE)

// Size of the new stack to be created for the wrapper function
#define STACK_SIZE (16 * 4096)

// Maximum value of the priv_ratio field in the driver_config_t structure
#define MAX_PRIV_RATIO (0xFF)

/// ================================================================================================
/// Interfaces
/// ================================================================================================
void *get_new_stack(size_t stack_size);
int runner_outer(input_t *config, input_t *iv, input_t *key, input_t *plaintext, uint8_t *output,
                 const void *new_stack);

#endif // DRIVER_COMMON_H