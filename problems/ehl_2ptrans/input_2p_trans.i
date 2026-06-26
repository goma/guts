# Goma input file for single phase lubp_liq comparison
# Author Andrew Cochrane (acochrane@gmail.com)
{include(variables.inc)}

#{idler_disp_start = 3.0}
#{idler_disp_step = 1e-6}
#{idler_disp_step_min = 1e-08}
#{idler_disp_step_max = 0.001}
#{idler_disp_end = 5.0001}

# FEM File Specifications
FEM file = trim_visc_dn_speed10.exoII
Output EXODUS II file = 2p_spd10.exoII
GUESS file                  = no
SOLN file                   = no
Write intermediate results  = no
Write initial solution      = yes

  
# General Specifications
Number of Processors        = 1
Output Level                = 0
Debug                       = 0
Initial Guess               = read_exoII
#Initial Guess               = one
#Initial Guess               = read_exoII_file guess_ss.exoII
#Initial Guess               = random
#Anneal Mesh on Output       = yes

#External Field               = HEIGHT Q1 gas_spd10_annealed.exoII
  
# Time Integration Specifications
Time integration            = transient
delta_t                     = 1e-5
Maximum number of time steps = 100
Maximum time                = 100
Minimum time step           = 1e-12
Maximum time step           = 0.25
Time step parameter         = {tsp}
Time step error             = -1e-2 1 1 1 1 1 1 1 1 1
Initial Time                = 0
Printing Frequency          = 10
  
# continuation specs
#Continuation = zero
Continuation Type = MT
Boundary condition ID = 0
Boundary condition data float tag = 0
Material id = 2
Material property tag = 7109
Material property tag subindex = 0
Initial parameter value = {0.01}
Final parameter value = {18.6e-5}
delta_s   =  0.001
Maximum number of path steps    = 2000
Minimum path step    = 1e-5
Maximum path step   = 200.0
Continuation Printing Frequency = 1


  

# Solver Specifications
Solution Algorithm          = umf
#Solution Algorithm          = amesos
#Amesos Solver Package       = superlu
Amesos Solver Package       = mumps
Preconditioner              = dom_decomp
Matrix subdomain solver     = ilut
Size of Krylov subspace     = 500
Maximum Linear Solve Iterations = 500
Number of Newton Iterations = 10
Newton correction factor      = 1
#Newton correction factor = 0.2 1.0e-10 0.15 1.0e-6 0.05 1.0e-2
Normalized Residual Tolerance = {1e-11}
#Matrix Absolute Threshold     = 1e-12
#  Printing Frequency          = 0 {(1e1)/100}
Printing Frequency          = 1

# Boundary Condition Specifications
Number of BC                  = -1
BC = SHELL_TFMP_PRES_BC NS 10       {boundary_pressure}
BC = SHELL_TFMP_PRES_BC NS 20       {boundary_pressure}

#BC = SHELL_LUBRICATION_OUTFLOW_BC NS 2
#BC = SHELL_TFMP_PRES_BC NS 3       1013250
#BC = SHELL_TFMP_PRES_BC NS 4       1013250
BC = SHELL_TFMP_FREE_LIQ_BC       NS 20
#BC = SHELL_TFMP_FREE_GAS_BC       NS 1
#BC = SHELL_TFMP_GRAD_S_BC       NS 200
#BC = SHELL_TFMP_SAT_BC       NS 2 0.50
BC = SHELL_TFMP_SAT_BC        NS 10 0.0005

BC = DX NS 1 0.
BC = DY NS 1 {idler_disp_start}
#BC = DX NS 1 0.0
#BC = DY NS 1 0.0

#BC = SH_SDET_BC NS 1 1.0
#BC = SH_SDET_BC NS 2 -1.0

#BC = SH_MESH2_WEAK_BC NS 2 {0.0}
  
BC = DY NS 2 {idler_disp_start}
BC = DX NS 2 0.0

#BC = DX NS 10 0.0
#BC = DX NS 20 0.0
  
#BC = SH_K NS 1 {0.0}
#BC = SH_K NS 2 .1

BC = SH_TENS NS 1 {stretch}

#BC = SH_NX_BC  NS 2 0.0 1
#BC = SH_NY_BC  NS 2 1.0 1

