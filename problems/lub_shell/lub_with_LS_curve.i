FEM Problem Specifications
--- ------- --------------
FEM file                         = shell_3D.gen
$FEM file                         = contin.exoII
Output EXODUS II file            = out.exoII
GUESS file                       = contin.dat
SOLN file                        = no
Write intermediate results       = no
$$Write initial solution  = yes

 ---
General Specifications
 ---
Number of processors             = 1
Output Level                     = 0
Debug                            = -0
Initial Guess                    = zero

---
Time Integration Specifications
---- ----------- --------------
Time integration                 = transient
delta_t                          = {1.e-6}
Initial Time                     = 0
Maximum number of time steps     = 3
Maximum time                     = {200}
Minimum time step                = {1.e-10} 
Maximum time step                = {1e-0}
Minimum Resolved Time Step       = {1.e-8}
Time step parameter              = 0.0
Time step error  		 = 5.e-1  1   1   1   1   0   0 0
Printing Frequency               = 5
#Fill Weight Function	         = Explicit
Fill Weight Function	         = Galerkin


#Courant Number Limit             = 2

Level Set Interface Tracking     = ON
Level Set Subelement Integration = OFF
Level Set Subgrid Integration Depth = 2
Level Set Length Scale           = {LSLS=0.04}
Level Set Initialization Method  = Surfaces 1
	                        SURF = SPHERE 0. 0.5 0. 0.7

$Level Set Initialization Method  = Exodus

Force Initial Level Set Renormalization = yes
Level Set Renormalization Method = Huygens
Level Set Renormalization Tolerance = 0.4
Level Set Renormalization Frequency = 10
Level Set Reconstruction Method  = POINTS

---
Solver Specifications
------ --------------
Solution Algorithm               = umf
#Solution Algorithm               = bicgstab
Preconditioner                  = Jacobi
Matrix subdomain solver          = ilut
Matrix reorder                   = rcm
Matrix Scaling                   = row_sum
Matrix ILUT fill factor          = 2.0
#Matrix Relative Threshold        = 1.0
#Matrix Absolute Threshold        = 1.e-5
Matrix drop tolerance            = 1.e-6
#Matrix Scaling                   = sym_diag
Matrix residual norm type        = r0
$Matrix output type               = 10
#Matrix factorization overlap     = diag
#Matrix factorization reuse       = calc
Size of Krylov subspace          = 250
Orthogonalization                = modified
Maximum Linear Solve Iterations  = 250

Number of Newton Iterations      = 9
Newton correction factor         = 1.0
Normalized Residual Tolerance    = 1.e-5
#Residual Ratio Tolerance         = 1e-10
Normalized Correction Tolerance  = 1.e-3
Residual Relative Tolerance      = 1.0e-06
Pressure Stabilization           = yes
Pressure Stabilization Scaling   = 0.1

Boundary Condition Specifications
-------- --------- --------------
Number of BC                     = -1
######################################

#BC = LUB_PRESS NS 1 0.
#BC = LUB_PRESS NS 2 0.
BC = LUB_PRESS NS 3 1e8
BC = LUB_PRESS NS 4 0.

END OF BC
######################################

Problem Description
---
Number of Materials = 1


MAT = liquid_gas_LS_curve     1
 
  Coordinate System = CARTESIAN
  Element Mapping   = isoparametric
  Mesh Motion = ARBITRARY
  Number of bulk species = 0
 
	Number of EQ			 = 3
	 EQ = lubp      Q1 LUBP  Q1           1    1     1   
#	 EQ = momentum1 Q1 U1    Q1  0    0   0    0    0     1
#	 EQ = momentum2 Q1 U2    Q1  0    0   0    0    0     1
#	 EQ = momentum3 Q1 U3    Q1  0    0   0    0    0     1
	 EQ = level_set Q1 F     Q1  1   1     1
	 EQ = shell_lub_curv Q1 SH_L_CURV Q1 1 1 1 0 1
                              	    mass adv bnd  dif  src porous

END OF EQ



Post Processing Specifications
---- ---------- --------------
Stream Function                 = yes
Lubrication Height              = yes
Lubrication Upper Velocity      = yes
Lubrication Lower Velocity      = yes
Lubrication Velocity Field      = yes
Streamwise normal stress        = no
Pressure contours               = no
Second Invarient of Strain      = no
Mesh Dilatation                 = no
Navier Stokes Residuals         = no
Moving Mesh Residuals           = no
Mass Diffusion Vectors          = no
Mass Fluxlines                  = no
Energy Conduction Vectors       = no
Energy Fluxlines                = no
Time Derivatives                = no
Viscosity = yes
Mesh Stress Tensor              = no
Porous Saturation = yes
