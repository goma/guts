Goma EFV Test Problem

A very simple problem to test reading of time dependent external fields.

CreateTimePlanes.input
This input desk runs a simple simulation on a 2D mesh.  It includes a 1D temperature profile that develops due to a temperature gradient across the mesh.  It also applies a time dependent, 2D velocity component onto the nodes.

Output is temp_flow_out.exoII

This does not have to be run every time to test time dependent fields, but was included for tweaking of the fields to read in.

ReadTimePlanes.input
The second input file runs a simple 1D species diffusion across the mesh while it reads in the temperature and velocity information.  Add "time_dep" to the external read line in the input deck to turn on the time varying reads.  If nothing (or any other text) is present on the line the behavior reverts to previous, it reads the last time plane of the external file.

Output is EFV_Test_out.exoII
This can be compared to EFV_Test_Master.exoII to determine effects of code changes.