#BC = VELO_NORMAL SS 3 0.0
#BC = VELO_TANGENT SS 3 0 0.0 0.0 0.0

END OF BC




# Problem Description
Number of Materials           = 3
MAT                           = ptm_rolling 1
Coordinate System             = CARTESIAN
Element Mapping                    = isoparametric
Mesh Motion                        = ARBITRARY
Number of bulk species             = 0
Number of bulk species equations   = 0

Number of EQ = -1                 # mas adv bnd dif src por
#EQ = tfmp_mass  Q1  TFMP_SAT   Q1    0   1       1
#EQ = tfmp_bound Q1  TFMP_PRES  Q1    0   1           1

EQ = shell_curvature  Q1  K    Q1               1
EQ = shell_tension  Q1 TENS  Q1                 1

EQ = mesh1      Q1  D1      Q1       0   0   1   1   0   0
EQ = mesh2      Q1  D2      Q1       0   0   1   1   0   0

#EQ = shell_normal1 Q1  SH_N1 Q1                 1
#EQ = shell_normal2 Q1  SH_N2 Q1                 1
  
#EQ = momentum1  Q1  U1         Q1   0   0   0   0   0   1
#EQ = momentum2  Q1  U2         Q1   0   0   0   0   0   1
#EQ = momentum3  Q1  U3         Q1   0   0   0   0   0   1

END OF EQ


MAT = ptm_rolling_10 2
Coordinate System             = CARTESIAN
Element Mapping                    = isoparametric
Mesh Motion                        = ARBITRARY
Number of bulk species             = 0
Number of bulk species equations   = 0

Number of EQ = -1                 # mas adv bnd dif src por
EQ = tfmp_mass  Q1  TFMP_SAT   Q1    1   1       1
EQ = tfmp_bound Q1  TFMP_PRES  Q1    1   1           0

EQ = shell_curvature  Q1  K    Q1               1
EQ = shell_tension  Q1 TENS  Q1                 1

EQ = mesh1      Q1  D1      Q1       0   0   1   1   0   0
EQ = mesh2      Q1  D2      Q1       0   0   1   1   0   0

#EQ = shell_normal1 Q1  SH_N1 Q1                 1
#EQ = shell_normal2 Q1  SH_N2 Q1                 1
  
#EQ = momentum1  Q1  U1         Q1   0   0   0   0   0   1
#EQ = momentum2  Q1  U2         Q1   0   0   0   0   0   1
#EQ = momentum3  Q1  U3         Q1   0   0   0   0   0   1

END OF EQ


  MAT                           = ptm_rolling 3
Coordinate System             = CARTESIAN
Element Mapping                    = isoparametric
Mesh Motion                        = ARBITRARY
Number of bulk species             = 0
Number of bulk species equations   = 0

Number of EQ = -1                 # mas adv bnd dif src por
#EQ = tfmp_mass  Q1  TFMP_SAT   Q1    0   1       1
#EQ = tfmp_bound Q1  TFMP_PRES  Q1    0   1           1

EQ = shell_curvature  Q1  K    Q1               1
EQ = shell_tension  Q1 TENS  Q1                 1

EQ = mesh1      Q1  D1      Q1       0   0   1   1   0   0
EQ = mesh2      Q1  D2      Q1       0   0   1   1   0   0

#EQ = shell_normal1 Q1  SH_N1 Q1                 1
#EQ = shell_normal2 Q1  SH_N2 Q1                 1
  
#EQ = momentum1  Q1  U1         Q1   0   0   0   0   0   1
#EQ = momentum2  Q1  U2         Q1   0   0   0   0   0   1
#EQ = momentum3  Q1  U3         Q1   0   0   0   0   0   1

END OF EQ

Post Processing Specifications
#Lubrication Saturation = no
#Pressure contours = no
#TFMP_gas_velo = yes
#TFMP_liq_velo = yes
#TFMP_Peclet = yes
#TFMP_Krg = yes
#$TFMP_rho = yes
#$TFMP_mu = yes
#$TFMP_rho_mu = yes
Lubrication Height = yes
#Volumetric Integration Output Format = CSV
#Post Processing Volumetric Integration = 
#VOLUME_INT = POROUS_LIQ_INVENTORY 1 0 volume.csv
#VOLUME_INT = TFMP_FORCE 1 0 force.csv
#END OF VOLUME_INT
