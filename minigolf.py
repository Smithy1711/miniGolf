import pygame as pg
import sys

class Game:
    def __init__(self):
        pg.init()

        self.current_screen = "main"

        self.screen_width = 800
        self.screen_height = 600
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("Blank Screen")
        self.clock = pg.time.Clock()
        self.is_running = True

        self.font = pg.font.Font(None, 36)  # None for default font, 36 is the font size

        self.button_width = 250
        self.button_height = 120
        self.button_play_coord = ((self.screen_width - self.button_width)/2, (self.screen_height - self.button_height)/2)

        self.radius = 10
        self.ball_centre_coord = ((10,10))

        self.power_bar_image = pg.image.load("images/powerbar.jpg")

        self.power_line_coord = [0, self.screen_height - 20]
        

    def run(self):
        while self.is_running:
            if self.current_screen == "main":
                self.loadMainScreen()
                self.handle_main_screen_events()
            elif self.current_screen == "gameload":
                self.loadGameScreen()
            elif self.current_screen == "game":
                self.runGame()
                

            self.update()
            self.clock.tick(60)

    def loadMainScreen(self):
        self.screen.fill((0, 255, 255))
        pg.draw.rect(self.screen, (0, 102, 0), (0, self.screen_height*2/3, self.screen_width, self.screen_height // 3))
        pg.draw.rect(self.screen, (128, 128, 128), (self.button_play_coord[0], self.button_play_coord[1], self.button_width, self.button_height))

        play_text = self.font.render("Play", True, (0, 0, 0))

        # Calculate the position for the text
        text_x = self.screen_width // 2 - play_text.get_width() // 2  # Center horizontally
        text_y = self.screen_height // 2 - play_text.get_height() // 2  # Center vertically within the lower third

        # Blit the text surface onto the screen
        self.screen.blit(play_text, (text_x, text_y))
        pg.display.flip()

    def loadGameScreen(self):
        self.current_screen = "game"
        self.screen.fill((0, 255, 255))
        pg.draw.rect(self.screen, (0, 102, 0), (0, self.screen_height*2/3, self.screen_width, self.screen_height // 3))
        self.screen.blit(self.power_bar_image, (-20, self.screen_height - 20) )
        pg.display.flip()
        
    
    
    def runGame(self):
        circle_surface = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
        pg.draw.circle(circle_surface, (255, 255, 255), (self.radius, self.radius), self.radius)


        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_running = False

            # Clear only the area where the circle will be
            rect_to_clear = pg.Rect(self.ball_centre_coord[0] - self.radius, self.ball_centre_coord[1] - self.radius, self.radius * 2, self.radius * 2)
            self.screen.fill((0, 0, 0), rect_to_clear)

            self.loadGameScreen()

            # Blit the pre-rendered circle onto the background
            self.screen.blit(circle_surface, (self.ball_centre_coord[0] - self.radius, self.ball_centre_coord[1] - self.radius))

            # Draw the rectangle
            pg.draw.rect(self.screen, (0, 0, 0), (self.power_line_coord[0], self.power_line_coord[1], 3, 20))

            # Update the display
            pg.display.update()

            # Move the rectangle
            self.power_line_coord[0] += 1

            self.clock.tick(60) 


    def handle_main_screen_events(self):
        for event in pg.event.get():
            mouse_x, mouse_y = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                self.is_running = False

            if self.button_play_coord[0] < mouse_x < self.button_play_coord[0] + self.button_width and self.button_play_coord[1] < mouse_y < self.button_play_coord[1] + self.button_height:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.current_screen = "gameload"
                    pg.mouse.set_cursor(*pg.cursors.arrow)
            else:
                pg.mouse.set_cursor(*pg.cursors.arrow)
            

    def update(self):
        pass


if __name__ == "__main__":
    game = Game()
    game.run()
    pg.quit()
    sys.exit()
