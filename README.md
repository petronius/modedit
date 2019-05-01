# EU4/Paradox Modding tools

A small plugin to make working on mods for Paradox games easier.

## Setup

Download the contents of this repository to your Sublime `Packages/modeditor` directory.

Recommended other packages:

* Taw's syntax highlighting for Paradox files: https://packagecontrol.io/packages/Paradox

## Settings

```javascript
{
    // Path to the game files you want to browse in read-only mode
    "edit_tree": "/Users/schuller_michael/Library/Application Support/Steam/steamapps/common/Europa Universalis IV",
    // Path to the project directory where you want copies of edited game files to be placed
    "project_dir": "/Users/schuller_michael/workspace/personal-projects/sola-fide/SolaFide",
    // List of file extensions that should have the syntax file applied
    "syntax_sigil": [
        ".txt"
    ],
    // List of file endings that should never be editable in Sublime
    "noedit_sigil": [
        ".dds"
    ],
    // Syntax file to apply to the endings above
    "syntax_file": "Packages/Paradox/Paradox.tmLanguage",
    // Shell command to run to open an image file
    "image_open_cmd": "open %s -a GIMP.app"
}
```

## Commands

After cusomizing the settings, run `ModEdit: Start` in the command menu (CTRL/CMD + SHIFT + P) to open the base game directory and your mod directory in the sidebar.

When browsing files, you can run `ModEdit: Show original` or `ModEdit: Overwrite` to flip between the mod version and the base game version of a file. When running the overwrite command, a copy of the base game file will be created in the mod directory if it does not already exit.

Run `ModEdit: Edit image` on a file to open it in the specified image editor.