import pygame
import sys

class Menu:
    def __init__(self, options, width, height):
        self.options = options
        self.font = pygame.font.Font(None, 36)
        self.option_rects = []
        self.selected_option = None
        self.width = width
        self.height = height

        self._create_option_rects()

    def _create_option_rects(self):
        for i, option in enumerate(self.options):
            text_surface = self.font.render(option, True, (0, 0, 0))
            rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 + i * 50))
            self.option_rects.append((option, rect))

    def display(self, screen):
        while not self.selected_option:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for option, rect in self.option_rects:
                        if rect.collidepoint(event.pos):
                            self.selected_option = option

            screen.fill((20,156,250))
            for option, rect in self.option_rects:
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)
                screen.blit(self.font.render(option, True, (0, 0, 0)), rect)
            pygame.display.flip()

            pygame.time.Clock().tick(60) 

        return self.selected_option
