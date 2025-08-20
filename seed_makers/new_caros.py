import os
import argparse
import random

# C code's common.h constants
CONF_SIZE = 16
IDX_VAL_SIZE = 1
PUBLIC_ARRAY_SIZE = 4
SECRET_ARRAY_SIZE = 4
LENGTH = 4

# ==============================================================================
# FINAL FIX: Instead of complex inverse calculations, we use a "perfect ratio"
# that guarantees the desired layout when parsed by the C code.
#
# Our target layout for the data part (13 bytes total):
# - Private Pool: 4 bytes (for secret_array)
# - Public Pool: 9 bytes (1 for idx_val, 4 for public_array, 4 unused)
#
# C code calculates: priv_size = (priv_ratio * 13) / 256
# To get priv_size = 4, `priv_ratio` must be between 79 and 98.
# We will use a stable middle value: 88.
# ==============================================================================
PERFECT_PRIV_RATIO = 88

def generate_seed_file(
    idx_val: int,
    public_array: bytes,
    secret_array: bytes
) -> bytes:
    """
    Generates a complete binary seed file with a guaranteed layout.
    """
    public_pool = idx_val.to_bytes(IDX_VAL_SIZE, 'little') + public_array
    private_pool = secret_array
    
    # In our new logic, the public pool might have extra padding bytes
    # to make the layout more stable for the fuzzer.
    # Let's define the total data size to be stable.
    # Total data = 4 (secret) + 1 (idx) + 4 (public_array) = 9 bytes
    # Let's add some padding to make it, for example, 13 bytes total.
    padding_size = 4
    public_pool += os.urandom(padding_size) # Add random padding

    config = bytearray(CONF_SIZE)
    config[0] = PERFECT_PRIV_RATIO

    # Assemble the final file in the order the C parser expects:
    # [Config][Private Pool][Public Pool]
    final_data = bytes(config) + private_pool + public_pool
    
    return final_data

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Generate seed files for the fuzzing target.")
    # ... (the rest of the main function is identical to the English version) ...
    # ... I will copy it here for completeness ...
    parser.add_argument(
        "-o", "--output_dir",
        type=str,
        default="seeds",
        help="Directory to save the generated seed files."
    )
    parser.add_argument(
        "-n", "--num_seeds",
        type=int,
        default=10,
        help="Number of seed files to generate."
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    print(f"Generating {args.num_seeds} seed files in '{args.output_dir}' directory...")

    for i in range(args.num_seeds):
        if random.random() < 0.8:
            idx_val = random.randint(0, LENGTH - 1)
        else:
            idx_val = random.randint(LENGTH, 255)
            
        public_array = bytearray(os.urandom(PUBLIC_ARRAY_SIZE))
        if random.random() < 0.8 and public_array[0] == 0:
            public_array[0] = random.randint(1, 255)
            
        secret_array = os.urandom(SECRET_ARRAY_SIZE)

        seed_data = generate_seed_file(idx_val, bytes(public_array), secret_array)
        
        file_path = os.path.join(args.output_dir, f"seed_{i:03d}.bin")
        with open(file_path, 'wb') as f:
            f.write(seed_data)

    print("Seed generation complete.")

if __name__ == "__main__":
    main()
