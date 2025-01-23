from Game import Game
import time

screen_width = 1280
screen_height = 720
window_name = "Fluffy Catastrophy - Python Edition"
fps_limit = 60


# todo: think of a way to structure the files

if __name__ == '__main__':
	game = Game()
	game.set_window_name(window_name)\
		.set_fps(fps_limit)\
		.set_screen_size(screen_width, screen_height)

	current_time = time.time()
	timeout = 0.2
	while time.time() - current_time < timeout:
		pass
	game.run_game()

