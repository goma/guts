FEM Problem Specifications
--- ------- --------------
FEM file                         = 40x40_Centi.exoII
Output EXODUS II file            = out.exoII
GUESS file                       = contin.dat
SOLN file                        = no
Write intermediate results       = no
Write initial solution           = yes

 ---
General Specifications
 ---
Number of processors             = 1
Output Level                     = 0
Debug                            = 0
Initialize                       = SHELL_FILMP 0 0.0
Initialize                       = SHELL_FILMH 0 2.6e-2
Initialize                       = SHELL_PARTC 0 0.1
External Field                   = THETA Q1 lines_40x40_Centi.exoII
---
Time Integration Specifications
---- ----------- --------------
Time integration                 = transient
delta_t                          = {1.e-10}
Initial Time                     = 0.
Maximum number of time steps     = 3
Maximum time                     = {10}
Minimum time step                = {1.e-14} 
Maximum time step                = {1}
Minimum Resolved Time Step       = {1.e-12}
Time step parameter              = 0.0
Time step error  		 = 1.0  1   1   1   1   0  0  0
Printing Frequency               = 50
Fill Weight Function	         = Explicit
Courant Number Limit             = 0.2


---
Solver Specifications
------ --------------
#Solution Algorithm               = amesos
#Amesos Solver Package            = superlu
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

Number of Newton Iterations      = 10
Newton correction factor         = 1.0
Normalized Residual Tolerance    = 1.e-10
Residual Ratio Tolerance         = 1e-10
#Normalized Correction Tolerance  = 1.e-5
Pressure Stabilization           = yes
Pressure Stabilization Scaling   = 0.1

Boundary Condition Specifications
-------- --------- --------------
Number of BC                     = -1
######################################

BC = SHELL_GRAD_FP_BC SS 100 0.0
BC = SHELL_GRAD_FH_BC SS 100 0.0  
BC = SHELL_GRAD_FP_BC SS 200 0.0
BC = SHELL_GRAD_FH_BC SS 200 0.0  
BC = SHELL_GRAD_FP_BC SS 300 0.0
BC = SHELL_GRAD_FH_BC SS 300 0.0
BC = SHELL_GRAD_FP_BC SS 400 0.0
BC = SHELL_GRAD_FH_BC SS 400 0.0 

END OF BC
######################################

Problem Description
---
Number of Materials = 1


MAT = mounding_film_coarse_grained     1
 
  Coordinate System = CARTESIAN
  Element Mapping   = isoparametric
  Mesh Motion = ARBITRARY
  Number of bulk species = 0
 
	 Number of EQ			 = 3
	 EQ = shell_filmp      Q1 SHELL_FILMP  Q1   1    1   1    1    1   
	 EQ = shell_filmh      Q1 SHELL_FILMH  Q1   1    1   1    1    1  
	 EQ = shell_partc      Q1 SHELL_PARTC  Q1   1    1   1    1    1  
                              	                   mass adv bnd  dif  src porous

END OF EQ




Post Processing Specifications
---- ---------- --------------
Stream Function                 = no
Lubrication Height = no
Lubrication Upper Velocity = no
Lubrication Lower Velocity = no
Disjoining Pressure        = yes
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
Porous Saturation = no
User-Defined Post Processing = no
