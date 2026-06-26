#!/usr/bin/env python3

tolerance = 1e-4

def eps_diff(x, y):
    mv = abs(max(x, y))
    if (abs(x - y) / mv) > tolerance:
        return True
    return False


def read_flux(fn):
    with open(fn) as f:
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
                assert l1[1] == "Side_Set"
                name = l1[0]
                l2 = lines[index + 2].strip().split()
                assert l2[0] == "flux="
                flux = float(l2[1])
                area = float(l2[4])
                index += 2
                times.append(time)
                names.append(name)
                fluxes.append(flux)
                areas.append(area)
            else:
                index += 1
        return times, names, fluxes, areas


def read_volume(fn):
    with open(fn) as f:
        lines = f.readlines()
        ll = len(lines)
        index = 0
        voltimes = []
        names = []
        volintes = []
        while index + 2 < ll:
            line = lines[index]
            s = line.strip().split(" ")
            if s[0] == "Time/iteration":
                time = float(s[2])
                l1 = lines[index + 1].strip().split()
                assert l1[1] == "Volume"
                name = l1[0]
                l2 = lines[index + 2].strip().split()
                assert l2[0] == "volume="
                volint = float(l2[1])
                # area = float(l2[4])
                index += 2
                voltimes.append(time)
                names.append(name)
                volintes.append(volint)
                # areas.append(area)
            else:
                index += 1
        return voltimes, names, volintes


test_passed = True

errorstring = ""

flux_files = [
    "flux1.out",
    "flux2.out",
    "flux3.out",
    "flux4.out",
    "flux5.out",
    "flux6.out",
    "flux11.out",
    "flux12.out",
]
blessed_flux_files = [
    "blessed_flux1.out",
    "blessed_flux2.out",
    "blessed_flux3.out",
    "blessed_flux4.out",
    "blessed_flux5.out",
    "blessed_flux6.out",
    "blessed_flux11.out",
    "blessed_flux12.out",
]

volume_files = ["volume1.out", "volume2.out"]
blessed_volume_files = ["blessed_volume1.out", "blessed_volume2.out"]

for f, bf in zip(flux_files, blessed_flux_files):
    times, names, fluxes, areas = read_flux(f)
    btimes, bnames, bfluxes, bareas = read_flux(bf)
    if len(btimes) != len(times):
        errorstring += "%s: Found %d times, expected %d\n" % (
            f,
            len(times),
            len(btimes),
        )
        test_passed = False
    else:
        for i in range(len(times)):
            with open("custTests.txt", "a") as ct:
                print("File = ", f, file=ct)
                print("Time = ", times[i], file=ct)
                print("Known flux = ", bfluxes[i], file=ct)
                print("Found flux = ", fluxes[i], file=ct)
            if eps_diff(fluxes[i], bfluxes[i]):
                errorstring += "%s at %f known: %f\t found: %f\n" % (
                    bfluxes[i],
                    fluxes[i],
                )
                test_passed = False


for f, bf in zip(volume_files, blessed_volume_files):
    times, names, volumes = read_volume(f)
    btimes, bnames, bvolumes = read_volume(bf)
    if len(btimes) != len(times):
        errorstring += "%s: Found %d times, expected %d\n" % (
            f,
            len(times),
            len(btimes),
        )
        test_passed = False
    else:
        for i in range(len(times)):
            with open("custTests.txt", "a") as ct:
                print("File = ", f, file=ct)
                print("Time = ", times[i], file=ct)
                print("Known volume = ", bvolumes[i], file=ct)
                print("Found volume = ", volumes[i], file=ct)
            if eps_diff(volumes[i], bvolumes[i]):
                errorstring += "%s at %f known: %f\t found: %f\n" % (
                    bvolumes[i],
                    volumes[i],
                )
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
