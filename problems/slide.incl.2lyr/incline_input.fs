{include(geometry.in)}

------------------------------------------------------------
                 FEM File Specifications
------------------------------------------------------------
FEM file                         = incline.exoII
Output EXODUS II file            = out.exoII
GUESS file                       = contin.dat
SOLN file                        = soln.dat
Write intermediate results       = no
------------------------------------------------------------
                 General Specifications
------------------------------------------------------------
Number of processors             = 1
Output Level                     = 0
Debug                            = 0
Initial Guess                    = read
------------------------------------------------------------
                 Time Integration Specifications
------------------------------------------------------------
Time integration                 = steady
delta_t                          = 5.0e-7
Maximum number of time steps     = 1000
Maximum time                     = 10.0e+0
Minimum time step                = 1.e-9
Time step parameter              = 0.
Time step error                  = 0.002  1  0  0  1  0
Printing Frequency               = 5
------------------------------------------------------------
                 Solver Specifications
------------------------------------------------------------
Solution Algorithm               = lu
Number of Newton Iterations      = 10
Newton correction factor         = 1
Normalized Residual Tolerance    = 1.0e-13
Residual Ratio Tolerance         = 1.0e-13
------------------------------------------------------------
	Boundary Condition Specifications                 
------------------------------------------------------------
-------------------------------------------------------------
             Related SS bc's on position
-------------------------------------------------------------
$ SET c's to zero for 2D problem 
$   {c1=0} {c2=0} {c3=0} {c4=0} {c5=0} {c6=0} {c7=0} {c8=0}
$
$ Calculate coefficients for general equation a*x + b*y +c*z +d = 0
$   {a1=(y2-y1)/(x1-x2)}
$   {d1=(-y1-a1*x1)}
$   {b1=1}
$
$   {a2=(y3-y2)/(x2-x3)}
$   {d2=(-y2-a2*x2)}
$   {b2=1}
$
$
$   {a4=(y4-y1)/(x1-x4)}
$   {d4=(-y4-a4*x4)}
$   {b4=1}
$
$   {a5=(y20-y21)/(x21-x20)}
$   {d5=(-y20-a5*x20)}
$   {b5=1}
$

Number of BC			 = -1
BC				 = PLANE SS 1 {a1} {b1} {c1} {d1}
BC				 = PLANE SS 2 {a2} {b2} {c2} {d2}
BC				 = PLANE SS 4 {a4} {b4} {c4} {d4}

$$$Parabolic inflow
BC = GD_PARAB SS 2 R_MOMENTUM1 0 MESH_POSITION2 0 0. {-denom*h1} {denom/cos(alpha)/2.}
BC = GD_LINEAR SS 2 R_MOMENTUM1 0 VELOCITY1 0 0. -1.
BC = GD_PARAB SS 2 R_MOMENTUM2 0 MESH_POSITION2 0 0. {-denom*h1*sin(alpha)/cos(alpha)} {denom*sin(alpha)/cos(alpha)/cos(alpha)/2.}
BC = GD_LINEAR SS 2 R_MOMENTUM2 0 VELOCITY2 0 0. -1.

$$Slide face
BC	= U NS 1 0.
BC	= V NS 1 0.

$$ This Combo creates a dead point at the top of the outflow plane
BC      = VELO_TANGENT SS 4 1 0 0 0
$$BC      = VELO_NORMAL SS 3 0.
$$BC      = VELO_NORMAL SS 5 0.
BC      = KINEMATIC SS 3 0.
BC      = CAPILLARY SS 3 1.0 0. 0.
BC      = SURFTANG NS 400 {-sin(PI/2 - alpha)} {-cos(PI/2 - alpha)} 0. -1.0

$$BC      = KINEMATIC_PETROV SS 5 0
$$BC      = CAPILLARY SS 5 1.0 0. 0.
$$BC      = SURFTANG NS 2001 {-sin(PI/2 - alpha)} {-cos(PI/2 - alpha)} 0. -1.0

 
$$ Top side of inflow (Must set this!!!!)
BC      = DX NS 300 {S*(cos(alpha_old)-cos(alpha_new)) -h1*(cos(PI/2-alpha_old)-cos(PI/2-alpha_new))} 1.0
BC      = DY NS 300 {h1*(sin(PI/2-alpha_old)-sin(PI/2-alpha_new))} 1.0
$$ Between two layers at inflow (Must set this!!!!)
BC      = DX NS 2000 {S*(cos(alpha_old)-cos(alpha_new)) -h1*(cos(PI/2-alpha_old)-cos(PI/2-alpha_new))} 1.0
BC      = DY NS 2000 {h1*(sin(PI/2-alpha_old)-sin(PI/2-alpha_new))} 1.0

END OF BC



###########
----
Problem Description
---

Number of Materials = 2

MAT = sample    1

	Coordinate System = CARTESIAN
 
	Element Mapping                  = isoparametric

	Mesh Motion = ARBITRARY
 
	Number of bulk species = 0

	Number of EQ			 = 5
	EQ = mesh1	SP   D1   SP       0.   0.   1.   1.   0.   0.
	EQ = mesh2	SP   D2   SP       0.   0.   1.   1.   0.   0.

	EQ = momentum1  Q2   U1   Q2	   0.   1.   1.   1.   1.   0.
	EQ = momentum2  Q2   U2   Q2	   0.   1.   1.   1.   1.   0.
	EQ = continuity	P1   P    P1   1.                      0.
                                      div  ms  adv  bnd  dif  src  por

MAT = sample1    2

	Coordinate System = CARTESIAN
 
	Element Mapping                  = isoparametric

	Mesh Motion = ARBITRARY
 
	Number of bulk species = 0

	Number of EQ			 = 5
	EQ = mesh1	SP   D1   SP       0.   0.   1.   1.   0.   0.
	EQ = mesh2	SP   D2   SP       0.   0.   1.   1.   0.   0.

	EQ = momentum1  Q2   U1   Q2	   0.   1.   1.   1.   1.   0.
	EQ = momentum2  Q2   U2   Q2	   0.   1.   1.   1.   1.   0.
	EQ = continuity	P1   P    P1   1.                      0.
                                      div  ms  adv  bnd  dif  src  por

Post Processing Specifications

Stream Function = yes
Streamwise normal stress = no
Pressure contours = yes
Second Invarient of Strain = no
Mesh Dilatation = no
Navier Stokes Residuals = yes
Moving Mesh Residuals = yes
Mass Diffusion Vectors = no
Mass Fluxlines = no
Energy Conduction Vectors = no
Energy Fluxlines = no
Time Derivatives = no
Mesh Stress Tensor = no
Mesh Strain Tensor = no
Lagrangian Convection = no
