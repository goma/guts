#!/usr/bin/env python3

frequency = 1e8
known_scattering = 3667.96
known_absorption =  -6.7456004e+02
tolerance = 1e-2

def eps_diff(x,y):
    mv = abs(max(x,y))
    if (abs(x-y)/mv) > tolerance:
        return True 
    return False

with open('sigma_scattering.out') as f:
    lines = f.readlines()
    ll = len(lines)
    index = 0
    times = []
    names = []
    fluxes = []
    areas = []
    while index + 2 < ll:
        line = lines[index]
        s = line.strip().split(" ")
        if s[0] == "Time/iteration":
            time = float(s[2])
            l1 = lines[index + 1].strip().split()
            assert (l1[1] == "Side_Set")
            name = l1[0]
            l2 = lines[index + 2].strip().split()
            assert (l2[0] == "flux=")
            flux = float(l2[1])
            area = float(l2[4])
            index += 2
            times.append(time)
            names.append(name)
            fluxes.append(flux)
            areas.append(area)
        else:
            index += 1

with open('abs_cs.out') as f:
    lines = f.readlines()
    ll = len(lines)
    index = 0
    voltimes = []
    names = []
    volintes = []
    areas = []
    while index + 2 < ll:
        line = lines[index]
        s = line.strip().split(" ")
        if s[0] == "Time/iteration":
            time = float(s[2])
            l1 = lines[index + 1].strip().split()
            assert (l1[1] == "Volume")
            name = l1[0]
            l2 = lines[index + 2].strip().split()
            assert (l2[0] == "volume=")
            volint = float(l2[1])
            #area = float(l2[4])
            index += 2
            voltimes.append(time)
            names.append(name)
            volintes.append(volint)
            #areas.append(area)
        else:
            index += 1

test_passed = True

errorstring = ""

if len(times) != 1 and len(voltimes) != 1:
    errorstring += "Found (%s,%s) times, expected (1,1)\n" % (len(times),len(voltimes))
    test_passed = False

#print("Testing frequency")
#print("Known:", frequency)
#print("Found:", times[0])
#if test_passed and eps_diff(frequency, times[0]):
#    errorstring += "Frequency different, known: %f\t found: %f\n" % (known_absorption, fluxes[0])
#    test_passed = False

with open("custTests.txt", "w") as f:
    print("Testing scattering cross section", file=f)
    print("Known:", known_scattering, file=f)
    print("Found:", fluxes[0], file=f)
if eps_diff(known_scattering, fluxes[0]):
    errorstring += "Scattering cross section different, known: %f\t found: %f\n" % (known_scattering, fluxes[0])
    test_passed = False

with open("custTests.txt", "a") as f:
    print("Testing absorption cross section", file=f)
    print("Known:", known_absorption,file=f)
    print("Found:", volintes[0],file=f)
if eps_diff(known_absorption, volintes[0]):
    errorstring += "Absorption cross section different, known: %f\t found: %f\n" % (known_absorption, volintes[0])
    test_passed = False

if not test_passed:
    with open("custTests.txt", "a") as f:
        print(errorstring, file=f)

with open("extra_test_code.txt", "w") as f:
    if test_passed:
        f.write("OK")
    else:
        f.write("FAILED")

with open("custTests.txt", "a") as f:
    if test_passed:
        f.write("All tests passed\n")
    else:
        f.write(errorstring)
