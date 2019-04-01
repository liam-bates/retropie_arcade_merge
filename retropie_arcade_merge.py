"""
Tool to merge the FBA and MAME folders in RetroPie and edit the emulators.cfg
file accordingly. Rather than assume where the files are the tool takes
the paths to the various folders / files as arguments.
"""
import argparse
import os
import shutil
import sys

# Select the filetype for the ROMs
ROMTYPE = '.zip'


def main():
    """
    Main script.
    """
    # Collect command line argument values from function
    args = get_args()

    # Store ROMs in lists
    fba_roms = dir_to_list(args.fba, ROMTYPE)
    mame_roms = dir_to_list(args.mame, ROMTYPE)

    # Copy roms in lists to merged directory
    copy_rom(fba_roms, args.arcade, args.fba)
    copy_rom(mame_roms, args.arcade, args.mame)

    # Amend emulators.cfg config file to reflect the correct emulator for ROMs
    config_editor(args.config, fba_roms, 'lr-fbalpha')
    config_editor(args.config, mame_roms, 'lr-mame2003')

    # Exit with success code
    sys.exit(0)


def get_args():
    """
    Function to ensure appropriate arguments have been provided for the tool and
    to provide help messaging based on the required and optional arguments.
    If appropriate arguments are provided the values are returned.
    """
    # General description of the program
    parser = argparse.ArgumentParser(description="""Tool to merge FBA and
    MAME-2003 folders to a joint arcade folder. The tool will additionally 
    edit the emulators.cfg file to remember which rom is run by which emulator.
    """)
    # Add three mandatory directory arguments, with dir checks function calls
    parser.add_argument("fba", type=check_dir,
                        help="Source directory of FBA ROMs")
    parser.add_argument("mame", type=check_dir,
                        help="Source directory of MAME-2003 ROMs")
    parser.add_argument("arcade", type=check_dir,
                        help="RetroPie arcade directory")
    parser.add_argument("config", type=check_cfg,
                        help="""RetroPie emulators.cfg file""")
    # Assuming no issues return the argument values
    return parser.parse_args()


def check_dir(directory):
    """
    Function to verify that the directory path passed to it exists and is a
    valid directory.
    """
    if not os.path.isdir(directory):
        msg = "{0} is not a directory".format(directory)
        raise argparse.ArgumentTypeError(msg)
    else:
        return os.path.abspath(os.path.realpath(os.path.expanduser(directory)))


def check_cfg(file):
    """
    Function to verify that the filename passed to it is a valid .cfg file.
    """
    if not os.path.isfile(file) or not file.endswith('.cfg'):
        msg = msg = "%r is not a valid config file" % file
        raise argparse.ArgumentTypeError(msg)
    else:
        return file


def dir_to_list(directory, filetype):
    """
    Function to find a filetype in a directory and place the filename in a list
    that is returned.
    """
    filenamelist = []
    for file in os.listdir(directory):
        if file.endswith(filetype) and not file.startswith('.'):
            filenamelist.append(file)
    return sorted(filenamelist)


def copy_rom(copy_list, target_dir, source_dir):
    """
    Function to take a list of matching ROM filenames in two directories (old
    ROMs and new ROMs) and copies these files. A delete list is also taken to
    remove any ROMs that have been renamed.
    """
    for rom in copy_list:
        shutil.copy(source_dir + '/' + rom, target_dir + '/' + rom)
        print('ROM copied to arcade folder: ' + rom)


def config_editor(config_file, game_list, emulator_name):
    """
    Function to append a emulators.cfg file for RetroPie to record the preferred
    emulator for each ROM. This allows MAME and FBA roms to coexist in the same
    directory.
    """
    with open(config_file, 'a') as cfg:
        for rom in game_list:
            cfg.write('arcade_' + rom[:-4] + ' = "' + emulator_name + '"\n')
    print(emulator_name + ' configs applied')


if __name__ == "__main__":
    main()
