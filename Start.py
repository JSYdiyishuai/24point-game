import os
import sys
import pygame
from modules import *
from fractions import Fraction


RED = (255, 0, 0)
BLACK = (0, 0, 0)
AZURE = (240, 255, 255)
WHITE = (255, 255, 255)
MISTYROSE = (255, 228, 225)
PALETURQUOISE = (175, 238, 238)
PAPAYAWHIP = (255, 239, 213)
CURRENTPATH = os.path.abspath(os.path.dirname(__file__))
FONTPATH = os.path.join(CURRENTPATH, 'fonts/font.TTF')

NUMBERFONT_COLORS = [BLACK, RED]
NUMBERCARD_COLORS = [MISTYROSE, PALETURQUOISE]
NUMBERFONT = [FONTPATH, 50]
NUMBERCARD_POSITIONS = [(25, 50, 150, 200), (225, 50, 150, 200), (425, 50, 150, 200), (625, 50, 150, 200)]

OPREATORS = ['+', '-', '×', '÷']
OPREATORFONT_COLORS = [BLACK, RED]
OPERATORCARD_COLORS = [MISTYROSE, PALETURQUOISE]
OPERATORFONT = [FONTPATH, 30]
OPERATORCARD_POSITIONS = [(230, 300, 50, 50), (330, 300, 50, 50), (430, 300, 50, 50), (530, 300, 50, 50)]

BUTTONS = ['RESET', 'ANSWERS', 'NEXT']
BUTTONFONT_COLORS = [BLACK, BLACK]
BUTTONCARD_COLORS = [MISTYROSE, PALETURQUOISE]
BUTTONFONT = [FONTPATH, 30]
BUTTONCARD_POSITIONS = [(25, 400, 700/3, 150), (50+700/3, 400, 700/3, 150), (75+1400/3, 400, 700/3, 150)]
SCREENSIZE = (800, 600)
GROUPTYPES = ['NUMBER', 'OPREATOR', 'BUTTON']


def checkClicked(group, mouse_pos, group_type='NUMBER'):
	selected = []
	if group_type == GROUPTYPES[0] or group_type == GROUPTYPES[1]:
		max_selected = 2 if group_type == GROUPTYPES[0] else 1
		num_selected = 0
		for each in group:
			num_selected += int(each.is_selected)
		for each in group:
			if each.rect.collidepoint(mouse_pos):
				if each.is_selected:
					each.is_selected = not each.is_selected
					num_selected -= 1
					each.select_order = None
				else:
					if num_selected < max_selected:
						each.is_selected = not each.is_selected
						num_selected += 1
						each.select_order = str(num_selected)
			if each.is_selected:
				selected.append(each.attribute)
	elif group_type == GROUPTYPES[2]:
		for each in group:
			if each.rect.collidepoint(mouse_pos):
				each.is_selected = True
				selected.append(each.attribute)
	return selected


def getNumberSpritesGroup(numbers):
	number_sprites_group = pygame.sprite.Group()
	for idx, number in enumerate(numbers):
		args = (*NUMBERCARD_POSITIONS[idx], str(number), NUMBERFONT, NUMBERFONT_COLORS, NUMBERCARD_COLORS, str(number))
		number_sprites_group.add(Card(*args))
	return number_sprites_group


def getOperatorSpritesGroup(operators):
	operator_sprites_group = pygame.sprite.Group()
	for idx, operator in enumerate(operators):
		args = (*OPERATORCARD_POSITIONS[idx], str(operator), OPERATORFONT, OPREATORFONT_COLORS, OPERATORCARD_COLORS, str(operator))
		operator_sprites_group.add(Card(*args))
	return operator_sprites_group


def getButtonSpritesGroup(buttons):
	button_sprites_group = pygame.sprite.Group()
	for idx, button in enumerate(buttons):
		args = (*BUTTONCARD_POSITIONS[idx], str(button), BUTTONFONT, BUTTONFONT_COLORS, BUTTONCARD_COLORS, str(button))
		button_sprites_group.add(Button(*args))
	return button_sprites_group


def calculate(number1, number2, operator):
	operator_map = {'+': '+', '-': '-', '×': '*', '÷': '/'}
	try:
		result = str(eval(number1+operator_map[operator]+number2))
		return result if '.' not in result else str(Fraction(number1+operator_map[operator]+number2))
	except:
		return None


def showInfo(text, screen):
	rect = pygame.Rect(200, 180, 400, 200)
	pygame.draw.rect(screen, PAPAYAWHIP, rect)
	font = pygame.font.Font(FONTPATH, 40)
	text_render = font.render(text, True, BLACK)
	font_size = font.size(text)
	screen.blit(text_render, (rect.x+(rect.width-font_size[0])/2,
							  rect.y+(rect.height-font_size[1])/2))


def main():
	pygame.init()
	screen = pygame.display.set_mode(SCREENSIZE)
	pygame.display.set_caption('24 point')

	game24_gen = game24Generator()
	game24_gen.generate()

	number_sprites_group = getNumberSpritesGroup(game24_gen.numbers_now)
	operator_sprites_group = getOperatorSpritesGroup(OPREATORS)
	button_sprites_group = getButtonSpritesGroup(BUTTONS)

	clock = pygame.time.Clock()
	selected_numbers = []
	selected_operators = []
	selected_buttons = []
	is_win = False
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(-1)
			elif event.type == pygame.MOUSEBUTTONUP:
				mouse_pos = pygame.mouse.get_pos()
				selected_numbers = checkClicked(number_sprites_group, mouse_pos, 'NUMBER')
				selected_operators = checkClicked(operator_sprites_group, mouse_pos, 'OPREATOR')
				selected_buttons = checkClicked(button_sprites_group, mouse_pos, 'BUTTON')
		screen.fill(AZURE)
		if len(selected_numbers) == 2 and len(selected_operators) == 1:
			noselected_numbers = []
			for each in number_sprites_group:
				if each.is_selected:
					if each.select_order == '1':
						selected_number1 = each.attribute
					elif each.select_order == '2':
						selected_number2 = each.attribute
					else:
						pass
				else:
					noselected_numbers.append(each.attribute)
				each.is_selected = False
			for each in operator_sprites_group:
				each.is_selected = False
			result = calculate(selected_number1, selected_number2, *selected_operators)
			if result is not None:
				game24_gen.numbers_now = noselected_numbers + [result]
				is_win = game24_gen.check()
			else:
				pass
			selected_numbers = []
			selected_operators = []
			number_sprites_group = getNumberSpritesGroup(game24_gen.numbers_now)

		for each in number_sprites_group:
			each.draw(screen, pygame.mouse.get_pos())
		for each in operator_sprites_group:
			each.draw(screen, pygame.mouse.get_pos())
		for each in button_sprites_group:
			if selected_buttons and selected_buttons[0] in ['RESET', 'NEXT']:
				is_win = False
			if selected_buttons and each.attribute == selected_buttons[0]:
				each.is_selected = False
				number_sprites_group = each.do(game24_gen, getNumberSpritesGroup, number_sprites_group, button_sprites_group)
				selected_buttons = []
			each.draw(screen, pygame.mouse.get_pos())

		if is_win:
			showInfo('Congratulations', screen)
		if not is_win and len(game24_gen.numbers_now) == 1:
			showInfo('Game Over', screen)
		pygame.display.flip()
		clock.tick(30)


if __name__ == '__main__':
	main()
