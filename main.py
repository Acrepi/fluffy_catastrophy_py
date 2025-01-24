from Game import Game
import time


# todo: think of a way to structure the files

if __name__ == '__main__':
	game = Game()
	game.set_window_name("Fluffy Catastrophy - Python Edition")\
		.set_fps(60)\
		.set_screen_size(1280, 720)

	current_time = time.time()
	timeout = 0.2
	while time.time() - current_time < timeout:
		pass
	game.run_game()
