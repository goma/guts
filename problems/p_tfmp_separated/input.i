# Goma input file for single phase lubp_liq comparison
# Author Andrew Cochrane (acochrane@gmail.com)
{include(variables.inc)}

# FEM File Specifications
FEM file                    = domain.exoII
Output EXODUS II file       = output.exoII
GUESS file                  = no
SOLN file                   = no
Write intermediate results  = no
Write initial solution      = yes

# General Specifications
Number of Processors        = 1
Output Level                = 0
Debug                       = 0
Initial Guess               = read_exoII
#Initial Guess               = random


# Time Integration Specifications
Time integration            = transient
delta_t                     = 1e-6
Maximum number of time steps = 5
Maximum time                = 0.0008
Minimum time step           = 1e-10
Maximum time step           = 1e-1
Time step parameter         = {tsp}
Time step error             = -3e-2 1 1 1 1 1 1 1 1 1 
Initial Time                = 0
  Printing Frequency          = 0 {0.0008/100}

# Solver Specifications
#Solution Algorithm          = bicgstab
Solution Algorithm          = amesos
Amesos Solver Package       = mumps
Preconditioner              = dom_decomp
Matrix subdomain solver     = ilut
Size of Krylov subspace     = 500
Maximum Linear Solve Iterations = 500
Number of Newton Iterations = 10
Newton correction factor      = 1
  Normalized Residual Tolerance = {nrt}

# Boundary Condition Specifications
Number of BC                  = 4
BC = SHELL_TFMP_PRES_BC NS 1       1013250
BC = SHELL_TFMP_PRES_BC NS 2       1013250
BC = SHELL_TFMP_PRES_BC NS 3       1013250
BC = SHELL_TFMP_PRES_BC NS 4       1013250
#BC = SHELL_TFMP_FREE_LIQ_BC SS 1

# Problem Description
Number of Materials           = 1
MAT                           = ptm 1
Coordinate System             = CARTESIAN
Element Mapping                    = isoparametric
Mesh Motion                        = ARBITRARY
Number of bulk species             = 0
Number of bulk species equations   = 0

Number of EQ = 2                  # mas adv bnd dif src por
#EQ = momentum1  Q1  U1         Q1   0   0   0   0   0   1
#EQ = momentum2  Q1  U2         Q1   0   0   0   0   0   1
#EQ = momentum3  Q1  U3         Q1   0   0   0   0   0   1
EQ = tfmp_mass  Q1  TFMP_SAT    Q1   1   1       1
EQ = tfmp_bound Q1  TFMP_PRES   Q1   1   1           0    


Post Processing Specifications
Lubrication Saturation = no
Pressure contours = no
TFMP_gas_velo = yes
TFMP_liq_velo = yes
TFMP_Peclet = yes
TFMP_Krg = yes
$TFMP_rho = yes
$TFMP_mu = yes
$TFMP_rho_mu = yes
Lubrication Height = yes
#Volumetric Integration Output Format = CSV
#Post Processing Volumetric Integration = 
#VOLUME_INT = POROUS_LIQ_INVENTORY 1 0 volume.csv
#END OF VOLUME_INT
