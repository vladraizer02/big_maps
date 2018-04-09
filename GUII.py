import pygame
 
pygame.init()
size = width, height = 350, 500
screen = pygame.display.set_mode(size)
 
class GUI:
    def __init__(self):
        self.elements = []
        
        
    def add_element(self, element):
        self.elements.append(element)
        
        
    def render(self, surface):
        for element in self.elements:
            render = getattr(element, 'render', None)
            if callable(render):
                element.render(surface)
    
    
    def update(self):
        for element in self.elements:
            update = getattr(element, 'update', None)
            if callable(update):
                element.update()     
                
                
    
    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, 'get_event', None)
            if callable(get_event):
                element.get_event(event)         
 
 
class Label:
    def __init__(self, rect, text):
        self.Rect = pygame.Rect(rect)
        self.text = text
        self.bgcolor = pygame.Color('white')
        self.font_color = pygame.Color('purple')
        self.font = pygame.font.SysFont('arial', self.Rect.height - 4)
        self.rendered_text = None
        self.rendered_rect = None
        
        
    def render(self, surface):
        surface.fill(self.bgcolor, self.Rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.Rect.x + 2, centery=self.Rect.centery)
        surface.blit(self.rendered_text, self.rendered_rect)
 
class Button(Label):
    def __init__(self, rect, text):
        super().__init__(rect, text)
        self.bgcolor = pygame.Color('blue')
        self.pressed = False
        
        
    def render(self, surface):
        surface.fill(self.bgcolor, self.Rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        if not self.pressed:
            color1, color2 = pygame.Color('white'), pygame.Color('black')
            self.rendered_rect = self.rendered_text.get_rect(x=self.Rect.x + 5, centery=self.Rect.centery)
        else:
            color1, color2 = pygame.Color('black'), pygame.Color('white')
            self.rendered_rect = self.rendered_text.get_rect(x=self.Rect.x + 7, centery=self.Rect.centery + 2)
            
        # границы кнопки
        pygame.draw.rect(surface,color1, self.Rect, 2)
        pygame.draw.line(surface, color2, (self.Rect.right - 1, self.Rect.top),(self.Rect.right - 1, self.Rect.bottom), 2)
        pygame.draw.line(surface, color2, (self.Rect.left, self.Rect.bottom),(self.Rect.right, self.Rect.bottom-1), 2)
        surface.blit(self.rendered_text, self.rendered_rect)
        
        
        
    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.Rect.collidepoint(event.pos)
            print(0)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False
 
class TextBox(Label):
    def __init__(self, rect, text):
        super().__init__(rect, text)
        self.focus = True
        self.blink = True
        self.blink_timer = 0
        
        
    def get_event(self, event):
        if event.type == pygame.KEYDOWN and self.focus:
            if event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                self.execute()
            elif event.key ==  pygame.K_BACKSPACE:
                if len(self.text) > 0:
                    self.text = self.text[:-1]
            else:
                self.text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.focus = self.Rect.collidepoint(event.pos)
            
            
            
    def update(self):
        if pygame.time.get_ticks() - self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()
    
    
    def render(self, surface):
        super(TextBox, self).render(surface)
        if self.focus and self.blink:
            pygame.draw.line(surface, pygame.Color('black'), (self.rendered_rect.right + 2, self.rendered_rect.top+2), (self.rendered_rect.right + 2, self.rendered_rect.bottom - 2))
 