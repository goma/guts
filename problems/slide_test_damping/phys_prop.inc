####################################################
#########                               ############
######### Geometry Aprepro Include	 ############
#########                               ############
####################################################

########### Geometry specification #################

# Inclination   from horizontal = {alpha = 30.0}
# Web inclination from vertical = {beta  = 30.0}
# Gap height = {H_gap = 3.0e-2} cm


### Layer 1 ####
# Feed slot length  = {L_slot_1 = 5.0e-1} cm
# Feed slot width = {W_slot_1 = 1.0e-1} cm
# Feed slot offset = {L_offset_1 = 2.54e-2} cm
# Corner radius = {R_offset_1 = 1.5e-2}
# Slide length = {L_slide_1 = 5.0} cm
# Corner radius = {R_slot_1 = 7.62e-2} cm
# Die lip radius = {R_lip = 5.08e-2} cm
# Static contact line position w.r.t. die edge {L_static = 4.0e-2} cm
# Layer 1 thickness {T_thick_1 = 1.3e-1}

### Layer 2 ####
# Feed slot length  = {L_slot_2 = 5.0e-1}
# Feed slot width = {W_slot_2= 1.0e-1}
# Feed slot offset = {L_offset_2 = 2.54e-2}
# Corner radius = {R_offset_2 = 1.5e-2}
# Length between slot exit of layer 1 and 2 = {L_slide_1_2 = 3.0}
# Corner radius = {R_slot_2 = 7.62e-2}

### Layer 3 ####
#Feed slot length  = {L_slot_3 = 5.0e-1}
#Feed slot width = {W_slot_3= 1.0e-1}
#Feed slot offset = {L_offset_3 = 2.54e-2}
#Corner radius = {R_offset_3 = 1.5e-2}
#Length between slot exit of layer 2 and 3 = {L_slide_2_3 = 3.0}
#Corner radius = {R_slot_3 = 7.62e-2}


### Web ####
# Web length from edge of slide to downstream= {L_web_down = 2.0} cm

######## Geometry calculation ###########

### Normal and tangent vectors ###

# x component of normal to web = {nx_web = -cosd(beta)}
# y component of normal to web = {ny_web =  sind(beta)}

# x component of tangent to web = {tx_web = sind(beta)}
# y component of tangent to web = {ty_web = cosd(beta)}

# Slope of the slide = {slope_slide = -tand(alpha)}
# Slope of the web   = {slope_web = tand(90.0 - beta)}

### Mesh fences ####

# Total slide length - layer 2 = {L_slide_2 = L_slide_1 + W_slot_1 + R_slot_1 + R_offset_1 +  L_slide_1_2}
# Total slide length - layer 3 = {L_slide_3 = L_slide_2 + W_slot_2 + R_slot_2 + R_offset_2 + L_slide_2_3}

# x position of slide end position = {x_slide_end =  R_lip * (sind(alpha) - 1.0)}
# y position of slide end position = {y_slide_end =  R_lip * cosd(alpha)}

# Mesh fence location from end of slide die straight edge {L_takeoff_1 = 3.5e-1} cm
# x position of mesh fence: Slide-lip = {x_slide_lip = x_slide_end - L_takeoff_1 * cosd(alpha)}
# y position of mesh fence: Slide-lip = {y_slide_lip = y_slide_end + L_takeoff_1 * sind(alpha)}
# Slope of mesh fence: Slide-lip = {slope_slide_lip = tand(90.0 - alpha)}

# x position of mesh fence: Exit-slide - layer 1 = {x_exit_1 = x_slide_end - L_slide_1  * cosd(alpha)}
# y position of mesh fence: Exit-slide - layer 1 = {y_exit_1 = y_slide_end + L_slide_1  * sind(alpha)}
# Slope of mesh fence: Exit-slide - layer 1 = {slope_exit_1 = tand(90.0 - alpha)}

# x position of mesh fence: Slot-exit - layer 1 = {x_slot_1 = x_exit_1 - (R_slot_1 + W_slot_1)  * cosd(alpha) - R_slot_1 * sind(alpha)}
# y position of mesh fence: Slot-exit - layer 1 = {y_slot_1 = y_exit_1 + (R_slot_1 + W_slot_1)  * sind(alpha) - R_slot_1 * cosd(alpha)}
# Slope of mesh fence: Slot-exit - layer 1 = {slope_slot_1 = -tand(alpha)}

# x position of mesh fence: Slide 2 to slide 1 = {x_slide_2_1 = x_slot_1 + (R_slot_1 + L_offset_1 + R_offset_1) * sind(alpha) - (R_offset_1 + 0.01 * L_slide_1_2) * cosd(alpha)}
# y position of mesh fence: Slide 2 to slide 1 = {y_slide_2_1 = y_slot_1 + (R_slot_1 + L_offset_1 + R_offset_1) * cosd(alpha) + (R_offset_1 + 0.01 * L_slide_1_2) * sind(alpha)}
# Slope of mesh fence: Slide 2 to slide 1 = {slope_slide_2_1 = tand(90.0 - alpha)}

# x position of mesh fence: Exit-slide - layer 2 = {x_exit_2 = x_slide_2_1 - 0.99 * L_slide_1_2  * cosd(alpha)}
# y position of mesh fence: Exit-slide - layer 2 = {y_exit_2 = y_slide_2_1 + 0.99 * L_slide_1_2  * sind(alpha)}
# Slope of mesh fence: Exit-slide - layer 2 = {slope_exit_2 = tand(90.0 - alpha)}

