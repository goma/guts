###############################################################################
### Goma input file for nanomanufacturing simulations
### Author:  Scott A Roberts (sarober@sandia.gov)
###############################################################################
# {include("journal.aprepro")}

###############################
### FEM File Specifications ###
###############################
FEM file                           = journal.tri.g
Output EXODUS II file              = journal.tri.exoII
GUESS file                         = no
SOLN file                          = no
Write intermediate results         = yes
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
Time integration                   = steady
#Time integration                   = transient
delta_t                            = -1.0e-0
Initial Time                       = 0.0
Maximum number of time steps       = 100
Maximum time                       = 100.0
Minimum time step                  = 1e-10
Maximum time step                  = 1e10
Time step parameter                = 0.5
Time step error                    = 0.0
Printing Frequency                 = 1


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
Number of Newton Iterations        = 20
Newton correction factor           = 1.0
Normalized Residual Tolerance      = 1e-8

#########################################
### Boundary Condition Specifications ###
#########################################
Number of BC                       = -1

### Lubrication boundary conditions
#BC = LUB_PRESS NS 1 {0}
BC = LUB_PRESS NS 2 {0}

### Pin ends of mesh
#BC = DZ NS 11 0.0

### Keep middle from moving
BC = DX NS 12 0.0
BC = DY NS 12 0.0
BC = DZ NS 12 0.0

### FSI coupling
BC = SH_LUBP_SOLID SS 10 1.0

END OF BC

###########################
### Problem Description ###
###########################
Number of Materials                = 2

### Lubrication
MAT                                = journal 1
Coordinate System                  = CARTESIAN
Element Mapping                    = isoparametric
Mesh Motion                        = ARBITRARY
Number of bulk species             = 0
Number of bulk species equations   = 0

### Equations
Number of EQ = -1 #                      mas adv bnd dif src div por
EQ = lubp             Q1 LUBP          Q1         1   1   1
END OF EQ

### Solid
MAT                                = solid 2
Coordinate System                  = CARTESIAN
Element Mapping                    = isoparametric
Mesh Motion                        = LAGRANGIAN
Number of bulk species             = 0
Number of bulk species equations   = 0

### Equations
Number of EQ = -1 #                      mas adv bnd dif src div por
EQ = mesh1            Q1 D1            Q1 0   0   1   1       0
EQ = mesh2            Q1 D2            Q1 0   0   1   1       0
EQ = mesh3            Q1 D3            Q1 0   0   1   1       0
END OF EQ

######################################
### Post Processing Specifications ###
######################################
Post Processing Specifications
Shell Normal Vectors            = yes
Lubrication Height              = yes
Lubrication Upper Velocity      = yes
Lubrication Lower Velocity      = yes
Lubrication Velocity Field      = yes

