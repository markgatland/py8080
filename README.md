# py8080


![Screenshot](https://i.imgur.com/OBVL5ez.png "Screenshot")

py8080, upgraded to include a resizable window, audio, and TV/Midway colours for Space Invaders. I've also implemented the remaining CPU instructions, so it passes the CPUDIAG.asm test.

## Usage

```bash
python main.py --rom <name of rom file group>

# or load a single ROM file

python main.py --filename <name of file in rom/ directory>

# or load a save state

python main.py --state <name of state file in saves/ directory>
```

If no rom/filename is provided, defaults to Space Invaders demo.

Avaliable ROMs are `space_invaders`, `lunar_rescue` and `balloon_bomber`. Place the files for each (invaders.h, invaders.g, etc.) in the `rom/` directory.

Provide sound files in `sound/` folder, these are .wav files that can be found on the internet named `0.wav` through `18.wav`, although only 0-8 are required.

## Controls

1. Press `c` key to insert coin
2. Press `1` key to start 1-player game
2. Press `2` key to start 2-player game
3. Press arrow keys to move (either player)
4. Press `Space` to shoot
5. Press `6` to save state

Cheats:
1. Press `k` to kill all aliens
2. Press `s` to die
3. Press `l` to add lives
4. Press `x` to break score


### Added features

* Simulated colour strips from the TV/Midway versions of Space Invaders
* Simulated audio from Space Invaders
* Resizable window that maintains aspect ratio
* Print method for use with CPUDIAG test (be sure to load this in starting at memory location `0x100`)
* Implemented remaining instructions and fixed errors
* Added memory maps for three games, so ROM files (eg. invaders.h, invaders.g) don't need to be concatenated

### Notes

* Screen colours for games other than Space Invaders will be incorrect
* Balloon Bomber plays fine, but halts during attract mode
