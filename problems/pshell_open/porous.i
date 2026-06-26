###############################################################################
### Goma input file for nanomanufacturing simulations
### Author:  Scott A Roberts (sarober@sandia.gov)
###############################################################################

###############################
### FEM File Specifications ###
###############################
FEM file                           = porousmesh.exoII
Output EXODUS II file              = porous.exoII
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
Initialize                         = SHELL_PRESS_OPEN 0 -4000
Anneal Mesh on Output              = no

#######################################
### Time Integration Specifications ###
####################################### 
Time integration                   = transient
delta_t                            = 1e-6
Initial Time                       = -1.0
Maximum number of time steps       = 5
Maximum time                       = 0.1
Minimum time step                  = 1e-10
Maximum time step                  = 1e-3
Time step parameter                = 0.5
Time step error                    = 0.02 0 0 0 0 0 0 0 0 1 
Printing Frequency                 = 1

################################
### Level Set Specifications ###
################################ 
Fill Weight Function                = Galerkin
Level Set Interface Tracking        = yes
Level Set Length Scale              = 0.2
Level Set Initialization Method     = Surfaces 1
                                      SURF = SPHERE 1.0 4.9 0.0 0.3
Level Set Renormalization Method    = Huygens_Constrained
Level Set Renormalization Tolerance = 0.8
Level Set Renormalization Frequency = 30
Level Set Reconstruction Method     = POINTS
Force Initial Level Set Renormalization = no

#############################
### Solver Specifications ###
#############################
#Solution Algorithm                 = gmres
Solution Algorithm                 = amesos
Amesos Solver Package              = superlu
Preconditioner                     = dom_decomp
Matrix subdomain solver            = ilut
Size of Krylov subspace            = 500
Maximum Linear Solve Iterations    = 500
Number of Newton Iterations        = 10
Newton correction factor           = 1.0
Normalized Residual Tolerance      = 1e-8
Residual Relative Tolerance      = 1.0e-06
Pressure Stabilization             = no

#########################################
### Boundary Condition Specifications ###
#########################################
Number of BC                       = -1

### Lubrication boundary conditions
BC = LUB_PRESS NS 1 0.0
BC = LUB_PRESS NS 2 0.0
BC = LUB_PRESS NS 3 0.0

END OF BC

###########################
### Problem Description ###
###########################
Number of Materials                = 1

### Lubrication
MAT                                = porous 1
Coordinate System                  = CARTESIAN
Element Mapping                    = isoparametric
Mesh Motion                        = ARBITRARY
Number of bulk species             = 0
Number of bulk species equations   = 0

### Equations
Number of EQ = -1 #                      mas adv bnd dif src div por 
EQ = lubp             Q1 LUBP          Q1         1   1   1
EQ = level_set        Q1 F             Q1 1   1   1   
EQ = shell_lub_curv   Q1 sh_l_curv     Q1 1   1   1   0   1 
EQ = shell_sat_open   Q1 SH_P_OPEN     Q1 1           1   1
END OF EQ

######################################
### Post Processing Specifications ###
######################################
Post Processing Specifications
Lubrication Height              = yes
Viscosity                       = yes
Density                         = yes
Lubrication Velocity Field      = yes
Porous Shell Open Saturation    = yes
