FEM Problem Specifications
--- ------- --------------
FEM file                         = shell.exoII
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
Debug                            = 0
#Initialize                       = SHELL_FILMP 0 0.0
Initial Guess                    = zero
External Pixel Field = HEIGHT Q1  tread.txt {blockid=1}
#External Pixel Field = weight Q1  tread.txt {blockid=1}
#External Field = HEIGHT Q1  map_pix.exoII
---
Time Integration Specifications
---- ----------- --------------
Time integration                 = steady
delta_t                          = {1.e-6}
Initial Time                     = 0.0
Maximum number of time steps     = 80000
Maximum time                     = {175000}
Minimum time step                = {1.e-10} 
Maximum time step                = {100}
Minimum Resolved Time Step       = {1.e-8}
Time step parameter              = 0.0
Time step error  		 = 100.0e-0  1   1   1   1   0  0  0
Printing Frequency               = 50
Fill Weight Function	         = Explicit
Courant Number Limit             = 0.2


---
Solver Specifications
------ --------------
Solution Algorithm               = umf
#Solution Algorithm               = gmres
#Solution Algorithm               = amesos
#Amesos Solver Package            = superlu
Preconditioner                  = dom_decomp
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
Size of Krylov subspace          = 150
Orthogonalization                = modified
Maximum Linear Solve Iterations  = 150

Number of Newton Iterations      = 10
Newton correction factor         = 1.0
Normalized Residual Tolerance    = 1.e-6
Residual Ratio Tolerance         = 1e-10
#Normalized Correction Tolerance  = 1.e-5
Pressure Stabilization           = yes
Pressure Stabilization Scaling   = 0.1

Boundary Condition Specifications
-------- --------- --------------
Number of BC                     = -1
######################################

BC = LUB_PRESS NS 1 1.
BC = LUB_PRESS NS 3 0.

END OF BC
######################################

Problem Description
---
Number of Materials = 1


MAT = simple     1
 
  Coordinate System = CARTESIAN
  Element Mapping   = isoparametric
  Mesh Motion = ARBITRARY
  Number of bulk species = 0
 
	 Number of EQ			 = 1
	 EQ = lubp      Q1 LUBP  Q1           1    1     1   

                              	                   mass adv bnd  dif  src porous

END OF EQ




Post Processing Specifications
---- ---------- --------------
Stream Function                 = no
Lubrication Height = yes
Lubrication Upper Velocity = no
Lubrication Lower Velocity = no
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
User-Defined Post Processing = yes
