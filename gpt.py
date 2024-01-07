"""Projekt WDI IQ puzzle - Wojciech Mierzejek 459435"""
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Vertical Split")
font = pygame.font.Font(None, 36)

def draw_vertical_line():
    # Draw a vertical line in the middle of the screen
    pygame.draw.line(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height), 3)

def display_text():
    # Render text for each side
    text_left = font.render("Left Side", True, white)
    text_right = font.render("Right Side", True, white)

    # Position the text
    text_left_rect = text_left.get_rect(center=(screen_width // 4, 50))
    text_right_rect = text_right.get_rect(center=(3 * screen_width // 4, 50))

    # Display the text on the screen
    screen.blit(text_left, text_left_rect)
    screen.blit(text_right, text_right_rect)

def display_images():
    # Load images
    image_left = pygame.image.load('left_image.png')
    image_right = pygame.image.load('right_image.png')

    # Resize images if needed
    image_left = pygame.transform.scale(image_left, (200, 200))
    image_right = pygame.transform.scale(image_right, (200, 200))

    # Position images
    image_left_rect = image_left.get_rect(center=(screen_width // 4, 150))
    image_right_rect = image_right.get_rect(center=(3 * screen_width // 4, 150))

    # Display images on the screen
    screen.blit(image_left, image_left_rect)
        screen.blit(image_right, image_right_rect)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill(black)
    
    # Draw the vertical line
    draw_vertical_line()

    # Display text on each side
    display_text()
    

    # Update the display
    pygame.display.update()

# Quit Pygame properly
pygame.quit()
sys.exit()
