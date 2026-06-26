### 
### GOMA input deck for railgun simulations
###
{include(solid.a)}

###############################
### FEM File Specifications ###
###############################
FEM file                           = solid.g
Output EXODUS II file              = solid.exoII
GUESS file                         = no
SOLN file                          = no
Write intermediate results         = no
Write initial solution             = yes

##############################
### General Specifications ###
##############################
Output Level                       = 0
Debug                              = -0
Initial Guess                      = ones
Anneal Mesh on Output              = no

#######################################
### Time Integration Specifications ###
####################################### 
Time integration                   = steady
delta_t                            = 1e-4
Initial Time                       = 0
Maximum number of time steps       = 1
Maximum time                       = 1e-3
Minimum time step                  = 1e-6
Minimum resolved time step         = 1e-6
Maximum time step                  = 1e-4
Time step parameter                = 0.5
Time step error                    = -0.01  1 0 0 0 0 0 1 1
Printing Frequency                 = 1
Courant Number Limit               = 0.2

################################
### Level Set Specifications ###
################################ 
Fill Weight Function                = Galerkin
Level Set Interface Tracking        = none

#############################
### Solver Specifications ###
#############################
Solution Algorithm                 = umf
Amesos Solver Package              = superlu
Maximum Linear Solver Iterations   = 500
Preconditioner                     = dom_decomp
Matrix subdomain solver            = ilut
Matrix Scaling                     = row_sum
Matrix ILUT fill factor            = 3.0
Matrix drop tolerance              = 1.e-6
Matrix residual norm type          = r0
Size of Krylov subspace            = 350
Orthogonalization                  = modified
Maximum Linear Solve Iterations    = 350

##############################
### Newton Loop Parameters ###
##############################
Number of Newton Iterations        = 100
Newton correction factor           = 1.0
Normalized Residual Tolerance      = 1.e-8
Residual Ratio Tolerance           = 1e-10
Pressure Stabilization             = no


#########################################
### Boundary Condition Specifications ###
#########################################
Number of BC                       = -1

BC = DX NS 12 0.0
BC = DY NS 12 0.0
BC = DZ NS 12 0.0
BC = FORCE SS 11 {Force} 0.0 0.0

END OF BC


###########################
### Problem Description ###
###########################
Number of Materials                = 1

### Solid block
MAT                                = solid 1
Coordinate System                  = CARTESIAN
Element Mapping                    = isoparametric
Mesh Motion                        = LAGRANGIAN
Number of bulk species             = 0
Number of bulk species equations   = 0
Number of EQ = -1 #                      mas adv bnd dif src div por
EQ = mesh1            Q1 D1            Q1 0   0       1   1   1
EQ = mesh2            Q1 D2            Q1 0   0       1   1   1
EQ = mesh3            Q1 D3            Q1 0   0       1   1   1
END OF EQ

######################################
### Post Processing Specifications ###
######################################
Post Processing Specifications
Mesh Stress Tensor = yes

