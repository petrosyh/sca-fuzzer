import os
import argparse
import random

# Constants matching those in the C code's common.h
CONF_SIZE = 16
IDX_VAL_SIZE = 1
PUBLIC_ARRAY_SIZE = 4
SECRET_ARRAY_SIZE = 4
LENGTH = 4

def generate_seed_file(
    idx_val: int,
    public_array: bytes,
    secret_array: bytes
) -> bytes:
    """
    Generates a complete binary seed file that the C program can parse,
    based on the given input values.
    """
    # 1. Construct the Public and Private data pools.
    # According to the policy, idx and public_array belong to the Public pool.
    public_pool = idx_val.to_bytes(IDX_VAL_SIZE, 'little') + public_array
    
    # secret_array belongs to the Private pool.
    private_pool = secret_array

    # 2. Calculate priv_ratio, which is the first byte of the config data.
    total_data_size = len(public_pool) + len(private_pool)
    
    # Inversely calculate priv_ratio from the formula:
    # priv_size = (priv_ratio * total_data_size) / 256
    # To compensate for the rounding errors caused by integer division in the C code,
    # we calculate the ceiling of the division.
    # The formula for ceiling division using only integer arithmetic is:
    # (numerator + denominator - 1) // denominator
    numerator = len(private_pool) * 256
    denominator = total_data_size
    
    priv_ratio = (numerator + denominator - 1) // denominator if denominator else 0

    # 3. Create the 16-byte config data.
    config = bytearray(CONF_SIZE)
    if priv_ratio > 255:
        # This case can occur if total_data_size is very small,
        # but it shouldn't happen with our seeds. Added as a safeguard.
        priv_ratio = 255
    config[0] = priv_ratio
    
    # 4. Assemble the final file in the order the C program expects to parse it.
    # [Config][Private Pool][Public Pool]
    final_data = bytes(config) + private_pool + public_pool
    
    return final_data

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Generate seed files for the fuzzing target.")
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

    # Create the output directory
    os.makedirs(args.output_dir, exist_ok=True)
    print(f"Generating {args.num_seeds} seed files in '{args.output_dir}' directory...")

    for i in range(args.num_seeds):
        # Generate random values that are likely to be "good" seeds.
        # idx_val executes a more interesting path when its value is less than LENGTH.
        # Generate a value between 0-3 with 80% probability, and a larger value with 20% probability.
        if random.random() < 0.8:
            idx_val = random.randint(0, LENGTH - 1)
        else:
            idx_val = random.randint(LENGTH, 255)
            
        # The program takes an interesting path when the first byte of public_array is non-zero.
        # Ensure the first byte is non-zero with 80% probability.
        public_array = bytearray(os.urandom(PUBLIC_ARRAY_SIZE))
        if random.random() < 0.8 and public_array[0] == 0:
            public_array[0] = random.randint(1, 255)
            
        secret_array = os.urandom(SECRET_ARRAY_SIZE)

        # Generate the seed file data
        seed_data = generate_seed_file(idx_val, bytes(public_array), secret_array)
        
        # Save to file
        file_path = os.path.join(args.output_dir, f"seed_{i:03d}.bin")
        with open(file_path, 'wb') as f:
            f.write(seed_data)

    print("Seed generation complete.")
    print(f"Example command to start AFL: afl-fuzz -i {args.output_dir} -o findings -- ./example -p policy.txt -o out.bin -d @@")


if __name__ == "__main__":
    main()