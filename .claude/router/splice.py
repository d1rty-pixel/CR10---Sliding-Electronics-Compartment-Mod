import sys, re
f = "G:/Things/CR10---Sliding-Electronics-Compartment-Mod/gen/wiring.py"
s = open(f).read(); code = open(sys.argv[1]).read().strip()
a = s.index("ROUTES = {"); b = s.index("\n", s.index("KINK = {", a))
s = s[:a] + code + s[b:]
open(f, "w").write(s)
