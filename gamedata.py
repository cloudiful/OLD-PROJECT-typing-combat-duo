import pygame

# monitor width and height
WIDTH, HEIGHT = 1600, 800

FPS = 60

# score multiplier
SCORE_MUL = WIDTH // 100

score_me = 0
score_opponent = 0
# count for combo
combo = 0

image_x, image_y = -WIDTH, HEIGHT // 4

IMAGE1raw = pygame.image.load('Assets/rope.png')
IMAGE1 = pygame.transform.scale(IMAGE1raw, (WIDTH * 2, HEIGHT // 2))

# string list for text file
TXT = []
FONTSIZE = 25

# header when TCP communicating, contains the length of message
HEADER = 64

# my index in server (for example: me - 0 opponent - 1)
net_index = 0

# received message from server
net_content = '!'

# how many client has connected to the server
client_count = 0