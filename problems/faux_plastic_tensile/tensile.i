### 
### GOMA input deck for railgun simulations
###
{include(armature.apre)}


###############################
### FEM File Specifications ###
###############################
FEM file                           = geometry.exoII
Output EXODUS II file              = tensile.exoII
GUESS file                         = no
SOLN file                          = no
Write intermediate results         = no
Write initial solution             = yes

##############################
### General Specifications ###
##############################
Output Level                       = 0
Debug                              = -0
Initial Guess                      = zeros
Anneal Mesh on Output              = no

#######################################
### Time Integration Specifications ###
####################################### 
Time integration                   = transient
delta_t                            = 1e-3
Initial Time                       = 0.0
Maximum number of time steps       = 10
Maximum time                       = 0.1
Minimum time step                  = 1e-9
Minimum resolved time step         = 1e-9
Maximum time step                  = 2e-2
Time step parameter                = 0.5
Time step error                    = 0.02 1
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
Solution Algorithm                 = gmres
Amesos Solver Package              = superlu
Maximum Linear Solver Iterations   = 500
Preconditioner                     = dom_decomp
Matrix subdomain solver            = ilu
Matrix Scaling                     = row_sum
Matrix ILUT fill factor            = 1.0
Matrix drop tolerance              = 1.e-6
Matrix residual norm type          = r0
Size of Krylov subspace            = 350
Orthogonalization                  = modified
Maximum Linear Solve Iterations    = 350

##############################
### Newton Loop Parameters ###
##############################
Number of Newton Iterations        = 20
Newton correction factor           = 1.0
Normalized Residual Tolerance      = 1.e-8
Residual Ratio Tolerance           = 1e-10
Residual Relative Tolerance      = 1e-6
Pressure Stabilization             = no


#########################################
### Boundary Condition Specifications ###
#########################################
Number of BC                       = -1

# Bottom BC
BC = DX NS 1 0.0
BC = DY NS 1 0.0
BC = DZ NS 1 0.0

# Top BC
BC = DX NS 2 0.0
BC = GD_LINEAR SS 2 R_MESH2 0 MESH_DISPLACEMENT2 0 1.0 0.0
BC = GD_TIME   SS 2 R_MESH2 0 LINEAR 0 0.0 1.0
BC = GD_LINEAR SS 2 R_MESH2 0 MESH_DISPLACEMENT2 0 0.0 -1.0
BC = DZ NS 2 0.0

END OF BC


###########################
### Problem Description ###
###########################
Number of Materials                = 1

### Solid block
MAT                                = solid 1
Coordinate System                  = CARTESIAN
Element Mapping                    = isoparametric
Mesh Motion                        = DYNAMIC_LAGRANGIAN
Number of bulk species             = 0
Number of bulk species equations   = 0
Number of EQ = -1 #                      mas adv bnd dif src div por
EQ = mesh1            Q1 D1            Q1 0   0       1   1   1
EQ = mesh2            Q1 D2            Q1 0   0       1   1   1
EQ = mesh3            Q1 D3            Q1 0   0       1   1   1
EQ = max_strain       Q1 MAX_STRAIN    Q1 1               1
END OF EQ

######################################
### Post Processing Specifications ###
######################################
Post Processing Specifications
Mesh Stress Tensor             = yes
Mesh Strain Tensor             = yes
First Invariant of Strain      = no
Second Invariant of Strain     = no
Third Invariant of Strain      = no
Lame MU                        = yes
Lame LAMBDA                    = yes
Von Mises Strain               = yes
Von Mises Stress               = yes

