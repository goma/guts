$ Roll radius			{radius = 10.} 10 cm
$ Roll speed			{omega = 1e-5}
$ target thickness		{hf = 10.00e-5} 100 nm
$ domain entrance thickness     {ho = 1e-4} 1 micron
$ wrap angle	  		{theta_w = 50} degrees
$ minimum init thickness        {hmin = 1e-4}

$ atmospheric pressure		{Patm = 0.0}
$ boundary pressure		{boundary_pressure = 0}
$ stretching force		{stretch = 10000} cgs -> 10 [N/m]
$ Shell bending stiffness       {shell_bend_stiff = 0}
$ Shell extensional stiffness   {shell_ext_stiff = 5.686e12}
$ Shell Poisson ratio           {shell_poisson = 0.3}
$ Contact Angle			{contact_angle = 0.0}
$ Surface Tension 	 	{surface_tension = 35}
$ Element Size			{element_size = 10e-4}
$ Gap closure rate              {dh_dt = -1e-6}
$ Streamline-Upwind/Petrov Galerkin weighting factor
$  			   	{supg = 0.0}

$ Time Step Parameter		{tsp = 0.0}
$ Gas Viscosity			{mu_g1 = 18.6e-5}
$ Gas Viscosity			{mu_g = 18.6e-5}
$ Liquid Viscosity		{mu_l = 0.01}
$ Gas Density			{rho_g = 1.18}
$ Liquid Density		{rho_l = 0.998}
$ Viscosity Error		{beta_mu = 0}
$ Density Error			{beta_rho = 0}
$ Backwards Diffusivity		{bdif = 1e-6}
$ Thin Film Multiphase Mass Lumping
$				{tfmp_ml = "yes"}

$ Thin Film Multiphase Clipping {tfmp_clip = "no"}

$ Thin Film Multiphase Clip strength
$				{tfmp_clip_strength = "1e-1"}

$ Thin Film Multiphase Diffusivity Transition Center
$     	    	       		{tfmp_diff_center = 0.88}

$ Thin Film Multiphase Diffusivity Transition Half-Length
$      	    	       		{tfmp_beta_d = 01.2}

$ Thin Film Multiphase Gas Permeability Transition Center
$      	    	       	   	{Scg = 0.5}

$ Thin Film Multiphase Gas Permeability Transition Half-Length
$      	    	       	   	{alphag = 0.5}

$ Thin Film Multiphase Liquid Permeability Transition Center
$      	    	       	        {Scl= 0.5}

$ Thin Film Multiphase Liquid Permeability Transition Half-Length
$      	    	       	        {alphal = 0.5}

$ Normalized Residual Tolerance	{nrt = 1e-11}

$ Thin Film Multiphase Gas Molecular Weight
$     	    	       	   	{Mg = 44.01}

$ Thin Film Multiphase Dissolved Gas Diffusivity
$      	    	       		{Dgl = 2.233e-5}

$ Thin Film Multiphase Henry's Law Constant
$      	    	       	        {Hgls = 3.3555e-11}

$ Thin Film Multiphase Drop Lattice Spacing
$      	    	       	    	{lattice_spacing = 160e-4}

$ Thin Film Multiphase Drop Lattice Volume
$      	    	       	    	{drop_volume = 6e-9}
