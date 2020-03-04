# Written by Benjamin J Cullen
import os
import subprocess

# Path to Configuration & .py Files
config = './config.txt'

# Subprocess Arguments
info = subprocess.STARTUPINFO()
info.dwFlags = 1
info.wShowWindow = 0

loop = True


# Main Menu Function
def main_menu():
    global loop
    print(100 * "-")
    print(45 * ' ' + 'GetPypi_v2')
    print("")
    print("1. Download Modules By OS Category (All OS)")
    print("2. Download Modules By Programming Language (All Programming Languages)")
    print("")
    print("Press Q to Exit")
    print(100 * "-")

    # Input Selection
    choice = input("Select [1-?]: ")

    if choice == "q":
        loop = False

    elif choice == "1":
        funk_1()

    elif choice == "2":
        funk_2()


# Option One Function
def funk_1():
    print('-- option one selected')

    # Confirm Selection
    x = input('Are you sure?')

    # Return To Main Menu
    if x is 'n':
        main_menu()

    # Run The Selected Function
    elif x is 'y':

        # Initiate A List Ready For Python Files
        get_pypi_os = []

        # Populate List With Applicable Python Files
        for dirName, subdirList, fileList in os.walk('./'):
            for fname in fileList:
                if fname.startswith('get_pypi_os_') and fname.endswith('.py'):
                    print(fname)
                    get_pypi_os.append(fname)

        # Algorithm Spawns Multiple Subprocess Each Running A Python Program From The Populated List
        i = 0
        proc_item = []
        for get_pypi_oss in get_pypi_os:
            py_file = get_pypi_os[i]
            cmd = ('python ' + py_file)
            xcmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            proc_item.append(xcmd)
            i += 1

        # Loop Decode And Read Output From Each Spawned Subprocess
        while True:
            i = 0
            for proc_items in proc_item:
                proc = proc_item[i]
                output = proc.stdout.readline()
                if output == '' and proc.poll() is not None:
                    break
                if output:
                    print(output.decode("utf-8").strip())
                i += 1

    # Input Out Of Bounds Re-Run This Function
    else:
        funk_1()


# Option Two Function
def funk_2():
    print('-- option two selected')

    # Confirm Selection
    x = input('Are you sure?')

    # Return To Main Menu
    if x is 'n':
        main_menu()

    # Run The Selected Function
    elif x is 'y':

        # Initiate A List Ready For Python Files
        get_pypi_lang = []

        # Populate List With Applicable Python Files
        for dirName, subdirList, fileList in os.walk('./'):
            for fname in fileList:
                if fname.startswith('get_pypi_lang_') and fname.endswith('.py'):
                    print(fname)
                    get_pypi_lang.append(fname)

        # Algorithm Spawns Multiple Subprocess Each Running A Python Program From The Populated List
        i = 0
        proc_item = []
        for get_pypi_langs in get_pypi_lang:
            py_file = get_pypi_lang[i]
            cmd = ('python ' + py_file)
            xcmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            proc_item.append(xcmd)
            i += 1

        # Loop Decode And Read Output From Each Spawned Subprocess
        while True:
            i = 0
            for proc_items in proc_item:
                proc = proc_item[i]
                output = proc.stdout.readline()
                if output == '' and proc.poll() is not None:
                    break
                if output:
                    print(output.decode("utf-8").strip())
                i += 1

    # Input Out Of Bounds Re-Run This Function
    else:
        funk_2()


# Loop until loop = False
while loop is True:
    
    # Display Main Menu
    main_menu()
