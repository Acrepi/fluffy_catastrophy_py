import os
import pygame


class Game:
	def __init__(self):
		pygame.init()
		self._screen_width = 0
		self._screen_height = 0
		self._game_screen = None
		self._window_name = ""
		self._icon = ""
		self._is_game_running = False
		self._game_clock = 0
		self._fps_limit = 60

	def set_screen_size(self, width, height):
		self._screen_width = width
		self._screen_height = height
		self._game_screen = pygame.display.set_mode((width, height))
		return self

	def get_screen_size(self):
		return { "x": self._screen_width, "y": self._screen_height }

	def set_window_name(self, name):
		self._window_name = name
		pygame.display.set_caption(name)
		return self

	def get_window_name(self):
		return self._window_name

	def set_window_icon(self, file):
		if file != "":
			self._icon = file
			icon = pygame.image.load(file)
			pygame.display.set_icon(icon)
		return self

	def set_fps(self, fps):
		self._fps_limit = fps
		return self

	def get_fps(self):
		return self._fps_limit

	def run_game(self):
		self._is_game_running = True
		self._game_clock = pygame.time.Clock()
		dt = 0

		# CAT MOVEMENT
		cat_sprite_sheet = {
			"run": [
				pygame.image.load('assets\\graphics\\cat_run_3.png'),
				pygame.image.load('assets\\graphics\\cat_run_2.png'),
				pygame.image.load('assets\\graphics\\cat_run_1.png'),
				pygame.image.load('assets\\graphics\\cat_run_2.png')
			],
			"jump": [
				pygame.image.load('assets\\graphics\\cat_jump_1.png'),
				pygame.image.load('assets\\graphics\\cat_jump_2.png')
			],
			"double_jump": [
				pygame.image.load('assets\\graphics\\cat_double_jump_1.png'),
				pygame.image.load('assets\\graphics\\cat_double_jump_2.png'),
				pygame.image.load('assets\\graphics\\cat_double_jump_3.png'),
				pygame.image.load('assets\\graphics\\cat_double_jump_4.png')
			]
		}

		obstacle_sprite_sheet = {
			"stand": [
				pygame.image.load('assets\\graphics\\obstacle_1_stand_1.png')
			],
			"break": [
				pygame.image.load('assets\\graphics\\obstacle_1_break_1.png'),
				pygame.image.load('assets\\graphics\\obstacle_1_break_2.png'),
				pygame.image.load('assets\\graphics\\obstacle_1_break_3.png')
			],
			"broken": [
				pygame.image.load('assets\\graphics\\obstacle_1_broken_1.png')
			]
		}

		# CREATE OBJECTS
		lives = 3
		points = 0
		speed_up_timer = 0
		speed_up_value = 1

		my_font = pygame.font.SysFont('Comic Sans MS', 32)


		obstacle = Obstacle()
		obstacle.set_size(100, 100) \
			.set_sprite_sheet(obstacle_sprite_sheet) \
			.set_start_position(self._screen_width, 500) \
			.set_pull_strength(-400) \
			.reset_obstacle()

		obstacle2 = Obstacle()
		obstacle2.set_size(100, 100) \
			.set_sprite_sheet(obstacle_sprite_sheet) \
			.set_start_position(self._screen_width, 500) \
			.set_pull_strength(-400) \
			.set_position(self._screen_width + 120, 500)

		cat = Player()
		cat.set_size(100, 100) \
			.set_sprite_sheet(cat_sprite_sheet) \
			.set_position(50, 10) \
			.set_gravity(18) \
			.set_jump_force(11) \
			.set_max_jumps(2)

		while self._is_game_running:
			# HANDLE EVENTS HERE
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self._is_game_running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						cat.jump()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						cat.jump()


			# RENDER GAME OBJECTS HERE
			self._game_screen.fill("black")
			text_points = my_font.render("Points: " + str(points), False, (255, 255, 255))
			text_lives = my_font.render("Lives:  " + str(lives), False, (255, 255, 255))
			self._game_screen.blit(text_points, (10, 0))
			self._game_screen.blit(text_lives, (10, 37))
			obstacle.draw_object(self._game_screen, dt)
			obstacle2.draw_object(self._game_screen, dt)
			cat.draw_object(self._game_screen, dt)

			if obstacle.get_position()["x"] + obstacle.get_size()["x"] < 0:
				obstacle.reset_obstacle()
			if obstacle2.get_position()["x"] + obstacle2.get_size()["x"] < 0:
				obstacle2.reset_obstacle()
			if obstacle.check_collision(cat):
				if obstacle.destroy_obstacle():
					lives -= 1
					if lives == 0:
						print("GAME OVER")
						self.exit_game()
			if obstacle2.check_collision(cat):
				if obstacle2.destroy_obstacle():
					lives -= 1
					if lives == 0:
						print("GAME OVER")
						self.exit_game()


			# UPDATE SCREEN
			pygame.display.flip()
			dt = self._game_clock.tick(self._fps_limit) / 1000

			points = points + round(dt * 1000)

			speed_up_timer += dt
			if speed_up_timer >= 1:
				speed_up_timer = 0
				obstacle.set_pull_strength(obstacle.get_pull_strength() - speed_up_value)
				obstacle2.set_pull_strength(obstacle2.get_pull_strength() - speed_up_value)

	def exit_game(self):
		self._is_game_running = False


