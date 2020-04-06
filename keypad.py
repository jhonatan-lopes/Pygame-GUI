# Copyright (c) 2020 Jhonatan Da Ponte Lopes
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import pygame
import sys

from pygame.locals import MOUSEBUTTONUP, MOUSEBUTTONDOWN

pygame.init()

class Button():
    """A simple button class"""
    def __init__(self, rect, button_color, function, **kwargs):
        self.process_kwargs(kwargs)
        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface(self.rect.size).convert()
        self.color = button_color
        self.function = function
        self.clicked = False
        self.hovered = False
        self.text = []
        self._render_text(self.font_color)

    def process_kwargs(self, kwargs):
        """Pass optional arguments to object"""
        settings = {"name": None,
                    "text" : None,
                    "font" : pygame.font.Font(None,16),
                    "call_on_release" : True,
                    "hover_color" : None,
                    "clicked_color" : None,
                    "font_color" : pygame.Color("black"),
                    "hover_font_color" : None,
                    "clicked_font_color" : pygame.Color("black")}

        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("Button has no {} keyword".format(kwarg))
        
        self.__dict__.update(settings)

    def _render_text(self, font_color):
        """Renders text object"""
        if self.name:
            self.text = self.font.render(self.name, True, font_color)

    def check_event(self, evnt):
        """Event detection. Needs to be integrated to main's function
         event loop."""
        # Mouse was clicked:
        if evnt.type == MOUSEBUTTONDOWN and evnt.button == 1:
            #self.on_click(event)
            # Check if click was inside button:
            if self.rect.collidepoint(evnt.pos):
                self.clicked = True
        elif evnt.type == MOUSEBUTTONUP and evnt.button == 1:
            #self.on_release(event)
            if self.clicked:
                self.function(self)
                self.clicked = False
    
    def check_hover(self):
        """Checks if the mouse if hovering over the button"""
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                #print('Hovering over {} button!'.format(self.name))
        else:
            self.hovered = False

    def draw(self, surface):
        """Draws the button to the surface. Needs to
        be called every frame in the main loop."""
        # Get current colors:
        color = self.color
        font_color = self.font_color
        self.check_hover()
        # Process click and hover:
        if self.clicked and self.clicked_color:
            color = self.clicked_color
            if self.clicked_font_color:
                font_color = self.clicked_font_color
        elif self.hovered and self.hover_color:
            color = self.hover_color
            if self.hover_font_color:
                font_color = self.hover_font_color
        # Draw button:
        self.image.fill(color)
        surface.blit(self.image, self.rect)
        # Render text:
        self._render_text(font_color)
        # Draw text:
        if self.text:
            text_rect = self.text.get_rect(center=self.rect.center)
            surface.blit(self.text, text_rect)

def button_function(self):
    """Button command when clicked"""

class Keypad():
    """Numerical on-screen keypad with clickable buttons"""
    def __init__(self, rect, **kwargs):
        self._process_kwargs(kwargs)
        self.rect = pygame.Rect(rect)
        self.check_keypad_config()
        self._get_buttons()
        self.value = None
    

    def check_keypad_config(self):
        """Check if keypad configuration is valid"""
        # Get number matrix
        number_matrix = self.keys_configuration
        # Get number of rows
        n_rows = len(number_matrix)
        # Get number of columns in each column
        n_cols_vector = []
        for row in number_matrix:
            current_row_length = len(row)
            if current_row_length not in n_cols_vector:
                n_cols_vector.append(current_row_length)
        # Get the unique numbers of columns
        n_cols = []
        for number in n_cols_vector:
            if number not in n_cols:
                n_cols.append(number)
        # Raise error if rows are of different length
        if len(n_cols) > 1:
            raise AttributeError("Keypad_configuration array attribute should have the same number of elements in each row.")

    def _get_buttons(self):
        """Initialise button objects"""
        # Get numpad configuration:
        number_matrix = self.keys_configuration
        self.n_rows = len(number_matrix)
        self.n_cols = len(number_matrix[1])
        flat_number_matrix = [item for row in number_matrix for item in row]
        self.flat_number_matrix = flat_number_matrix
        buttons = [None for row in number_matrix for item in row]
        # Button settings:
        button_settings =  {"font": self.font,
                            "hover_color": self.hover_color,
                            "clicked_color": self.clicked_color,
                            "font_color": self.font_color,
                            "hover_font_color": self.hover_font_color,
                            "clicked_font_color": self.clicked_font_color}
        # Iterate over numbers:
        for idx, number in enumerate(flat_number_matrix):
            button_rect = self._get_button_rect(number)
            buttons[idx] = Button(button_rect, self.button_color,
                                    button_function, name=str(number),
                                    **button_settings)
        # Pass to keypad:
        self.buttons = buttons


    def _get_number_index(self, number):
        """Find the index of a number on the Numpad's 
        configuration matrix. Internal method."""
        # Get numpad configuration:
        number_matrix = self.keys_configuration
        # Find index of number in numpad:
        for row in number_matrix:
            if number in row:
                j, i = (number_matrix.index(row),row.index(number))
                return i, j
        return None, None

    def _get_button_rect(self, number):
        """Get button object for a given number"""
        # Get number index on numpad:
        i, j = self._get_number_index(number)
        # Numpad widht and height
        left = self.rect[0]
        top = self.rect[1]
        w = self.rect[2]
        h = self.rect[3]
        # Button's rectangle dimensions
        button_w = int((w - 2*self.gap_size)/3)
        button_h = int((h - 2*self.gap_size)/3)
        button_left = int(left + i*(button_w + self.gap_size))
        button_top = int(top + j*(button_w + self.gap_size))
        
        # Return the rectangle object
        return pygame.Rect(button_left, button_top, button_w, button_h)

    
    def _process_kwargs(self, kwargs):
        """Pass optional arguments to object"""
        settings = {"button_color": (250, 250, 250),
                    "gap_size": 2,
                    "name": None,
                    "text" : None,
                    "font" : pygame.font.Font(None,16),
                    "call_on_release" : True,
                    "hover_color" : None,
                    "clicked_color" : None,
                    "font_color" : pygame.Color("black"),
                    "hover_font_color" : None,
                    "clicked_font_color" : pygame.Color("black"),
                    "keys_configuration": [[7,8,9],[4,5,6],[1,2,3]]}

        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("Button has no {} keyword".format(kwarg))
        
        self.__dict__.update(settings)
    
    def check_event(self, event):
        """Checks if event was mousepress into one of the buttons.
        Prints the button value and updates the keypad current value"""
        for button in self.buttons:
            button.check_event(event)
            if button.clicked:
                self.value = int(button.name)
                print('Pressed number {}'.format(self.value))


    def draw(self, surface):
        """Draws the keypad"""
        for button in self.buttons:
            button.draw(surface)
