# The IngeTrazo document lies Z0_MM higher than the generator frame (Z = 0 = bottom of the frame profiles), so the CR10
# feet stand on Z = 0, which is Newton's ground. Generator data, build/*.json and the measurements in docs/ stay in the
# generator frame; every script that moves coordinates between generator and document adds or subtracts Z0_MM.
Z0_MM = 25.0
