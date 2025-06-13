#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 00:49:42 2025

@author: laurendonnelly
"""

import hashlib
import random

# Simulated model weights
weights = 0.5

# Save checkpoints here
checkpoints = {}

#random state
random.seed(a=3294)
rand_state = random.getstate()

# Simulate task
for step in range(1, 101):
    weights += 0.01 * (random.random() - 0.5)  # Simulated gradient update

    if step % 20 == 0:
        # Create checkpoint: hash of weight value
        hash_object = hashlib.sha256(str(weights).encode())
        checkpoint_hash = hash_object.hexdigest()
        checkpoints[step] = checkpoint_hash
        print(f"Worker checkpoint at step {step}: {checkpoint_hash}")

# Verifier checks a random checkpoint
random.seed() #to test different checkpoints, will switch state to system time
check_step = random.choice(list(checkpoints.keys()))

#reset random state
random.setstate(rand_state)
# Recompute weight value up to check_step
verifier_weights = 0.5
for step in range(1, check_step + 1):
    verifier_weights += 0.01 * (random.random() - 0.5)  # Should ideally use same RNG seed to match

# Hash verifier's result
verifier_hash = hashlib.sha256(str(verifier_weights).encode()).hexdigest()

# Compare
print(f"\nVerifier checkpoint at step {check_step}: {verifier_hash}")
if verifier_hash == checkpoints[check_step]:
    print("Good: Verification passed.")
else:
    print("Bad: Verification failed.")
