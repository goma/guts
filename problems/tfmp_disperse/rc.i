# Goma input file for single phase lubp_liq comparison
# Author Andrew Cochrane (acochrane@gmail.com)
{include(variables.inc)}

# FEM File Specifications
FEM file                    = cdom_map.exoII
Output EXODUS II file       = coutput.exoII
GUESS file                  = no
SOLN file                   = no
Write intermediate results  = no
Write initial solution      = yes

# General Specifications
Number of Processors        = 1
Output Level                = 0
Debug                       = 0
#Initial Guess               = zeros
Initial Guess               = read_exoII
#Initial Guess               = random


# Time Integration Specifications
Time integration            = transient
delta_t                     = 1e-3
Maximum number of time steps = 15
  Maximum time                = 1
Minimum time step           = 1e-6
#Minimum Resolved Time Step  = 0.05
Maximum time step           = 1e-2
Time step parameter         = {tsp}
Time step error             = -5.0e-1 1 1 1 1 1 1 1 1 1
  Time step decelerator       = {0.5}
Initial Time                = 0
Printing Frequency          = 1

# Solver Specifications
#Total Number of Matrices         = 2
#Matrix storage format       = epetra
#Matrix storage format       = MSR
#Stratimikos File            = stratimikos.xml
#Solution Algorithm          = stratimikos
#Solution Algorithm          = aztecoo
Solution Algorithm          = amesos
#Solution Algorithm          = 
Amesos Solver Package       = mumps
AztecOO Solver              = gmres
#Preconditioner              = dom_decomp
Preconditioner              = sym_GS
Matrix subdomain solver     = rilu
Size of Krylov subspace     = 500
Maximum Linear Solve Iterations = 5000
Number of Newton Iterations = 10
#Newton correction factor      = .7 1e-7 0.25 2e-6 1 1e-4
Newton correction factor      = 1
Normalized Residual Tolerance = 1e-9
Matrix factorization overlap  = 2
Matrix polynomial order       = 4
Matrix drop tolerance         = 1.0e-10
Matrix graph fillin           = 1

# Boundary Condition Specifications
Number of BC                  = -1
#BC = SHELL_TFMP_SAT_BC      NS 3    1
BC = SHELL_TFMP_PRES_BC     NS 1     1013250
#BC = SHELL_TFMP_PRES_BC     NS 2    1
#BC = SHELL_TFMP_PRES_BC     NS 3    0
#BC = SHELL_TFMP_PRES_BC     NS 4    0

BC = SHELL_TFMP_FREE_LIQ_BC SS 1
#BC = SHELL_TFMP_FREE_GAS_BC SS 1
#BC = SHELL_TFMP_FREE_LIQ_BC SS 2
#BC = SHELL_TFMP_FREE_GAS_BC SS 2
#BC = SHELL_TFMP_FREE_LIQ_BC SS 3
#BC = SHELL_TFMP_FREE_GAS_BC SS 3
#BC = SHELL_TFMP_FREE_LIQ_BC SS 4
#BC = SHELL_TFMP_FREE_GAS_BC SS 4

END OF BC

# Problem Description
Number of Materials           = 1
MAT                           = ptm 1
Coordinate System             = CARTESIAN
Element Mapping                    = isoparametric
Mesh Motion                        = ARBITRARY
Number of bulk species             = 0
Number of bulk species equations   = 0

#Number of Matrices = 2


#MATRIX = 1
#Disable time step control = yes
  Number of EQ = 2
#EQ = momentum1  Q2  U1         Q2   0   0   0   0   0   1
#EQ = momentum2  Q2  U2         Q2   0   0   0   0   0   1
#EQ = momentum3  Q2  U3         Q2   0   0   0   0   0   1

#MATRIX = 2
#Number of EQ = 2                 # mas adv bnd dif src por
EQ = tfmp_mass  Q1  TFMP_PRES  Q1   1   1       1
EQ = tfmp_bound Q1  TFMP_SAT   Q1   1   1            0

Post Processing Specifications
#Pressure contours = yes
#Lubrication Saturation = yes
TFMP_gas_velo = yes
TFMP_liq_velo = yes
TFMP_inverse_Peclet = yes
TFMP_Krg = yes
#TFMP_satu = yes
#TFMP_rho = yes
#TFMP_mu = yes
#TFMP_rho_mu = yes
#TFMP_GradP_X = yes
#TFMP_GradP_Y = yes
#TFMP_GradP_Z = yes
#Volumetric Integration Output Format = CSV
#Post Processing Volumetric Integration = 
#VOLUME_INT = POROUS_LIQ_INVENTORY 1 0 volume.csv
#END OF VOLUME_INT
