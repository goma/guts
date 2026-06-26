
5/26/09
This problem has some uninitialized memory errors or memory overwrites 
of unknown form. I eliminated a few UMR's, but the problem still remains
unstable. It's unstable in the sense that different link lines seem to
product slightly different exodiff results and residual convergence
histories.

Differences in the solution files are on the order of the differences between
out_blessed_3.exoII and out_blessed_4.exoII

Differences in the residual histories are on the order of differences between
base2.serr and serr_bad.ball.  Note, all cases actually basically solve the
problem.

Currently, the -g and the -O solution are different.

Noticed that there are floating point comparisons against 0.0 in the level set
algorithms.