# x position of mesh fence: Slot-exit - layer 2 = {x_slot_2 = x_exit_2 - (R_slot_2 + W_slot_2)  * cosd(alpha) - R_slot_2 * sind(alpha)}
# y position of mesh fence: Slot-exit - layer 2 = {y_slot_2 = y_exit_2 + (R_slot_2 + W_slot_2)  * sind(alpha) - R_slot_2 * cosd(alpha)}
# Slope of mesh fence: Slot-exit - layer 2 = {slope_slot_2 = -tand(alpha)}

# x position of mesh fence: Slide 3 to slide 2 = {x_slide_3_2 = x_slot_2 + (R_slot_2 + L_offset_2 + R_offset_2) * sind(alpha) - (R_offset_2 + 0.01 * L_slide_2_3) * cosd(alpha)}
# y position of mesh fence: Slide 3 to slide 2 = {y_slide_3_2 = y_slot_2 + (R_slot_2 + L_offset_2 + R_offset_2) * cosd(alpha) + (R_offset_2 + 0.01 * L_slide_2_3) * sind(alpha)}
# Slope of mesh fence: Slide 3 to slide 2 = {slope_slide_3_2 = tand(90.0 - alpha)}

# x position of mesh fence: Exit-slide - layer 3 = {x_exit_3 = x_slide_3_2 - 0.99 * L_slide_2_3  * cosd(alpha)}
# y position of mesh fence: Exit-slide - layer 3 = {y_exit_3 = y_slide_3_2 + 0.99 * L_slide_2_3  * sind(alpha)}
# Slope of mesh fence: Exit-slide - layer 3 = {slope_exit_3 = tand(90.0 - alpha)}

# x position of slot exit - layer 3 = {x_slot_exit_3 = x_exit_3 - (R_slot_3 + W_slot_3)  * cosd(alpha)}
# y position of slot exit - layer 3 = {y_slot_exit_3 = y_exit_3 + (R_slot_3 + W_slot_3)  * sind(alpha)}
# Slope of slot exit - layer 3 = {slope_slot_exit_3 = tand(90.0 - alpha)}

# x position of web starting point = {x_web_start =  H_gap * cosd(alpha)}
# y position of web starting point = {y_web_start = -H_gap * sind(alpha)}

# Mesh fence location from start of web surface {L_landing = 4.0e-1} cm
# x position of mesh fence: Bead-web = {x_bead_web = x_web_start + L_landing * sind(beta)}
# y position of mesh fence: Bead-web = {y_bead_web = y_web_start + L_landing * cosd(beta)}
# Slope of mesh fence: Bead-web = {slope_bead_web = -tand(beta)}

# x position of outlet = {x_outlet = x_web_start + L_web_down * sind(beta)}
# y position of outlet = {y_outlet = y_web_start + L_web_down * cosd(beta)}
# Slope of outlet = {slope_outlet = -tand(beta)}


####################################################
#########                               ############
######### Mat Prop Aprepro Include	############
#########                               ############
####################################################

# Gravity = {grav = 980.0} cm/s^2

### Layer 1 ####
# Density = {rho_1 = 1.0} g/cm^3
# Viscosity = {visc_1 = 2} Poise
# Low rate viscosity = {mu_0_1 = 100.0} Poise
# Power law exponent = {nexp_1 = 0.2}
# High rate viscosity = {mu_inf_1 = 0.3} Poise
# Time constant = {tau_1 = 0.45} s
# Aexp = {Aexp_1 = 4.0}
# Surface tension = {surf_tens_1 = 30.0} dyne/cm

### Layer 2 ####
# Density = {rho_2 = 1.0} g/cm^3
# Viscosity = {visc_2 = 2.3} Poise
# Low rate viscosity = {mu_0_2 = 30.0} Poise
# Power law exponent = {nexp_2 = 0.0}
# High rate viscosity = {mu_inf_2 = 1.5} Poise
# Time constant = {tau_2 = 100.0} s
# Aexp = {Aexp_2 = 2.0}
# Surface tension = {surf_tens_2 = 30.0} dyne/cm

### Layer 3 ####
# Density = {rho_3 = 1.0} g/cm^3
# Viscosity = {visc_3 = 2.0} Poise
# Low rate viscosity = {mu_0_3 = 30.0} Poise
# Power law exponent = {nexp_3 = 0.49}
# High rate viscosity = {mu_inf_3 = 0.15} Poise
# Time constant = {tau_3 = 350.0} s
# Aexp = {Aexp_3 = 1.0}
# Surface tension = {surf_tens_3 = 30.0} dyne/cm


####################################################
#########                               ############
#########    Operating Condition        ############
#########    Aprepro Include	        ############
#########                               ############
####################################################

# Web speed = {U_web = 1.5} cm/s
# Upstream pressure = {P_vac = -1.5e3} {-1.75e+3} dyne/cm^2

# Film thickness on web - layer 1 = {h_web_1 = 3.0e-2} cm
# Film thickness on web - layer 2 = {h_web_2 = 1.3e-2} cm
# Film thickness on web - layer 3 = {h_web_3 = 1.0e-2} cm

# Flowrate layer 1 = {flowrate_1 = U_web * h_web_1} cm^2/s
# Flowrate layer 2 = {flowrate_2 = U_web * h_web_2} cm^2/s
# Flowrate layer 3 = {flowrate_3 = U_web * h_web_3} cm^2/s


# Static contact angle at die face surface = {CA_die = 60.0}
# Dynamic contact angle at web surface = {DCA = 120.0}

# Slip coefficient at dynamic contact line = {beta_slip = 1.0e-4}
# Slip length from dynamic contact line = {slip_dist = 1.0e-3} cm
