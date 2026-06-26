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
Debug = 0
Number of Jacobian File Dumps = 1

Time Integration Specifications
---- ----------- --------------
Time integration                 = transient 
delta_t                          = 0.75
Maximum number of time steps     = 15
Maximum time                     = 350.0
Minimum time step                = 1.0E-10
Maximum time step                = 20.0
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
BC = DX NS {bottom_ns} 0.0
BC = DY NS {bottom_ns} 0.0
#
# ----------------------------------------------------------
#
#    Top of the domain -> made up of mat_b
#
BC = YFLUX    SS {top_ss} 0 1.0 0.02
#
BC = DX NS {top_ns} 0.0
BC = DY NS {top_ns} 0.0
#
# ----------------------------------------------------------
#
#    Right side of the domain
#
BC = PLANE SS {right1_ss}   1.0 0.0 0.0 { - x_2 }
BC = PLANE SS {right2_ss}   1.0 0.0 0.0 { - x_2 }
#
# ----------------------------------------------------------
#
#    Left side of the domain
#
BC = PLANE SS {left1_ss}   1.0 0.0 0.0  0.0
BC = PLANE SS {left2_ss}   1.0 0.0 0.0  0.0
# ----------------------------------------------------------
#
#    Internal Interface
#
#
#
  BC = IS_EQUIL_PSEUDORXN SS {interface_ss} 0 1 2 1.0
#
#
# SURFDOMAINCHEMKIN_KIN_STEFAN_FLOW:
#    This moves the interface according to the stefan flow equations
#    
#
  BC = SURFDOMAINCHEMKIN_KIN_STEFAN_FLOW SS {interface_ss} 1 IS_EQUIL_PSEUDORXN
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

	Number of EQ			 = 3
        EQ = species_bulk Q1_D Y Q1_D   1.   1.   1.   1    0.
        EQ = mesh1        Q1  D1 Q1     0.   0.   1.   1    0.
        EQ = mesh2        Q1  D2 Q1     0.   0.   1.   1    0.

	
MAT = mat_b 2
	
  	Coordinate System = CARTESIAN
  	Element Mapping   = isoparametric
  	Mesh Motion = ARBITRARY
  	Number of bulk species = 2
  	Number of bulk species equations = 1

	Number of EQ			 = 3
        EQ = species_bulk Q1_D Y Q1_D   1.   1.   1.   1    0.
        EQ = mesh1        Q1  D1 Q1     0.   0.   1.   1    0.
        EQ = mesh2        Q1  D2 Q1     0.   0.   1.   1    0.
		
	
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
