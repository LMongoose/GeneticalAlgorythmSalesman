import pygame
import pygame_gui
from ga import GeneticAlgorithm


class Game():
    def __init__(self, title: str, width: int, height: int):
        pygame.init()
        pygame.display.set_caption(title)
        pygame.display.set_icon(pygame.image.load("icon.png"))
        self.size = width, height
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 20)
        self.manager = pygame_gui.UIManager(self.size)
        self.ga = GeneticAlgorithm()
        self.create_elements()

    def create_elements(self):
        self.lbl_num_cities = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 10), (230, 30)), text="Digite o número de cidades: ", manager=self.manager)
        self.txt_num_cities = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((260, 10), (50, 30)), manager=self.manager)
        self.lbl_pop_size = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 40), (255, 30)), text="Digite o tamanho da população: ", manager=self.manager)
        self.txt_pop_size = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((260, 40), (50, 30)), manager=self.manager)
        self.btn_generate = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 80), (100, 50)), text="Gerar", manager=self.manager)
        self.btn_calculate = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, 80), (100, 50)), text="Calcular", manager=self.manager)
        self.lbl_current_best = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((30, 170), (180, 30)), text="Melhor Caminho Atual: ", manager=self.manager)
        self.area_current_best = pygame.Surface((600, 480))
        self.area_current_best.fill((200, 200, 200))
        self.screen.blit(self.area_current_best, (30, 200))
        self.lbl_total_best = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((650, 170), (180, 30)), text="Melhor Caminho Total: ", manager=self.manager)
        self.area_total_best = pygame.Surface((600, 480))
        self.area_total_best.fill((200, 200, 200))
        self.screen.blit(self.area_total_best, (650, 200))
        self.start_screen = self.screen.copy()
        self.window_error = pygame_gui.windows.ui_message_window.UIMessageWindow(rect=pygame.Rect((300, 200), (100, 80)), window_title="", html_message="", manager=self.manager, visible=False)

    def error(self, title: str, message: str):
        self.window_error = pygame_gui.windows.ui_message_window.UIMessageWindow(rect=pygame.Rect((300, 200), (100, 80)), window_title=title, html_message=message, manager=self.manager)

    def eventhandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if(event.ui_element == self.window_error.close_window_button
                        or event.ui_element == self.window_error.dismiss_button):
                            self.screen.blit(self.start_screen, (0, 0))

                    if event.ui_element == self.btn_generate:
                        self.ga.generate(self)

                    if event.ui_element == self.btn_calculate:
                        self.ga.calculate(self)

            self.manager.process_events(event)

    def mainloop(self):
        self.running = True
        while self.running:
            self.eventhandler()
            self.manager.update(self.clock.tick(60) / 1000.0)
            self.manager.draw_ui(self.screen)
            pygame.display.update()

        pygame.quit()