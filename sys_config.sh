#!/bin/bash

# This script must be run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root. Use sudo."
   exit 1
fi

echo "--- Initial State ---"
echo "core_pattern: $(cat /proc/sys/kernel/core_pattern)"
echo "randomize_va_space: $(cat /proc/sys/kernel/randomize_va_space)"

# Apply fuzzing-friendly settings
echo "core" > /proc/sys/kernel/core_pattern
echo "0" > /proc/sys/kernel/randomize_va_space

echo
echo "--- Final State ---"
echo "core_pattern: $(cat /proc/sys/kernel/core_pattern)"
echo "randomize_va_space: $(cat /proc/sys/kernel/randomize_va_space)"
echo
echo "System configured."

#sudo sh -c "echo core > /proc/sys/kernel/core_pattern"
#sudo sh -c "echo 0 > /proc/sys/kernel/randomize_va_space"
