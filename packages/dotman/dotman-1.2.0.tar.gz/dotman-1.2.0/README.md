# dotman
Manage your dotfiles easily.

## Installation
`python3 setup.py install`

## Running
- `dotman -a APP_NAME`
Links all the files under directory `APP_NAME` to its suitable place relative to your home directory.
- `dotman -a  APP_NAME -d /tmp/mylinksroot` 
Links all the files under APP_NAME relative to `/tmp/mylinksroot` directory
- `dotman -a APP_NAME -s -v`
Runs a simulation on the filesystem.


## Dotfiles layout
```
        i3
        `-- .config
            `-- i3
                `-- config
```
So we have here a directory named i3 in the very top `indicates APP_NAME` and under it a tree of config paths. Here it means `config` file is supposed to be linked under `.config/i3/config` related to the home directory.

## Why?
I used to use stow, and for some reason it stopped working correctly, and I really didn't want to spend time reading perl code :( 