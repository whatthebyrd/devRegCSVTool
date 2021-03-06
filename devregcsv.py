#!/usr/bin/env python3

# devregcsv
# Invoke by: devregcsv
# Creates a CSV file containijng specified device details for a group of devices.
# Originally converted from JPetruno's Excel script of the same name.
# Original Creation: 28AUG21
# Released under GNU 3.0 License

import sys  # Used to determine number of args passed for program mode
import datetime  # Used to provide date & time for filename

# Define vars. Most defined inline for the "Guided" mode, however this allows for a "headless" mode in the future.
relV = "30.00"  # Release version number
caseNum = "00000"  # Case number
devNum = 0  # The number internally assigned to each device. Can be used as a counter.
devNumSeed = 1  # The number at which to start numbering devices.
devEUIseed = "FFFFFF0100000000"  # The initial value of the EUI. Initially modified by devNumSeed and then by device.
contId = ""  # Default contract ID
profID = ""  # Default profile ID
latSeed = 39.8283  # Initial latitude. 39.8283N, 98.5795W = geographic center of CONUS.
longSeed = 98.5795  # Initial longitude. 39.8283N, 98.5795W = geographic center of CONUS.
latIncr = 0.0001  # Value by which to increment each device's latitude.
longIncr = 0.0001  # Value by which to increment each device's longitude.
devType = "DEVICE"  # Name of default device type.
devClass = "CLASS_A"  # Device class default.
fwVer = "1.02.03.04"  # Default fw version for device.

if len(sys.argv) == 1:  # Guided process
    print("\n\nDevRegCSV tool")
    relV = input("To begin, please specify the relv:\n")
    print("Relv is set to " + relV + "\n")

    caseNum = input("\nPlease enter the case # associated with these devices:\n")
    print("Case # is: " + caseNum + "\n")

    devNum = int(input("\nPlease enter the number of devices you would like listed:\n"))
    if devNum == 0:
        print("Number of devices to list must be greater than 0.\n")
        devNum = int(input("Please enter the number of devices you would like listed: \n"))
        if devNum == 0:
            print("Number of devices to list must be greater than 0.\nExiting.\n")
            exit()
    print(str(devNum) + " devices will be listed.\n")

    devNumSeed = int(input("\nPlease enter the device # you would like to start the list at: "
                           "(e.g. 1 will have the first device listed as device #1)\n"))
    print("Device numbering will start at " + str(devNumSeed) + ".\n")

    print("\nDefault EUI seed is set to " + devEUIseed + " with the first EUI being " + f"{(int(devEUIseed, 16) + devNumSeed):X}" + ".")
    chgSeed = input("Would you like to change it? y/n\n")
    if chgSeed == "y":
        devEUIseed = input("Please input the new EUI seed:\n")
        print("New EUI seed is " + devEUIseed + ".\n")

    contrIdChg = input("\nThe default contractID is blank. Would you like to change it? y/n\n")
    if contrIdChg == "y":
        contrId = input("Please input the new contractID:\n")
        print("New contractID is " + contrId + ".\n")
    else:
        contrId = ""

    profIdChg = input("\nThe default profID is blank. Would you like to change it? y/n\n")
    if profIdChg == "y":
        profId = input("Please input the new profID:\n")
        print("New profID is " + profId + ".\n")
    else:
        profId = ""

    print("\nThe current lat/long seed is set to " + str(latSeed) + "N, " + str(longSeed) + "W.")
    llChg = input("Would you like to change it? y/n\n")
    if llChg == "y":
        latSeed = float(input("Please input the new lat in decimal:\n"))
        print("New lat seed is " + str(latSeed) + "N.\n")
        longSeed = float(input("Please input the new long in decimal:\n"))
        print("New long seed is " + str(longSeed) + "W.\n")
    else:
        print("Lat/long is set at " + str(latSeed) + "N, " + str(longSeed) + "W.\n")

    print("\nThe default value to increment lat is " + str(latIncr) + " and long is " + str(longIncr) + ".")
    chgIncr = input("Would you like to change it? y/n\n")
    if chgIncr == "y":
        latIncr = float(input("Please input the new lat increment in decimal:\n"))
        print("New lat increment is " + str(latIncr) + "N.\n")
        longIncr = float(input("Please input the new long increment in decimal:\n"))
        print("New long increment is " + str(longIncr) + "W.\n")
    else:
        print("Lat/long increments are set at " + str(latIncr) + " and " + str(longIncr) + " respectively.\n")

    tags = "Relv" + relV + " - Case " + caseNum + ": Device-" + str(devNumSeed) + " Tag"
    metadata = "Device-" + str(devNumSeed) + " Metadata"

    print("\nThe default tags are \"" + tags + "\".")
    chgTags = input("Would you like to change them? y/n\n")
    if chgTags == "y":
        tags = input("Please input the new tags:\n")
        print("New tags are \"" + tags + "\".\n")
    else:
        print("Tags are set at \"" + tags + "\".\n")

    print("\nThe default metadata is \"" + metadata + "\".")
    chgMd = input("Would you like to change it? y/n\n")
    if chgMd == "y":
        metadata = input("Please input the new metadata:\n")
        print("New metadata is \"" + metadata + "\".\n")
    else:
        print("Metadata is \"" + metadata + "\".\n")

    chgDevType = input("\nThe default device type is \"" + devType + "\". Would you like to set a device type? y/n\n")
    if chgDevType == "y":
        devType = input("Please input the new device type:\n")  # Add dict/tuple for device types?
        print("New device type is \"" + devType + "\".\n")
    else:
        print("Device type is \"" + str(devType) + "\".\n")

    chgDevClass = input("\nThe default device class is \"CLASS_A\". Would you like to set a device class? y/n\n")
    if chgDevClass == "y":
        devClass = input("Please input the new device class:\n")  # Add dict/tuple for device classes?
        print("New device class is \"" + devClass + "\".\n")
    else:
        print("Device class is \"" + devClass + "\".\n")

    chgFWver = input("\nThe default fwVer is \"" + fwVer + "\". Would you like to input a new fwVer? y/n\n")
    if chgFWver == "y":
        fwVer = input("Please input the new fwVer:\n")
        print("New fwVer is \"" + fwVer + "\".\n")
    else:
        print("Device fwVer is \"" + fwVer + "\".\n")

    # Add an option to specify the path.

    proceed = input("\nThe CSV file will be output into the CWD. Would you like to proceed? y/n\n")
    if proceed == "n":
        print("Exiting.")
        exit()

today = datetime.datetime.now()
filename = today.strftime("%d%b%y-%H%M")
count = 0
csvfile = open(f"{filename}.csv", "x")
csvfile.write("devEUI, appKey, contractId, profId, lat, long, tags, metadata, devType, devClass, fwVer\n")
devNumID = devNumSeed
devEUI = int(devEUIseed, 16) + devNumSeed
appKey = str(devEUI) * 2
lat = latSeed
long = longSeed

while count != devNum:
    appKey = f"{devEUI:X}" * 2
    devLine = f"{devEUI:X},{appKey},{contrId},{profId},{lat:.4f},{long:.4f},{tags},{metadata},{devType},{devClass},{fwVer}\n"
    csvfile.write(devLine)
    devNumID += 1
    devEUI +=1
    if chgTags != "y":
        tags = "Relv" + relV + " - Case " + caseNum + ": Device-" + str(devNumID) + " Tag"
    if chgMd != "y":
        metadata = "Device-" + str(devNumID) + " Metadata"
    lat += latIncr
    long += longIncr
    count += 1

sys.exit(f"CSV is output in CWD at {filename}.csv with {devNum} devices listed.\nExiting.")
