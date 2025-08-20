///
/// File: stabilizers.c
///       Stabilization wrappers to determinize DynamoRIO traces
///
// Copyright (C) Microsoft Corporation
// SPDX-License-Identifier: MIT

#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <stdint.h>

#include "driver.h"
#include "common.h"

/// @brief Create a new stack make stack-based operations independent of environmental variables
///        and command line arguments.
void *get_new_stack(size_t stack_size)
{
    const int permission_flags = PROT_READ | PROT_WRITE;
    const int map_flags = MAP_PRIVATE | MAP_ANONYMOUS;
    void *new_stack = mmap(NULL, stack_size, permission_flags, map_flags, -1, 0);
    if (new_stack == MAP_FAILED) {
        perror("mmap failed");
        return NULL;
    }
    return new_stack;
}

/// @brief Wrapper function that serves as an indicator to DynamoRIO
///        that it should start tracing from this point.
__attribute__((noinline)) int wrapper(input_t *config, input_t *idx, input_t *public_array,
                                      input_t *secret_array, uint8_t *output)
{
    return run_test(config, idx, public_array, secret_array, output);
}

/// @brief Pre-wrapper function that aims to stabilize the stack layout for the `wrapper` function.
///        It uses `mmap` to create a new stack and switches to it before calling `wrapper`.
/// @return 0 on success, non-zero on failure.
int runner_outer(input_t *config, input_t *idx, input_t *public_array, input_t *secret_array, uint8_t *output,
                 const void *new_stack)
{
    // Switch to the new stack, call `wrapper`, and restore the original stack after the call
    int result = 0;
    asm volatile(""
                 "pushq %%r8\n"
                 "movq %6, %%r8\n"
                 "pushq %%rbp\n"
                 "movq %%rsp, %%rbp\n"
                 "movq %1, %%rsp\n"
                 "pushq %%rbp\n"
                 "movq %%rsp, %%rbp\n"

                 // "sub $8, %%rsp\n" // align stack to 16 bytes

                 "pushq %6\n"
                 "pushq %5\n"
                 "pushq %4\n"
                 "pushq %3\n"
                 "pushq %2\n"

                 "callq %P7\n"

                 "add $5*8, %%rsp\n"

                 // "add $8, %%rsp\n"

                 "popq %%rbp\n"
                 "movq %%rbp, %%rsp\n"
                 "popq %%rbp\n"
                 "popq %%r8\n"

                 : "=A"(result)
                 : "r"(new_stack + STACK_SIZE), "r"(config), "r"(idx), "r"(public_array), "r"(secret_array),
                   "r"(output), "p"(wrapper)
                 : "memory");

    return result;
}
