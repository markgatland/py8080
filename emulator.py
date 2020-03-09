import pygame

from cheats import SpaceInvadersCheatEngine
import cpu
import pickle
import time
import ctypes

MIN_WIDTH = 256
MIN_HEIGHT = 224


class Emulator:
    """
    Contains 8080 CPU and uses Pygame to display the VRAM

    Controls:
      1. Press 'c' key to insert coin
      2. Press '1' key to choose 1 player
      3. Press '2' key to choose 2 players
      4. Press arrow keys to move (either player)
      5. Press 'Space' to shoot

    Cheats:
      1. Press 'k' to kill all aliens
      2. Press 's' to die
      3. Press 'l' to add lives
      4. Press 'x' to break score


    """

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    ASPECT_RATIO = MIN_WIDTH / MIN_HEIGHT
    CAPTION_FORMAT = 'Py8080: {}'

    def __init__(self, path=None, width=MIN_WIDTH):
        if path:
            self._cpu = cpu.CPU(path)
            self._cpu.init_instruction_table()
            self._cheats = SpaceInvadersCheatEngine(self._cpu.memory)
        else:
            # From save state
            self._cpu = None
            self._cheats = None

        self._path = path
        self._width = max(MIN_WIDTH, width)
        self._height = round(self._width / self.ASPECT_RATIO)
        self._scaled_width = self._width
        self._scaled_height = self._height
        self._window_width = self._height
        self._window_height = self._width
        self._px_array = None
        self._fps = 60

    def _refresh(self):
        """
        Update the pixel array

        :return:
        """
        j_range = int(self._width * 0.125)
        k_range = j_range // 4

        for i in range(self._height):
            index = self._cpu.VRAM_ADDRESS + (i << 5)

            for j in range(j_range):
                if 23 < j < 28:
                    on = self.RED
                elif 1 < j < 9 or (j < 2 and 24 < i < 136):
                    on = self.GREEN
                else:
                    on = self.WHITE
                vram = self._cpu.memory[index]
                index += 1
                for k in range(k_range):
                    y = self._width - 1 - j*k_range - k

                    if (vram & 0x01) == 1:
                        self._px_array[i][y] = on
                    else:
                        self._px_array[i][y] = self.BLACK

                    vram >>= 1

    def _handle(self, event):
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                self._cpu.io.in_port1 |= 0x01
            if event.key == pygame.K_2:
                self._cpu.io.in_port1 |= 0x02
            if event.key == pygame.K_1:
                self._cpu.io.in_port1 |= 0x04
            if event.key == pygame.K_SPACE:
                self._cpu.io.in_port1 |= 0x10
                self._cpu.io.in_port2 |= 0x10
            if event.key == pygame.K_LEFT:
                self._cpu.io.in_port1 |= 0x20
                self._cpu.io.in_port2 |= 0x20
            if event.key == pygame.K_RIGHT:
                self._cpu.io.in_port1 |= 0x40
                self._cpu.io.in_port2 |= 0x40
            if event.key == pygame.K_6:
                # Save state
                self.save()
            if event.key == pygame.K_s:
                self._cheats.hack_kill_player()
            if event.key == pygame.K_k:
                self._cheats.hack_kill_mobs()
            if event.key == pygame.K_l:
                self._cheats.hack_add_lives()
            if event.key == pygame.K_x:
                self._cheats.hack_score()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_c:
                self._cpu.io.in_port1 &= 255 - 0x01
            if event.key == pygame.K_2:
                self._cpu.io.in_port1 &= 255 - 0x02
            if event.key == pygame.K_1:
                self._cpu.io.in_port1 &= 255 - 0x04
            if event.key == pygame.K_SPACE:
                self._cpu.io.in_port1 &= 255 - 0x10
                self._cpu.io.in_port2 &= 255 - 0x10
            if event.key == pygame.K_LEFT:
                self._cpu.io.in_port1 &= 255 - 0x20
                self._cpu.io.in_port2 &= 255 - 0x20
            if event.key == pygame.K_RIGHT:
                self._cpu.io.in_port1 &= 255 - 0x40
                self._cpu.io.in_port2 &= 255 - 0x40

        if event.type == pygame.VIDEORESIZE:
            self._window_width, self._window_height = event.w, event.h
            if self._window_width < 224:
                self._window_width = 224
            if self._window_height < 256:
                self._window_height = 256
            self._scaled_width = self._window_height
            self._scaled_height = self._window_width
            if self._window_width/self._window_height > self._height/self._width:
                self._scaled_height = int(self._window_height * self._height/self._width)
            if self._window_width/self._window_height < self._height/self._width:
                self._scaled_width = int(self._window_width * self._width/self._height)
            self._window = pygame.display.set_mode((self._window_width, self._window_height), pygame.RESIZABLE)
            self._scaled_surface = pygame.Surface((self._scaled_height, self._scaled_width))

    def save(self):
        """
        Save CPU state to disk

        :return:
        """

        timestamp = round(time.time())
        state_path = 'saves/{}_{}.pickle'.format(self._path, timestamp)
        with open(state_path, 'wb') as state_file:
            pickle.dump(self._cpu, state_file)

    @classmethod
    def load(cls, state):
        """
        Load CPU state from disk

        :param state: Pickle file
        :return:
        """

        with open(state, 'rb') as state_file:
            cpu = pickle.load(state_file)

        emu = cls()
        emu._cpu = cpu
        emu._cheats = SpaceInvadersCheatEngine(cpu.memory)
        return emu

    def run(self):
        """
        Sets up display and starts game loop

        :return:
        """
        ctypes.windll.user32.SetProcessDPIAware()
        pygame.init()
        self._window = pygame.display.set_mode((self._window_width, self._window_height), pygame.RESIZABLE)
        surface = pygame.Surface((self._height, self._width))
        self._scaled_surface = pygame.Surface((self._scaled_height, self._scaled_width))
        caption = self.CAPTION_FORMAT.format(self._path if self._path else '')
        pygame.display.set_caption(caption)
        self._px_array = pygame.PixelArray(surface)
        pygame.display.update()
        fps_clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                self._handle(event)

            self._cpu.run()
            self._refresh()
            fps_clock.tick(self._fps)
            pygame.transform.scale(surface, (self._scaled_height, self._scaled_width), self._scaled_surface)
            horizontal_pos = int((self._window_width - self._scaled_surface.get_width()) / 2)
            vertical_pos = int((self._window_height - self._scaled_surface.get_height()) / 2)
            self._window.blit(self._scaled_surface, (horizontal_pos, vertical_pos))
            pygame.display.update()
