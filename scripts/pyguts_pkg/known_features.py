KNOWN_FEATURES: frozenset = frozenset({
    # Bulk physics
    "maxwell", "free_surface", "thermal", "solid_mechanics", "electrostatics",
    "voltage", "viscoelastic", "newtonian", "suspension", "reaction", "species",
    "chemkin", "no_chemkin", "discontinuous_variables", "energy", "porous_media",
    # Coordinate systems
    "cartesian", "cylindrical", "spherical", "swirling", "shell", "shell_mechanics",
    "3d", "2d", "1d",
    # Algorithm features
    "level_set", "volume_of_fluid", "parallel", "serial", "moving_mesh",
    "fixed_mesh", "overlapping_meshes", "pspg", "eigen", "arpack",
    "adaptive", "segregated",
    # Solvers
    "lu", "front", "gmres", "umf", "aztec", "amesos2", "amesos", "trilinos",
    "cgs", "petsc_complex", "petsc", "superlu", "mumps",
    # Solution methods
    "steady", "transient", "continuation", "augmenting_conditions",
})