class GameObject:
	def __init__(self):
		self._size_x = 0
		self._size_y = 0
		self._position_x = 0
		self._position_y = 0

	def set_size(self, width, height):
		self._size_x = width
		self._size_y = height
		return self

	def get_size(self):
		return { "x": self._size_x, "y": self._size_y }

	def set_position(self, position_x, position_y):
		self._position_x = position_x
		self._position_y = position_y
		return self

	def get_position(self):
		return { "x": self._position_x, "y": self._position_y }

	def draw_hitbox(self, game_screen, color):
		pygame.draw.rect(game_screen, color, [self._position_x, self._position_y, self._size_x, self._size_y])

	def check_collision(self, game_object):
		obj_pos = game_object.get_position()
		obj_size = game_object.get_size()
		if self._position_x + self._size_x > obj_pos["x"] and self._position_x < obj_pos["x"] + obj_size["x"]:
			if self._position_y + self._size_y > obj_pos["y"] and self._position_y < obj_pos["y"] + obj_size["y"]:
				return True
		return False


class Obstacle(GameObject):
	def __init__(self):
		super().__init__()
		self._start_position_x = 0
		self._start_position_y = 0
		self._sprite_sheet = {}
		self._is_visible = True
		self._is_destroyed = False
		self._speed_x = 0
		self._speed_y = 0
		self._animation_name = "stand"
		self._animation_frame = 0
		self._animation_counter = 0
		self._pull_strength = 0

	def set_start_position(self, start_position_x, start_position_y):
		self._start_position_x = start_position_x
		self._start_position_y = start_position_y
		return self

	def set_size(self, width, height):
		self._size_x = width
		self._size_y = height
		self._resize_sprite_sheet()
		return self

	def set_pull_strength(self, pull_strength):
		self._pull_strength = pull_strength
		return self

	def _resize_sprite_sheet(self):
		keys = list(self._sprite_sheet.keys())
		if len(keys) > 0:
			for i in range(0, len(keys)):
				elem = len(self._sprite_sheet[keys[i]])
				for j in range(0, elem):
					self._sprite_sheet[keys[i]][j] = pygame.transform.scale(self._sprite_sheet[keys[i]][j], (self._size_x, self._size_y))

	def set_sprite_sheet(self, sprite_sheet):
		self._sprite_sheet = sprite_sheet
		self._resize_sprite_sheet()
		return self

	def set_speed(self, speed_x, speed_y):
		self._speed_x = speed_x
		self._speed_y = speed_y
		return self

	def _animate(self, delta_time):
		if self._animation_name == "break":
			self._animation_counter += delta_time
			if self._animation_counter >= 0.05:
				self._animation_frame += 1
				self._animation_counter = 0
				if self._animation_frame == len(self._sprite_sheet["break"]):
					self._change_animation("broken")

	def _change_animation(self, animation_name):
		if animation_name == "stand" and self._animation_name != "stand":
			self._animation_name = "stand"
			self._animation_frame = 0
			self._animation_counter = 0
		elif animation_name == "break" and self._animation_name != "break":
			self._animation_name = "break"
			self._animation_frame = 0
			self._animation_counter = 0
		elif animation_name == "broken" and self._animation_name != "broken":
			self._animation_name = "broken"
			self._animation_frame = 0
			self._animation_counter = 0

	def draw_object(self, game_screen, delta_time):
		self._position_x += self._pull_strength * delta_time
		self._animate(delta_time)
		game_screen.blit(self._sprite_sheet[self._animation_name][self._animation_frame], (self._position_x, self._position_y))

	def check_collision(self, game_object):
		obj_pos = game_object.get_position()
		obj_size = game_object.get_size()
		if self._position_x + self._size_x > obj_pos["x"] and self._position_x < obj_pos["x"] + obj_size["x"]:
			if self._position_y + self._size_y > obj_pos["y"] and self._position_y < obj_pos["y"] + obj_size["y"]:
				return True
		return False

	def destroy_obstacle(self):
		if not self._is_destroyed:
			self._is_destroyed = True
			self._change_animation("break")
			return True
		return False

	def fix_obstacle(self):
		if self._is_destroyed:
			self._is_destroyed = False
			self._change_animation("stand")
			return True
		return False

	def reset_obstacle(self):
		self._position_x = self._start_position_x
		self._position_y = self._start_position_y
		self._speed_x = 0
		self._speed_y = 0
		self.fix_obstacle()

	def get_pull_strength(self):
		return self._pull_strength


