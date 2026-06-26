###############################################################################
### Goma input file for nanomanufacturing simulations
### Author:  Scott A Roberts (sarober@sandia.gov)
###############################################################################
# {include("slidertop.aprepro")}

###############################
### FEM File Specifications ###
###############################
FEM file                           = geometry.exoII
Output EXODUS II file              = slidertop.exoII
GUESS file                         = no
SOLN file                          = no
Write intermediate results         = no
Write initial solution             = yes

##############################
### General Specifications ###
##############################
Output Level                       = 0
Debug                              = 0
Initial Guess                      = zeros
Anneal Mesh on Output              = no

#######################################
### Time Integration Specifications ###
####################################### 
Time integration                   = steady

################################
### Level Set Specifications ###
################################ 
Level Set Interface Tracking        = no

#############################
### Solver Specifications ###
#############################
Solution Algorithm                 = umf
Number of Newton Iterations        = 8
Newton correction factor           = 1.0
Normalized Residual Tolerance      = 1e-10

#########################################
### Boundary Condition Specifications ###
#########################################
Number of BC                       = -1

### Lubrication boundary conditions
BC = LUB_PRESS NS 1 0.0
#BC = LUB_PRESS NS 2 0.0
BC = LUB_PRESS NS 3 0.0
#BC = LUB_PRESS NS 4 0.0

### Pin the top of the mesh
BC = DX NS 60 0.0
BC = DY NS 60 0.0
BC = DZ NS 60 0.0

### FSI coupling
BC = SH_LUBP_SOLID SS 50 1.0


END OF BC

###########################
### Problem Description ###
###########################
Number of Materials                = 2

### Lubrication
MAT                                = slidertop 1
Coordinate System                  = CARTESIAN
Element Mapping                    = isoparametric
Mesh Motion                        = ARBITRARY
Number of bulk species             = 0
Number of bulk species equations   = 0

### Equations
Number of EQ = -1 #                      mas adv bnd dif src div por
EQ = lubp             Q1 LUBP          Q1         1   1   1
END OF EQ

### Lubrication
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
Lubrication Height              = yes
Lubrication Upper Velocity      = yes
Lubrication Lower Velocity      = yes
Lubrication Velocity Field      = yes

