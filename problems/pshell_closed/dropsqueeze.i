###############################################################################
### Goma input file for nanomanufacturing simulations
### Author:  Scott A Roberts (sarober@sandia.gov)
###############################################################################
# {include("dropsqueeze.aprepro")}

###############################
### FEM File Specifications ###
###############################
FEM file                           = geometry.exoII
Output EXODUS II file              = dropsqueeze.exoII
GUESS file                         = no
SOLN file                          = no
Write intermediate results         = no
Write initial solution             = yes

##############################
### General Specifications ###
##############################
Output Level                       = 0
Debug                              = 0
Initial Guess                      = read_exoII
Initialize                         = SHELL_SAT_CLOSED 0 0.0
Initialize                         = SHELL_SAT_GASN 0 1.0
Initialize                         = LUBP 0 {p0}
#Initial Guess                      = read_exoII_file guess.exoII
Anneal Mesh on Output              = no

#######################################
### Time Integration Specifications ###
####################################### 
Time integration                   = transient
delta_t                            = -1e-8
Initial Time                       = -1.0
Maximum number of time steps       = 10
Maximum time                       = 2e-5
Minimum time step                  = 1e-12
Maximum time step                  = 1e-5
Time step parameter                = 0.5
Time step error                    = 1
Printing Frequency                 = 1

################################
### Level Set Specifications ###
################################ 
Fill Weight Function                = Galerkin
Level Set Interface Tracking        = yes
Level Set Length Scale              = {LSLS}
#Level Set Initialization Method     = Exodus
Level Set Initialization Method     = Surfaces 1
                                      SURF = CIRCLE 0.0 0.0 {dropR}
Level Set Renormalization Method    = Huygens_Constrained
Level Set Renormalization Tolerance = 0.25
Level Set Renormalization Frequency = 25
Level Set Reconstruction Method     = FACETS

#############################
### Solver Specifications ###
#############################
Solution Algorithm                 = amesos
Amesos Solver Package              = superlu
Number of Newton Iterations        = 100
Newton correction factor           = 1
Normalized Residual Tolerance      = 1e-8

#########################################
### Boundary Condition Specifications ###
#########################################
Number of BC                       = -1

### FSI coupling
#BC = SH_LUBP_SOLID SS 50 1.0

### Lubrication boundary conditions
BC = LUB_PRESS NS 1 {p0}
BC = LUB_PRESS NS 2 {p0}
BC = LUB_PRESS NS 3 {p0}
BC = LUB_PRESS NS 4 {p0}

### Pin the top so there is no horizontal movement
#BC = DX NS 60 0.0
#BC = DY NS 60 0.0

# Pin the sides
#BC = DX NS 10 0.0
#BC = DY NS 20 0.0
#BC = DX NS 30 0.0
#BC = DY NS 40 0.0

### Manipulation of continuum elements
#BC = FORCE SS 60 0.0 0.0 {Force_top}
#BC = DZ NS 60 0.0

END OF BC

###########################
### Problem Description ###
###########################
Number of Materials                = 1

### Lubrication
MAT                                = dropsqueeze 1
Coordinate System                  = CARTESIAN
Element Mapping                    = isoparametric
Mesh Motion                        = ARBITRARY
Number of bulk species             = 0
Number of bulk species equations   = 0

### Equations
Number of EQ = -1 #                      mas adv bnd dif src div por
EQ = lubp             Q1 LUBP          Q1         1   1   1
EQ = level_set        Q1 F             Q1 1   1   1   
EQ = shell_lub_curv   Q1 SH_L_CURV     Q1 1   1   1   1       1 
EQ = shell_sat_closed Q1 SH_SAT_CLOSED Q1 1                   1
EQ = shell_sat_gasn   Q1 SH_SAT_GASN   Q1 1               1
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
Lubrication Velocity Field      = yes
Viscosity                       = yes
Density                         = yes
