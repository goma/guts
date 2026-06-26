#!/bin/sh

# Create mesh
cubit -nographics -nojournal -batch porousmesh.jou

# Run goma (serial)
./goma -a -i porous.i

# Run goma (parallel)
./brk -n 4 geometry.brk porousmesh.exoII
mpirun -np 4 ./goma -a -i porous.i

# Cleanup
rm *~
rm *?of?.*
rm cubit* history*
rm *.blot.log 
rm echo_* tmp.* User_Params coords
