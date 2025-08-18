import struct
import os

def create_seed_file(filename, priv_ratio, iv_data, key_data, plaintext_data):
    """Create a seed file with proper driver_config_t structure"""
    
    # Create proper driver_config_t structure (16 bytes total)
    # First 2 bytes: priv_ratio, cypher_type=0, emulation_mode=0
    byte1 = priv_ratio  # priv_ratio
    byte2 = 0           # cypher_type (4 bits) + emulation_mode (4 bits)
    
    # Next 6 bytes: unused (48 bits)
    unused = b'\x00' * 6
    
    # Last 8 bytes: cypher_rnd
    cypher_rnd = struct.pack('<Q', 0)
    
    # Combine to make 16-byte config
    config = struct.pack('<BB', byte1, byte2) + unused + cypher_rnd
    
    # Create the complete file
    file_data = config + iv_data + key_data + plaintext_data
    
    with open(filename, 'wb') as f:
        f.write(file_data)
    
    return len(file_data)

# Configuration
priv_ratio = 200  # 200/255 ≈ 78% private area

# Create multiple seed files
seeds = [
    {
        'filename': 'seed1.bin',
        'iv': b'\x00' * 16,
        'key': b'\x01' * 16,
        'plaintext': b'A' * 48
    },
    {
        'filename': 'seed2.bin', 
        'iv': b'\xff' * 16,
        'key': b'\x42' * 16,
        'plaintext': b'B' * 48
    },
    {
        'filename': 'seed3.bin',
        'iv': b'\x55' * 16,
        'key': b'\xaa' * 16,
        'plaintext': b'TestData' * 6  # 48 bytes
    }
]

print("Creating seed files...")
for seed in seeds:
    size = create_seed_file(
        seed['filename'],
        priv_ratio,
        seed['iv'],
        seed['key'], 
        seed['plaintext']
    )
    print(f"Created {seed['filename']}: {size} bytes")

# Verify calculations
total_data_size = 80  # Total size minus config (96 - 16)
priv_size = (priv_ratio * total_data_size) // 255
pub_size = total_data_size - priv_size

print(f"\nCalculations:")
print(f"Total file size: 96 bytes")
print(f"Config: 16 bytes")
print(f"Data area: {total_data_size} bytes")
print(f"Private area: {priv_size} bytes (key=16 + plaintext=16+ = 32+ needed)")
print(f"Public area: {pub_size} bytes (iv=16 needed)")

# Verify structure
null_bytes = b'\x00' * 6
config_size = len(struct.pack('<BB', priv_ratio, 0) + null_bytes + struct.pack('<Q', 0))
print(f"\nStructure verification:")
print(f"- Config size should be 16: {config_size}")
print(f"- Private area has enough space: {priv_size >= 32}")
print(f"- Public area has enough space: {pub_size >= 16}")

print(f"\nTest your seeds with:")
print(f"~/works/repo/example -p ~/works/repo/policy.txt -o /tmp/test -d seed1.bin")