class Player(GameObject):
	def __init__(self):
		super().__init__()
		self._sprite_sheet = {}
		self._is_visible = True
		self._gravity_value = 0
		self._speed_x = 0
		self._speed_y = 0
		self._jump_force = 0
		self._max_jumps = 0
		self._current_jump = 0
		self._animation_name = "run"
		self._animation_frame = 0
		self._animation_counter = 0

	def set_size(self, width, height):
		self._size_x = width
		self._size_y = height
		self._resize_sprite_sheet()
		return self

	def _resize_sprite_sheet(self):
		keys = list(self._sprite_sheet.keys())
		if len(keys) > 0:
			for i in range(0, len(keys)):
				elem = len(self._sprite_sheet[keys[i]])
				for j in range(0, elem):
					self._sprite_sheet[keys[i]][j] = pygame.transform.scale(self._sprite_sheet[keys[i]][j], (self._size_x, self._size_y))

	def set_sprite_sheet(self, sprite_sheet):
		self._sprite_sheet = sprite_sheet
		self._resize_sprite_sheet()
		return self

	def set_gravity(self, gravity_value):
		self._gravity_value = gravity_value
		return self

	def set_speed(self, speed_x, speed_y):
		self._speed_x = speed_x
		self._speed_y = speed_y
		return self

	def set_jump_force(self, jump_force):
		self._jump_force = jump_force
		return self

	def set_max_jumps(self, max_jumps):
		self._max_jumps = max_jumps
		return self

	def _animate(self, delta_time):
		self._animation_counter += delta_time
		if self._animation_name == "run":
			if self._animation_counter >= 0.2:
				self._animation_frame += 1
				self._animation_counter = 0
				if self._animation_frame == len(self._sprite_sheet["run"]):
					self._animation_frame = 0
		elif self._animation_name == "jump":
			if self._speed_y <= 0:
				self._animation_frame = 0
			else:
				self._animation_frame = 1
		elif self._animation_name == "double_jump":
			if self._animation_counter >= 0.1:
				self._animation_frame += 1
				self._animation_counter = 0
				if self._animation_frame == len(self._sprite_sheet["double_jump"]):
					self._animation_frame = 0

	def _change_animation(self, animation_name):
		if animation_name == "run" and self._animation_name != "run":
			self._animation_name = "run"
			self._animation_frame = 0
			self._animation_counter = 0
		elif animation_name == "jump" and self._animation_name != "jump":
			self._animation_name = "jump"
			self._animation_frame = 0
			self._animation_counter = 0
		elif animation_name == "double_jump" and self._animation_name != "double_jump":
			self._animation_name = "double_jump"
			self._animation_frame = 0
			self._animation_counter = 0

	def draw_object(self, game_screen, delta_time):
		floor = 600
		if self._position_y + self._size_x < floor - self._speed_y or self._speed_y < 0:
			self._speed_y += self._gravity_value * delta_time
			self._position_y += self._speed_y
		else:
			self._change_animation("run")
			self._current_jump = 0
			self._position_y = floor - self._size_x
			self._speed_y = 0

		self._animate(delta_time)
		game_screen.blit(self._sprite_sheet[self._animation_name][self._animation_frame], (self._position_x, self._position_y))

	def jump(self):
		if self._current_jump < self._max_jumps:
			self._current_jump += 1
			self._speed_y = -self._jump_force

		if self._current_jump == 1:
			self._change_animation("jump")
		elif self._current_jump == 2:
			self._change_animation("double_jump")
