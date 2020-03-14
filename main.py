from argparse import ArgumentParser

from emulator import Emulator


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--rom', help='Named set of ROM files (space_invaders, lunar_rescue, balloon_bomber)')
    arg_parser.add_argument('--filename', help='Single ROM file')
    arg_parser.add_argument('--state', help='Save state file')
    args = arg_parser.parse_args()

    rom = args.rom
    filename = args.filename
    state = args.state

    if state:
        emu = Emulator.load(state)
    elif rom:
        emu = Emulator(mapname=rom)
    else:
        emu = Emulator(path=filename)

    emu.run()


if __name__ == '__main__':
    main()
