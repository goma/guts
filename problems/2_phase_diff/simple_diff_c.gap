# Note: hash marks are comment characters. Everything following a hash mark
# will be ignored. Lines beginning with a hash mark will be deleted.
#
$ GOMA input file
$ CREATION_DATE USER_NAME_AND_SITE
$ {ECHO(OFF)} 
$     {include(Defs)}
$ {ECHO(ON)}

FEM Problem Specifications
--- ------- --------------
FEM file                         = geom2d2mat.exoII
Output EXODUS II file            = simple_diff_out.exoII
GUESS file                       = guess.d
SOLN file                        = simple_diff_out.d 
Write intermediate results	 = no

General Specifications
------- --------------

Number of processors = 1
Output level = 1
Initial Guess = read_exoII_file guess.exoII

Time Integration Specifications
---- ----------- --------------
Time integration                 = steady
delta_t                          = 1.0E-6
Maximum number of time steps     = 400
Maximum time                     = 1000.0
Minimum time step                = 1.0E-10
Maximum time step                = 10.0
Time step parameter              = 0.0
Time step error                  = 0.001 1 1 1 1 0 1
Printing Frequency               = 1
Initial Time                     = 0.0


Solver Specifications
------ --------------
Solution Algorithm               = lu
Number of Newton Iterations      = 17
Newton correction factor         = 1
Normalized Residual Tolerance    = 1e-10
Residual Ratio Tolerance         = 1e-2

Boundary Condition Specifications
-------- --------- --------------
Number of BC			 = -1
#
# ----------------------------------------------------------
#
#    Bottom of the domain -> made up of mat_a
#
BC = YFLUX    SS {bottom_ss} 0 1.0 0.05
#
# ----------------------------------------------------------
#
#    Top of the domain -> made up of mat_b
#
BC = YFLUX    SS {top_ss} 0 1.0 0.02
#
# ----------------------------------------------------------
#
#    Internal Interface
#
#
# BC = VL_EQUIL SS {interface_ss} 0 1 2 1.0E6 28. 18. 1800. 18.
#
  BC = IS_EQUIL_PSEUDORXN SS {interface_ss} 0 1 2 1.0
#
#
# ----------------------------------------------------------
#
#
END_OF_BOUNDARY_CONDITIONS

----
Problem Description
---
Number of Materials = 2

MAT = mat_a    1

  	Coordinate System = CARTESIAN
  	Element Mapping   = isoparametric
  	Mesh Motion = ARBITRARY
#            Number of bulk species is one less than the
#            total number in the problem
  	Number of bulk species = 2
  	Number of bulk species equations = 1

	Number of EQ			 = 1
        EQ = species_bulk Q1_D Y Q1_D   0.   1.   1.   1    0.

	
MAT = mat_b 2
	
  	Coordinate System = CARTESIAN
  	Element Mapping   = isoparametric
  	Mesh Motion = ARBITRARY
  	Number of bulk species = 2
  	Number of bulk species equations = 1

	Number of EQ			 = 1
        EQ = species_bulk Q1_D Y Q1_D   0.   1.   1.   1    0.
		
	
Post Processing Specifications
---- ---------- --------------
Streamwise normal stress	= no
Second Invarient of Strain	= no
Mesh Dilatation			= no
Navier Stokes Residuals		= yes
Moving Mesh Residuals		= no
Mass Diffusion Vectors		= no
Mass Fluxlines			= no
Energy Conduction Vectors	= no
Energy Fluxlines		= no
Time Derivatives		= no
Mesh Stress Tensor		= no
