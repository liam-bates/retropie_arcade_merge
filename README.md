# retropie_arcade_merge

Tool to merge FBA and MAME-2003 folders to a joint arcade folder. The tool will additionally edit the emulators.cfg file to remember which rom is run by which emulator.

## Usage

Usage: ```python3 retropie_arcade_merge.py [-h] fba mame arcade config```

### Mandatory arguments

* ```fba``` Source directory of Final Burn Alpha ROMs.
* ```mame``` Source directory of MAME ROMs.
* ```arcade``` Target RetroPie arcade directory where the ROMs will be merged to.
* ```config``` Target RetroPie emulators.cfg file to record the correct emulator for each ROM.

### Optional arguments

* ```-h``` Show help message
