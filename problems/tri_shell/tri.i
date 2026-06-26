###############################################################################
### Goma input file for nanomanufacturing simulations
### Author:  Scott A Roberts (sarober@sandia.gov)
###############################################################################
# {include("tri.aprepro")}

###############################
### FEM File Specifications ###
###############################
FEM file                           = trimesh.exoII
Output EXODUS II file              = tri.exoII
GUESS file                         = no
SOLN file                          = no
Write intermediate results         = no
Write initial solution             = no

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
Fill Weight Function                = Galerkin
Level Set Interface Tracking        = none

#############################
### Solver Specifications ###
#############################
Solution Algorithm                 = umf
Amesos Solver Package              = superlu
Number of Newton Iterations        = 10
Newton correction factor           = 1.0
Normalized Residual Tolerance      = 1e-10

#########################################
### Boundary Condition Specifications ###
#########################################
Number of BC                       = -1

### Lubrication boundary conditions
BC = LUB_PRESS NS 3 0.0

END OF BC

###########################
### Problem Description ###
###########################
Number of Materials                = 1

### Lubrication
MAT                                = tri 1
Coordinate System                  = CARTESIAN
Element Mapping                    = isoparametric
Mesh Motion                        = ARBITRARY
Number of bulk species             = 0
Number of bulk species equations   = 0

### Equations
Number of EQ = -1 #                      mas adv bnd dif src div por
EQ = lubp             Q1 LUBP          Q1         1   1   1
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

