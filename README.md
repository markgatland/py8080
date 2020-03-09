# py8080


![Screenshot](https://i.imgur.com/OBVL5ez.png "Screenshot")

py8080, modified to include a resizable window and TV/Midway colours.

I started off by writing my own Intel 8080 emulator in Python, and although it works it isn't really worth sharing on GitHub (it achieves the same results as [matthewmpalen](https://github.com/matthewmpalen/py8080)'s emulator, but has a seperate method for almost every opcode). Making my own helped me understand things, but rather than try to refactor that code into something that will eventually resemble an existing project, I decided I'd be better off building upon the existing project in question.

## Usage

```bash
python main.py --filename <filename>

# or load a save state

python main.py --state saves/<state file>
```

If no filename is provided, defaults to Space Invaders demo. (File can be created by concatenating Space Invaders ROM files in the order: invaders.h, invaders.g, invaders.f, invaders.e)

## Controls

1. Press `c` key to insert coin
2. Press `1` key to start 1-player game
2. Press `2` key to start 2-player game
3. Press arrow keys to move
4. Press `Space` to shoot
5. Press `6` to save state

Cheats:
1. Press `s` to kill player (suicide)
2. Press `k` to kill mobs
3. Press `l` to add lives
4. Press `x` to break score

### To-do

* Add CP/M print method for CPUDIAG program
* Fix incorrect Parity flag setting (currently indicates parity instead of *bit* parity)
* Add jumps/calls for Parity flag
* Fix Carry arithmetic
* Add sound
* Add memory mapping functionality (so .e, .f, .g, etc. files are used instead of a single file)

### Notes

1. Still contains unimplemented instructions
2. Rendered using [Pygame](https://www.pygame.org/wiki/GettingStarted)
