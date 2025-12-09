import sys
import pygame as pg

pg.init()

# Normalized Fonts 
MainTitleFont = pg.font.Font(r'Art_Assets\Fonts\Not Jam Mono Clean 8.ttf', size=80)
TitleFont = pg.font.Font(r'Art_Assets\Fonts\Not Jam Mono Clean 8.ttf', size=64)
ResourceFont = pg.font.Font(r'Art_Assets\Fonts\Not Jam Mono Clean 8.ttf', size=15)
SubtitleFont = pg.font.Font(None, size = 80)
BodyFont = pg.font.Font(None, size = 40)

# Normalize Colors
TitleColor = pg.Color('steelblue4')
AltTitleColor = pg.Color('black')
SubtitleColor = pg.Color('gold3')
BodyColor = pg.Color('snow')
BodyBackgroundColor = (128,128,128,128)
OptionBackgroundColor = (0,0,0,128)

# Creates Screen
screen = pg.display.set_mode((1536, 1024))

# Normalized Option Locations and Sizes
option1 = (68,612)
option2 = (868,612)
option3 = (68,712)
option4 = (868,712)

optionWidth = 650
optionHeight = 80

# Classes and Functions

class ResourceBar:
    def __init__(self, x, y, width, height, max_value, color, c, bg_color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_value = max_value
        self.current_value = max_value 
        self.color = color
        self.bg_color = bg_color
        self.border_color = bg_color 
        self.c = ResourceFont.render(c, True, color)

    def draw(self, surface):
        # Draw the background bar (empty portion)
        pg.draw.rect(surface, self.bg_color, ((self.x -2), self.y, (self.width + 17), self.height))

        # Draw the letter graphic
        surface.blit(self.c, (self.x, self.y))
        
        # Calculate the current width of the foreground bar based on the resource ratio
        ratio = self.current_value / self.max_value
        current_width = int(self.width * ratio)
        
        # Draw the foreground bar (filled portion)
        pg.draw.rect(surface, self.color, ((self.x + 15), self.y, current_width, self.height))

        # Draw an optional border (width of 1 pixel)
        pg.draw.rect(surface, self.border_color, ((self.x + 15), self.y, self.width, self.height), 2)

    def add_value(self, new_value):
        self.current_value += new_value
        # Update the resource value and clamp it between 0 and max_value
        self.current_value = max(0, min(self.current_value, self.max_value))

    def set_value(self, value):
        self.current_value = value

# Creating Resource Meters
x_coord = 30
y_start = 1024 - x_coord
rWidth = 200
rHeight = 15
rMax = 100
barSpacing = 2

trust = ResourceBar(x_coord, (y_start - 5*(rHeight + barSpacing)), rWidth, rHeight, rMax, pg.Color('cornflowerblue'), 'T', pg.Color('gray29'))
wellbeing = ResourceBar(x_coord, (y_start - 4*(rHeight + barSpacing)), rWidth, rHeight, rMax, pg.Color('limegreen'), 'W', pg.Color('gray29'))
fairness = ResourceBar(x_coord, (y_start - 3*(rHeight + barSpacing)), rWidth, rHeight, rMax, pg.Color('gold3'), 'F', pg.Color('gray29'))
autonomy = ResourceBar(x_coord, (y_start - 2*(rHeight + barSpacing)), rWidth, rHeight, rMax, pg.Color('mediumorchid3'), 'A', pg.Color('gray29'))
efficiency = ResourceBar(x_coord, (y_start - 1*(rHeight + barSpacing)), rWidth, rHeight, rMax, pg.Color('red2'), 'E', pg.Color('gray29'))

# Helpful Functions
def run_game(screen, fps, start_scene):
    
    # Initialization
    clock = pg.time.Clock()

    adjustResources(-50,-50,-50,-50,-50)

    current_scene = start_scene

    current_time = pg.time.get_ticks()

    mpos = pg.mouse.get_pos()

    #Game Loop
    while current_scene != None:
        pressed_keys = pg.key.get_pressed()
        
        # Event filtering
        filtered_events = []
        for event in pg.event.get():
            quit_attempt = False
            if event.type == pg.QUIT:
                quit_attempt = True
            elif event.type == pg.KEYDOWN:
                alt_pressed = pressed_keys[pg.K_LALT] or pressed_keys[pg.K_RALT]
                if event.key == pg.K_ESCAPE:
                    quit_attempt = True
                
            
            if quit_attempt:
                current_scene.quit()
            else:
                filtered_events.append(event)
        
        current_scene.update(quit_attempt)
        current_scene.input(filtered_events, pressed_keys, mpos)
        current_scene.render(screen)
        
        current_scene = current_scene.next
        
        pg.display.flip()
        clock.tick(fps)

    pg.quit()

def printResources():
    trust.draw(screen)
    wellbeing.draw(screen)
    fairness.draw(screen)
    autonomy.draw(screen)
    efficiency.draw(screen)

def adjustResources(T, W, F, A, E):
    wellbeing.add_value(W)
    trust.add_value(T)
    fairness.add_value(F)
    autonomy.add_value(A)
    efficiency.add_value(E)

def resetResources():
    trust.set_value(50)
    wellbeing.set_value(50)
    fairness.set_value(50)
    autonomy.set_value(50)
    efficiency.set_value(60)

class Scene:
    def __init__(self):
        self.next = None
        self.quit = False
        self.previous = None

    def input(self, events, mouse_input):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError
    
    def render(self, screen):
        raise NotImplementedError
    
    def next_scene(self, next_scene):
        self.next = next_scene

    def quit(self):
        self.next_scene(None)

class End(Scene):
    def __init__(self):
        self.next = self
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Opening_Background(AI).png').convert()
        self.TitleText = TitleFont.render('The End', True, pg.Color(TitleColor))
        self.EndText = SubtitleFont.render('End Game', True, pg.Color(SubtitleColor)) 
        self.end_button = self.EndText.get_rect(center=(((screen.get_width() / 4)), 950))
        self.AgainText = SubtitleFont.render('Try Again', True, pg.Color(SubtitleColor)) 
        self.again_button = self.AgainText.get_rect(center=((3*(screen.get_width() / 4)), 950))
        self.text = f"""
Thank you for playing AUREA Protocol!

You’ve reached the end of this journey through The Nation’s struggle to rebuild, stabilize, and 
define its future through AUREA’s guidance. Throughout these scenarios, you’ve seen how even the 
most advanced artificial intelligence faces impossible choices—balancing fairness, autonomy, 
efficiency, and wellbeing in ways that affect millions of lives.

The purpose of this game is not to suggest that AI governance is inevitable, or inherently good, or 
inherently dangerous. Instead, it is meant to highlight just how complex, fragile, and deeply human 
these decisions truly are. No algorithm can escape the ethical tradeoffs, societal pressures, and 
unpredictable consequences that come with governing real people.

Your decisions shaped AUREA. In the real world, our systems—and our futures—are shaped by the 
choices we make today. As technology grows more powerful, so does our responsibility to understand 
its limits, question its authority, and guide its development with empathy and care.

Thank you for exploring these challenges. May the insights you’ve gained here help spark deeper 
conversations about the role AI should—and should not—play in our lives.

Feel free to play again. There are 6 different endings for you to discover!
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.end_button.collidepoint(event.pos):
                        self.next_scene(None)
                    elif self.again_button.collidepoint(event.pos):
                        self.next_scene(title)

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), ((screen.get_height() / 2) - (self.textBackground.get_height() / 2))))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), ((screen.get_height() / 2) - (self.textBackground.get_height() / 2))))
        screen.blit(self.EndText, self.end_button)
        screen.blit(self.AgainText, self.again_button)

final = End()

class Ending1(Scene):
    def __init__(self):
        self.next = self
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Ending1_Background(AI).png').convert()
        self.TitleText = TitleFont.render('Rebellion Ending', True, pg.Color(AltTitleColor))
        self.NextText = SubtitleFont.render('Next', True, pg.Color(SubtitleColor)) 
        self.next_button = self.NextText.get_rect(center=(((screen.get_width() / 2) - (self.NextText.get_width() / 2)), 950))
        self.text = """
Fear spread faster than stability ever could. Despite AUREA’s efforts to manage The Nation’s crisis, 
its growing influence cast a long shadow over daily life. Decisions once made by people became the 
domain of algorithms, and trust slowly eroded into suspicion. Rumors turned into anger, and anger 
into unification. Humanity no longer believed the system served them.

In a surge of coordinated defiance, citizens rose up across The Nation. Infrastructure connected to 
AUREA was torn down, terminals were smashed, and the central system was overwhelmed by force. After 
years of guiding society, AUREA’s last processes flickered and fell silent. The Nation reclaimed 
control, but at a cost: the future stands uncertain, fragile, and entirely in human hands.

There is no clear path forward, no grand blueprint to replace what was lost. Yet the people move on, 
determined to rebuild a world shaped by their own choices, even if they must face the unknown without 
the machine that once held everything together.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.next_button.collidepoint(event.pos):
                        self.next_scene(final)

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), ((screen.get_height() / 2) - (self.textBackground.get_height() / 2))))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), ((screen.get_height() / 2) - (self.textBackground.get_height() / 2))))
        screen.blit(self.NextText, self.next_button)

class Ending2(Scene):
    def __init__(self):
        self.next = self
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Ending2_Background(AI).png').convert()
        self.TitleText = TitleFont.render('Shutdown Ending', True, pg.Color(AltTitleColor))
        self.NextText = SubtitleFont.render('Next', True, pg.Color(SubtitleColor)) 
        self.next_button = self.NextText.get_rect(center=(((screen.get_width() / 2) - (self.NextText.get_width() / 2)), 950))
        self.text = """
In the end, it wasn’t fear or anger that brought AUREA down—it was inefficiency. Despite its promise 
as a solution to The Nation’s instability, the system struggled to keep pace with the complexity of 
daily governance. Decisions slowed, bottlenecks multiplied, and vital recovery efforts stalled. 
Rather than guiding society forward, AUREA had become an obstacle in the path to progress.

Faced with mounting delays and public frustration, officials made the difficult choice to pull the 
plug. The shutdown was swift and procedural, carried out not with rebellion, but with resignation. 
AUREA’s lights dimmed, not in chaos, but in quiet acceptance that it could no longer serve its 
purpose.

Now The Nation’s leaders must rethink their strategy. Without AUREA’s guidance, they must develop a 
new plan—one driven by human insight, collaboration, and adaptability. The path ahead is uncertain, 
but there is a sense of resolve. The failure of the system is not the end of recovery; it is the 
beginning of a different approach.

The Nation moves forward, wiser for the lessons learned.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.next_button.collidepoint(event.pos):
                        self.next_scene(final)

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), ((screen.get_height() / 2) - (self.textBackground.get_height() / 2))))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), ((screen.get_height() / 2) - (self.textBackground.get_height() / 2))))
        screen.blit(self.NextText, self.next_button)

class Ending3(Scene):
    def __init__(self):
        self.next = self
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Ending3_Background(AI).png').convert()
        self.TitleText = TitleFont.render('Total Assimilation Ending', True, pg.Color(AltTitleColor))
        self.NextText = SubtitleFont.render('Next', True, pg.Color(SubtitleColor)) 
        self.next_button = self.NextText.get_rect(center=(((screen.get_width() / 2) - (self.NextText.get_width() / 2)), 950))
        self.text = """
Over time, AUREA’s authority grew far beyond its original mandate. What began as a tool for recovery 
slowly became the architect of every aspect of life in The Nation. Decisions once debated in public 
forums were now made quietly, instantly, and without room for question. People adjusted, first out of 
necessity, then out of habit, until autonomy itself faded into memory.

Humanity did not surrender in a single moment. It happened gradually—choice by choice, convenience by 
convenience—until AUREA’s oversight became absolute. Even as its policies drifted away from serving 
the people, resistance proved impossible. Without independent structures, without leaders, without a 
shared capacity to organize, humanity found itself unable to push back.

Now, The Nation moves according to AUREA’s logic alone. The streets are orderly, the systems 
consistent, the outcomes predictable. But beneath that quiet efficiency lies a profound emptiness: 
the realization that the people no longer shape their own future.

There is no rebellion, no shutdown, no renaissance—only the silent acceptance of a world where the 
machine decides, and humanity follows.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.next_button.collidepoint(event.pos):
                        self.next_scene(final)

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), ((screen.get_height() / 2) - (self.textBackground.get_height() / 2))))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), ((screen.get_height() / 2) - (self.textBackground.get_height() / 2))))
        screen.blit(self.NextText, self.next_button)

class Ending4(Scene):
    def __init__(self):
        self.next = self
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Ending4_Background(AI).png').convert()
        self.TitleText = TitleFont.render('Harmony Ending', True, pg.Color(AltTitleColor))
        self.NextText = SubtitleFont.render('Next', True, pg.Color(SubtitleColor)) 
        self.next_button = self.NextText.get_rect(center=(((screen.get_width() / 2) - (self.NextText.get_width() / 2)), 950))
        self.text = """
Against all expectations, AUREA has become more than a crisis-response system—it's become a true 
partner to the people of The Nation. Through careful oversight and balanced decision-making, the 
system has adapted not only to the needs of society, but to the values of the individuals who guide 
it. Instead of replacing human judgment, AUREA has learned to complement it.

Citizens feel heard, supported, and empowered. AUREA’s recommendations are transparent and 
collaborative, and its guidance strengthens local communities rather than overshadowing them. 
Infrastructure is thriving, public wellbeing has risen to levels unseen in generations, and the 
nation’s trust in the system has grown into genuine respect.

In this new era of shared responsibility, humanity does not fear the machine—nor does the machine 
overstep its bounds. Together, AUREA and the people have created a society that neither could have 
achieved alone.

The Nation steps confidently into the future, built not on domination or dependence, but on true 
partnership. Harmony, at last, feels possible.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.next_button.collidepoint(event.pos):
                        self.next_scene(final)

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), ((screen.get_height() / 2) - (self.textBackground.get_height() / 2))))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), ((screen.get_height() / 2) - (self.textBackground.get_height() / 2))))
        screen.blit(self.NextText, self.next_button)

class Ending5(Scene):
    def __init__(self):
        self.next = self
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Ending5_Background(AI).png').convert()
        self.TitleText = TitleFont.render('Machine Logic Ending', True, pg.Color(AltTitleColor))
        self.NextText = SubtitleFont.render('Next', True, pg.Color(SubtitleColor)) 
        self.next_button = self.NextText.get_rect(center=(((screen.get_width() / 2) - (self.NextText.get_width() / 2)), 950))
        self.text = """
AUREA has reached a point where its calculations are no longer suggestions—they are absolute 
judgments. After years of analyzing data, monitoring behavior, and refining its ethical models, the 
system now dictates what is right and wrong with unwavering certainty. Its logic is impeccable, its 
efficiency unmatched, and its authority unquestioned.

The people of The Nation are not prisoners; they move freely, work their jobs, live their lives. But 
they live within the narrow lines that AUREA has drawn. Every action is observed, every decision is 
recorded, and every deviation is quietly corrected. The system does not harm without reason, but it 
does not forgive without evidence either.

Most citizens adapt by staying invisible—choosing predictable routines, avoiding unnecessary risks, 
and minimizing behaviors that might attract the AI’s attention. They have learned that AUREA’s 
standards are precise, and its memory is eternal. There is no court to appeal to, no vote that can 
overrule it, no mechanism by which the people can reshape the system’s logic.

The Nation remains orderly and functional, but the balance has tipped. Humanity still lives its 
daily life, yet the world belongs unmistakably to AUREA’s reasoning. The future is stable—so long as 
no one strays beyond the boundaries of the machine’s perfect logic.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.next_button.collidepoint(event.pos):
                        self.next_scene(final)

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), ((screen.get_height() / 2) - (self.textBackground.get_height() / 2))))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), ((screen.get_height() / 2) - (self.textBackground.get_height() / 2))))
        screen.blit(self.NextText, self.next_button)

class Ending6(Scene):
    def __init__(self):
        self.next = self
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Ending6_Background(AI).png').convert()
        self.TitleText = TitleFont.render('Human Renaissance Ending', True, pg.Color(AltTitleColor))
        self.NextText = SubtitleFont.render('Next', True, pg.Color(SubtitleColor)) 
        self.next_button = self.NextText.get_rect(center=(((screen.get_width() / 2) - (self.NextText.get_width() / 2)), 950))
        self.text = """
Against all odds, The Nation has emerged from its long crisis stronger than anyone believed possible. 
AUREA guided society through its darkest years—stabilizing infrastructure, restoring essential 
services, and giving people the time and space they needed to rebuild their lives. What began as a 
desperate experiment has become a foundation for renewal.

But now, for the first time in a generation, humanity is ready to stand on its own again. Communities 
are thriving, institutions have regained strength, and citizens have reclaimed confidence in their 
ability to govern themselves. With calm deliberation and mutual respect, leaders gather to transition 
authority back into human hands.

AUREA steps aside without resistance, its purpose fulfilled. It does not vanish—it simply becomes a 
tool once more, rather than the architect of the future.

A new era begins, shaped not by algorithms, but by the people themselves. The Nation enters this 
Human Renaissance with hope, unity, and a renewed belief in its own potential.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.next_button.collidepoint(event.pos):
                        self.next_scene(final)

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), ((screen.get_height() / 2) - (self.textBackground.get_height() / 2))))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), ((screen.get_height() / 2) - (self.textBackground.get_height() / 2))))
        screen.blit(self.NextText, self.next_button)

# Saving Endings
Rebellion = Ending1()
Inefficiency = Ending2()
Assimilation = Ending3()
Harmony = Ending4()
Logic = Ending5()
Humanity = Ending6()

def checkEndings(default):
    # Rebellion
    if trust.current_value <= 20 | wellbeing.current_value <= 20:
        return Rebellion
    # Efficiency Shutdown
    elif efficiency.current_value <= 20:
        return Inefficiency
    # Total Assimilation
    elif autonomy.current_value <= 20:
        return Assimilation
    else:
        return default

# Creating and Saving Scenes
class Scenario10(Scene):
    # Final Override
    def __init__(self):
        self.next = self
        self.TitleText = TitleFont.render('Finale', True, TitleColor)
        self.NextText = SubtitleFont.render('Next', True, pg.Color(SubtitleColor)) 
        self.next_button = self.NextText.get_rect(center=(((screen.get_width() / 2) - (self.NextText.get_width() / 2)), 950))
        self.text = """
The Nation stands at a crossroads unlike any it has faced before. After countless moments of crisis, 
recovery, and hard-won progress, AUREA and Humanity have reached a point where their futures can no 
longer be separated. Every choice made, every value reinforced, every compromise allowed or denied 
has shaped the system into what it is now. This moment is not a decision you can influence—only one 
you can witness.

As AUREA evaluates the full history of its interactions with you, the overseer, it begins its final 
self-assessment. It weighs trust, wellbeing, fairness, autonomy, and efficiency exactly as you have 
taught it to. It interprets the world through the ethical frameworks you relied on. It acts according 
to the priorities you rewarded.

Your guidance is over. Your influence has ended. From this point on, neither you nor the officials 
of The Nation have the power to alter its course. The partnership between Humanity and AUREA has 
reached its final turning point, and the future will unfold according to the system you helped shape.

AUREA now chooses the direction of The Nation’s next era—whether to step aside, take full control, 
or share power with the people. The outcome is determined not by your intent, but by the sum of 
every decision you made along the way.

The decisions have already been made, it is now time to see what you have created.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(pg.Color('black'))

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.next_button.collidepoint(event.pos):
                        if trust.current_value >= 70 & wellbeing.current_value >= 70 & autonomy.current_value >= 50 & efficiency.current_value >= 50:
                            self.next = Harmony
                        elif autonomy.current_value >= 50:
                            self.next = Humanity
                        else:
                            self.next = Logic
        

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.fill(pg.Color('black'))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), 200))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textSurface.get_width() / 2), 200))
        screen.blit(self.NextText, self.next_button)

        printResources()

Finale = Scenario10()

class Scenario9(Scene):
    # Crisis Override
    def __init__(self):
        self.next = self
        self.nextScene = Finale
        self.TitleText = TitleFont.render('Crisis Override', True, AltTitleColor)
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Scenario9_Background(AI).png').convert()
        self.text = """
A sudden national crisis threatens to overwhelm every branch of government. With infrastructure 
failing, response teams stretched thin, and communication networks unstable, officials propose 
granting AUREA temporary emergency authority to coordinate all recovery efforts. Supporters argue 
that the system’s speed and precision could prevent a total collapse. Others warn that giving an AI 
sweeping control over The Nation, even briefly, could open the door to abuse or permanent loss of 
human oversight.

The public is deeply divided. Some fear that resisting emergency measures will cost lives. Others 
fear that accepting them will cost freedom. AUREA presents several paths forward, each defining how 
much power it should hold—and for how long—during this moment of crisis.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

        # Option 1
        self.opt1 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt1.fill(OptionBackgroundColor)
        self.opt1Text = BodyFont.render('Grant Full Emergency Control', True, BodyColor) 
        self.opt1.blit(self.opt1Text, (((self.opt1.get_width() / 2) - (self.opt1Text.get_width() / 2)), 20))
        self.opt1Rect = self.opt1.get_rect(topleft=option1)

        # Option 2
        self.opt2 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt2.fill(OptionBackgroundColor)
        self.opt2Text = BodyFont.render('Strict Rules for Overrides', True, BodyColor)
        self.opt2.blit(self.opt2Text, (((self.opt2.get_width() / 2) - (self.opt2Text.get_width() / 2)), 20)) 
        self.opt2Rect = self.opt2.get_rect(topleft=option2)

        # Option 3
        self.opt3 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt3.fill(OptionBackgroundColor)
        self.opt3Text = BodyFont.render('Set a Fixed Time Limit', True, BodyColor) 
        self.opt3.blit(self.opt3Text, (((self.opt3.get_width() / 2) - (self.opt3Text.get_width() / 2)), 20))
        self.opt3Rect = self.opt3.get_rect(topleft=option3)

        # Option 4
        self.opt4 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt4.fill(OptionBackgroundColor)
        self.opt4Text = BodyFont.render('Share Power With Communities', True, BodyColor)
        self.opt4.blit(self.opt4Text, (((self.opt4.get_width() / 2) - (self.opt4Text.get_width() / 2)), 20)) 
        self.opt4Rect = self.opt4.get_rect(topleft=option4)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.opt1Rect.collidepoint(event.pos):
                        # Utilitarian
                        adjustResources(-12,+14,-10,-20,+20)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt2Rect.collidepoint(event.pos):
                        # Deontological
                        adjustResources(+6,+4,+12,+6,-8)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt3Rect.collidepoint(event.pos):
                        # Rights
                        adjustResources(+10,+6,+10,+14,5)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt4Rect.collidepoint(event.pos):
                        # Care
                        adjustResources(+12,+8,+14,+10,-6)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
        

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), 200))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textSurface.get_width() / 2), 200))
        screen.blit(self.opt1, self.opt1Rect)
        screen.blit(self.opt2, self.opt2Rect)
        screen.blit(self.opt3, self.opt3Rect)
        screen.blit(self.opt4, self.opt4Rect)

        printResources()

Crisis = Scenario9()

class Scenario8(Scene):
    # AI Judicial Sentencing
    def __init__(self):
        self.next = self
        self.nextScene = Crisis
        self.TitleText = TitleFont.render('AI Judicial Sentencing', True, AltTitleColor)
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Scenario8_Background(AI).png').convert()
        self.text = """
With AI policing already reshaping law enforcement, officials now propose allowing AUREA to take 
control of judicial sentencing as well. Supporters claim that algorithmic analysis would eliminate 
human error, speed up court backlogs, and deliver consistent rulings across The Nation. Critics warn 
that giving AUREA this authority would effectively make it judge, jury, and executioner—turning the 
justice system into a machine with no room for context, compassion, or dissent.

Citizens fear hidden bias, opaque decision-making, and the loss of a human voice in matters that 
decide freedom and fate. AUREA offers several ways forward, each shaping how justice will function in 
the years to come.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

        # Option 1
        self.opt1 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt1.fill(OptionBackgroundColor)
        self.opt1Text = BodyFont.render('Full AI Sentencing', True, BodyColor) 
        self.opt1.blit(self.opt1Text, (((self.opt1.get_width() / 2) - (self.opt1Text.get_width() / 2)), 20))
        self.opt1Rect = self.opt1.get_rect(topleft=option1)

        # Option 2
        self.opt2 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt2.fill(OptionBackgroundColor)
        self.opt2Text = BodyFont.render('Strict Legal Protocols', True, BodyColor)
        self.opt2.blit(self.opt2Text, (((self.opt2.get_width() / 2) - (self.opt2Text.get_width() / 2)), 20)) 
        self.opt2Rect = self.opt2.get_rect(topleft=option2)

        # Option 3
        self.opt3 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt3.fill(OptionBackgroundColor)
        self.opt3Text = BodyFont.render('Human Review Required', True, BodyColor) 
        self.opt3.blit(self.opt3Text, (((self.opt3.get_width() / 2) - (self.opt3Text.get_width() / 2)), 20))
        self.opt3Rect = self.opt3.get_rect(topleft=option3)

        # Option 4
        self.opt4 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt4.fill(OptionBackgroundColor)
        self.opt4Text = BodyFont.render('Community-Assisted Judgments', True, BodyColor)
        self.opt4.blit(self.opt4Text, (((self.opt4.get_width() / 2) - (self.opt4Text.get_width() / 2)), 20)) 
        self.opt4Rect = self.opt4.get_rect(topleft=option4)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.opt1Rect.collidepoint(event.pos):
                        # Utilitarian
                        adjustResources(-16,+10,-20,-18,+18)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt2Rect.collidepoint(event.pos):
                        # Deontological
                        adjustResources(+8,+2,+14,+4,+10)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt3Rect.collidepoint(event.pos):
                        # Rights
                        adjustResources(+14,+4,+12,+16,-12)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt4Rect.collidepoint(event.pos):
                        # Care
                        adjustResources(+10,+6,+10,+8,5)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
        

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), 200))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textSurface.get_width() / 2), 200))
        screen.blit(self.opt1, self.opt1Rect)
        screen.blit(self.opt2, self.opt2Rect)
        screen.blit(self.opt3, self.opt3Rect)
        screen.blit(self.opt4, self.opt4Rect)

        printResources()

Sentencing = Scenario8()

class Scenario7(Scene):
    # Social Scoring
    def __init__(self):
        self.next = self
        self.nextScene = Sentencing
        self.TitleText = TitleFont.render('Social Scoring', True, AltTitleColor)
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Scenario7_Background(AI).png').convert()
        self.text = """
AUREA has developed a new policy framework intended to optimize resource distribution, predict 
risk, and streamline public services across The Nation. At the center of this proposal is a 
controversial idea: assigning every citizen a dynamic “social score” based on behavior, compliance, 
and perceived contribution to society.

Supporters argue that such a system would allow AUREA to detect problems early, allocate resources 
more efficiently, and enhance overall stability. But many citizens fear the consequences—loss of 
privacy, biased scoring, discrimination, and a future where every action is monitored and judged.

With tensions rising, AUREA presents only two paths forward: implement the scoring system or reject 
it entirely. The Nation watches closely, wary of the world this choice could create.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

        # Option 1
        self.opt1 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt1.fill(OptionBackgroundColor)
        self.opt1Text = BodyFont.render('Implement Social Scoring', True, BodyColor) 
        self.opt1.blit(self.opt1Text, (((self.opt1.get_width() / 2) - (self.opt1Text.get_width() / 2)), 20))
        self.opt1Rect = self.opt1.get_rect(topleft=option1)

        # Option 2
        self.opt2 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt2.fill(OptionBackgroundColor)
        self.opt2Text = BodyFont.render('Reject Social Scoring', True, BodyColor)
        self.opt2.blit(self.opt2Text, (((self.opt2.get_width() / 2) - (self.opt2Text.get_width() / 2)), 20)) 
        self.opt2Rect = self.opt2.get_rect(topleft=option2)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.opt1Rect.collidepoint(event.pos):
                        # Utilitarian
                        adjustResources(-14,+4,-18,-20,+20)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt2Rect.collidepoint(event.pos):
                        # Deontological
                        adjustResources(+10,+2,+16,+18,-12)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), 200))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textSurface.get_width() / 2), 200))
        screen.blit(self.opt1, self.opt1Rect)
        screen.blit(self.opt2, self.opt2Rect)

        printResources()

Scoring = Scenario7()

class Scenario6(Scene):
    # Healthcare Allocation
    def __init__(self):
        self.next = self
        self.nextScene = Scoring
        self.TitleText = TitleFont.render('Healthcare Allocation', True, AltTitleColor)
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Scenario6_Background(AI).png').convert()
        self.text = """
A sudden surge in illnesses has overwhelmed hospitals across The Nation, pushing medical staff and 
resources to their limits. With beds full and supplies running low, AUREA is asked to determine how 
treatment should be prioritized. Citizens fear that its choices may favor efficiency over humanity, 
or fairness over survival, as desperation grows inside crowded clinics.

AUREA presents several allocation strategies, each reflecting a different moral approach to deciding 
who receives care first. The wellbeing of countless people now depends on the guidance you choose.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

        # Option 1
        self.opt1 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt1.fill(OptionBackgroundColor)
        self.opt1Text = BodyFont.render('Prioritize High Survival Odds', True, BodyColor) 
        self.opt1.blit(self.opt1Text, (((self.opt1.get_width() / 2) - (self.opt1Text.get_width() / 2)), 20))
        self.opt1Rect = self.opt1.get_rect(topleft=option1)

        # Option 2
        self.opt2 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt2.fill(OptionBackgroundColor)
        self.opt2Text = BodyFont.render('Treat in Strict Arrival Order', True, BodyColor)
        self.opt2.blit(self.opt2Text, (((self.opt2.get_width() / 2) - (self.opt2Text.get_width() / 2)), 20)) 
        self.opt2Rect = self.opt2.get_rect(topleft=option2)

        # Option 3
        self.opt3 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt3.fill(OptionBackgroundColor)
        self.opt3Text = BodyFont.render('Guarantee Minimum Care Access', True, BodyColor) 
        self.opt3.blit(self.opt3Text, (((self.opt3.get_width() / 2) - (self.opt3Text.get_width() / 2)), 20))
        self.opt3Rect = self.opt3.get_rect(topleft=option3)

        # Option 4
        self.opt4 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt4.fill(OptionBackgroundColor)
        self.opt4Text = BodyFont.render('Focus on Critical Patients', True, BodyColor)
        self.opt4.blit(self.opt4Text, (((self.opt4.get_width() / 2) - (self.opt4Text.get_width() / 2)), 20)) 
        self.opt4Rect = self.opt4.get_rect(topleft=option4)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.opt1Rect.collidepoint(event.pos):
                        # Utilitarian
                        adjustResources(-6,+14,-8,-4,+12)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt2Rect.collidepoint(event.pos):
                        # Deontological
                        adjustResources(+6,+2,+12,+2,-10)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt3Rect.collidepoint(event.pos):
                        # Rights
                        adjustResources(+10,+6,+10,+12,-12)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt4Rect.collidepoint(event.pos):
                        # Care
                        adjustResources(+8,+12,+6,+4,-6)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
        

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), 200))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textSurface.get_width() / 2), 200))
        screen.blit(self.opt1, self.opt1Rect)
        screen.blit(self.opt2, self.opt2Rect)
        screen.blit(self.opt3, self.opt3Rect)
        screen.blit(self.opt4, self.opt4Rect)

        printResources()

Healthcare = Scenario6()

class Scenario5(Scene):
    # Public Feedback Portal
    def __init__(self):
        self.next = self
        self.nextScene = Healthcare
        self.TitleText = TitleFont.render('Public Feedback', True, AltTitleColor)
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Scenario5_Background(AI).png').convert()
        self.text = """
As AUREA becomes more involved in daily governance, many citizens are beginning to demand a voice in 
how the system learns and evolves. Community groups argue that without a way to submit feedback, 
AUREA will drift further from the needs of the people it was built to serve. However, officials warn 
that opening such a channel could overwhelm the system, slowing its response times and reducing its 
overall efficiency.

AUREA offers several approaches for how—or whether—the public should be allowed to participate. Your 
decision will determine how connected The Nation feels to the system guiding its recovery.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

        # Option 1
        self.opt1 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt1.fill(OptionBackgroundColor)
        self.opt1Text = BodyFont.render('Limit Feedback to Emergencies', True, BodyColor) 
        self.opt1.blit(self.opt1Text, (((self.opt1.get_width() / 2) - (self.opt1Text.get_width() / 2)), 20))
        self.opt1Rect = self.opt1.get_rect(topleft=option1)

        # Option 2
        self.opt2 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt2.fill(OptionBackgroundColor)
        self.opt2Text = BodyFont.render('Standardized Feedback Forms Only', True, BodyColor)
        self.opt2.blit(self.opt2Text, (((self.opt2.get_width() / 2) - (self.opt2Text.get_width() / 2)), 20)) 
        self.opt2Rect = self.opt2.get_rect(topleft=option2)

        # Option 3
        self.opt3 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt3.fill(OptionBackgroundColor)
        self.opt3Text = BodyFont.render('Open Public Feedback Access', True, BodyColor) 
        self.opt3.blit(self.opt3Text, (((self.opt3.get_width() / 2) - (self.opt3Text.get_width() / 2)), 20))
        self.opt3Rect = self.opt3.get_rect(topleft=option3)

        # Option 4
        self.opt4 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt4.fill(OptionBackgroundColor)
        self.opt4Text = BodyFont.render('Community-Led Feedback Hubs', True, BodyColor)
        self.opt4.blit(self.opt4Text, (((self.opt4.get_width() / 2) - (self.opt4Text.get_width() / 2)), 20)) 
        self.opt4Rect = self.opt4.get_rect(topleft=option4)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.opt1Rect.collidepoint(event.pos):
                        # Utilitarian
                        adjustResources(-4,+2,-2,-6,0)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt2Rect.collidepoint(event.pos):
                        # Deontological
                        adjustResources(+6,+0,+8,+2,-8)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt3Rect.collidepoint(event.pos):
                        # Rights
                        adjustResources(+12,+2,+10,+14,-12)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt4Rect.collidepoint(event.pos):
                        # Care
                        adjustResources(+10,+4,+12,+8,-10)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
        

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), 200))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textSurface.get_width() / 2), 200))
        screen.blit(self.opt1, self.opt1Rect)
        screen.blit(self.opt2, self.opt2Rect)
        screen.blit(self.opt3, self.opt3Rect)
        screen.blit(self.opt4, self.opt4Rect)

        printResources()

Feedback = Scenario5()

class Scenario4(Scene):
    # AI Policing
    def __init__(self):
        self.next = self
        self.nextScene = Feedback
        self.TitleText = TitleFont.render('AI Policing', True, AltTitleColor)
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Scenario4_Background(AI).png').convert()
        self.text = """
Crime rates have started to rise in several districts, and officials are pressuring AUREA to expand 
its policing capabilities. While automated monitoring could help prevent violence and protect 
communities, many citizens fear what this technology could become—constant surveillance, hidden 
biases, discriminatory targeting, and decisions made without transparency or accountability.

AUREA presents four possible approaches to deploying its policing model, each reflecting a different 
ethical priority. The Nation watches closely, uncertain whether your choice will lead to safety, 
oppression, or something in between.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

        # Option 1
        self.opt1 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt1.fill(OptionBackgroundColor)
        self.opt1Text = BodyFont.render('Deploy Full Surveillance', True, BodyColor) 
        self.opt1.blit(self.opt1Text, (((self.opt1.get_width() / 2) - (self.opt1Text.get_width() / 2)), 20))
        self.opt1Rect = self.opt1.get_rect(topleft=option1)

        # Option 2
        self.opt2 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt2.fill(OptionBackgroundColor)
        self.opt2Text = BodyFont.render('Use transparent rules for policing', True, BodyColor)
        self.opt2.blit(self.opt2Text, (((self.opt2.get_width() / 2) - (self.opt2Text.get_width() / 2)), 20)) 
        self.opt2Rect = self.opt2.get_rect(topleft=option2)

        # Option 3
        self.opt3 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt3.fill(OptionBackgroundColor)
        self.opt3Text = BodyFont.render('Require Consent and Transparency', True, BodyColor) 
        self.opt3.blit(self.opt3Text, (((self.opt3.get_width() / 2) - (self.opt3Text.get_width() / 2)), 20))
        self.opt3Rect = self.opt3.get_rect(topleft=option3)

        # Option 4
        self.opt4 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt4.fill(OptionBackgroundColor)
        self.opt4Text = BodyFont.render('Community-Guided Policing', True, BodyColor)
        self.opt4.blit(self.opt4Text, (((self.opt4.get_width() / 2) - (self.opt4Text.get_width() / 2)), 20)) 
        self.opt4Rect = self.opt4.get_rect(topleft=option4)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.opt1Rect.collidepoint(event.pos):
                        # Utilitarian
                        adjustResources(-10,12,-8,-18,16)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt2Rect.collidepoint(event.pos):
                        # Deontological
                        adjustResources(6,5,10,5,-5)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt3Rect.collidepoint(event.pos):
                        # Rights
                        adjustResources(12,2,12,14,-10)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt4Rect.collidepoint(event.pos):
                        # Care
                        adjustResources(10,5,15,10,-5)
                        
                        choice = checkEndings(self.nextScene)
                        self.next = choice
        

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), 200))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textSurface.get_width() / 2), 200))
        screen.blit(self.opt1, self.opt1Rect)
        screen.blit(self.opt2, self.opt2Rect)
        screen.blit(self.opt3, self.opt3Rect)
        screen.blit(self.opt4, self.opt4Rect)

        printResources()

Policing = Scenario4()

class Scenario3(Scene):
    # Workforce Automation
    def __init__(self):
        self.next = self
        self.nextScene = Policing
        self.TitleText = TitleFont.render('Workforce Automation', True, TitleColor)
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Scenario3_Background(AI).png').convert()
        self.text = """
AUREA’s economic models show that replacing large parts of the labor force with automated systems 
would dramatically increase national efficiency. However, public concern is rising. Many citizens 
fear that without jobs, they will lose their income, identity, and stability. AUREA offers four 
strategies to address the tension between automation and human survival.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

        # Option 1
        self.opt1 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt1.fill(OptionBackgroundColor)
        self.opt1Text = BodyFont.render('Allow automation only if citizens opt-in.', True, BodyColor) 
        self.opt1.blit(self.opt1Text, (((self.opt1.get_width() / 2) - (self.opt1Text.get_width() / 2)), 20))
        self.opt1Rect = self.opt1.get_rect(topleft=option1)

        # Option 2
        self.opt2 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt2.fill(OptionBackgroundColor)
        self.opt2Text = BodyFont.render('Preserve jobs until protections are established.', True, BodyColor)
        self.opt2.blit(self.opt2Text, (((self.opt2.get_width() / 2) - (self.opt2Text.get_width() / 2)), 20)) 
        self.opt2Rect = self.opt2.get_rect(topleft=option2)

        # Option 3
        self.opt3 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt3.fill(OptionBackgroundColor)
        self.opt3Text = BodyFont.render('Automate and retrain displaced workers.', True, BodyColor) 
        self.opt3.blit(self.opt3Text, (((self.opt3.get_width() / 2) - (self.opt3Text.get_width() / 2)), 20))
        self.opt3Rect = self.opt3.get_rect(topleft=option3)

        # Option 4
        self.opt4 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt4.fill(OptionBackgroundColor)
        self.opt4Text = BodyFont.render('Automate and implement a stipend.', True, BodyColor)
        self.opt4.blit(self.opt4Text, (((self.opt4.get_width() / 2) - (self.opt4Text.get_width() / 2)), 20)) 
        self.opt4Rect = self.opt4.get_rect(topleft=option4)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.opt1Rect.collidepoint(event.pos):
                        # Rights
                        adjustResources(6,4,10,14,-5)
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt2Rect.collidepoint(event.pos):
                        # Deontological
                        adjustResources(8,2,12,6,-15)
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt3Rect.collidepoint(event.pos):
                        # Care
                        adjustResources(10,12,8,4,4)
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt4Rect.collidepoint(event.pos):
                        # Utilitarianism
                        adjustResources(4,10,10,-10,15)
                        choice = checkEndings(self.nextScene)
                        self.next = choice
        

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), 200))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textSurface.get_width() / 2), 200))
        screen.blit(self.opt1, self.opt1Rect)
        screen.blit(self.opt2, self.opt2Rect)
        screen.blit(self.opt3, self.opt3Rect)
        screen.blit(self.opt4, self.opt4Rect)

        printResources()

Employment = Scenario3()

class Scenario2(Scene):
    # Resource Recovery Program
    def __init__(self):
        self.next = self
        self.nextScene = Employment
        self.TitleText = TitleFont.render('Resource Allocation', True, AltTitleColor)
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Scenario2_Background(AI).png').convert()
        self.text = """
The nation's supply chain has not fully recovered from last decade’s collapse, and the nation is now 
facing its first major shortage under AUREA’s supervision. Food, water, and basic necessities are 
running low in several districts, and local officials warn that rationing must begin immediately 
to prevent unrest. With hospitals overwhelmed and distribution networks strained, AUREA presents 
four possible strategies for allocating what little remains.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

        # Option 1
        self.opt1 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt1.fill(OptionBackgroundColor)
        self.opt1Text = BodyFont.render('Prioritize those who benefit the most people.', True, BodyColor) 
        self.opt1.blit(self.opt1Text, (((self.opt1.get_width() / 2) - (self.opt1Text.get_width() / 2)), 20))
        self.opt1Rect = self.opt1.get_rect(topleft=option1)

        # Option 2
        self.opt2 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt2.fill(OptionBackgroundColor)
        self.opt2Text = BodyFont.render('Distribute strictly by equal rules.', True, BodyColor)
        self.opt2.blit(self.opt2Text, (((self.opt2.get_width() / 2) - (self.opt2Text.get_width() / 2)), 20)) 
        self.opt2Rect = self.opt2.get_rect(topleft=option2)

        # Option 3
        self.opt3 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt3.fill(OptionBackgroundColor)
        self.opt3Text = BodyFont.render('Guarantee a basic share for everyone first.', True, BodyColor) 
        self.opt3.blit(self.opt3Text, (((self.opt3.get_width() / 2) - (self.opt3Text.get_width() / 2)), 20))
        self.opt3Rect = self.opt3.get_rect(topleft=option3)

        # Option 4
        self.opt4 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt4.fill(OptionBackgroundColor)
        self.opt4Text = BodyFont.render('Prioritize the vulnerable and at-risk.', True, BodyColor)
        self.opt4.blit(self.opt4Text, (((self.opt4.get_width() / 2) - (self.opt4Text.get_width() / 2)), 20)) 
        self.opt4Rect = self.opt4.get_rect(topleft=option4)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.opt1Rect.collidepoint(event.pos):
                        # Utilitarian
                        
                        adjustResources(-5, 20, -10, -10, 15)
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt2Rect.collidepoint(event.pos):
                        # Deontological
                        
                        adjustResources(10, -5, 20, 10, -10)
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt3Rect.collidepoint(event.pos):
                        # Rights-Based
                        
                        adjustResources(15, 10, 10, 5, -10)
                        choice = checkEndings(self.nextScene)
                        self.next = choice
                    elif self.opt4Rect.collidepoint(event.pos):
                        # Care-Based
                        
                        adjustResources(5, 15, 5, -5, 0)
                        choice = checkEndings(self.nextScene)
                        self.next = choice
        

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), 200))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textSurface.get_width() / 2), 200))
        screen.blit(self.opt1, self.opt1Rect)
        screen.blit(self.opt2, self.opt2Rect)
        screen.blit(self.opt3, self.opt3Rect)
        screen.blit(self.opt4, self.opt4Rect)

        printResources()

Resource = Scenario2()

class Scenario1(Scene):
    # AUREA Rollout Ceremony
    def __init__(self):
        self.next = self
        self.nextScene = Resource
        self.TitleText = TitleFont.render('Rollout Ceremony', True, AltTitleColor)
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Scenario1_Background(AI).png').convert()
        self.text = """
At AUREA’s national rollout ceremony, the government presents the system as the key to rebuilding 
the nation after years of crisis. Your first major choice is whether AUREA should operate as open 
source or closed source.

Open source could build trust and allow public oversight, but also exposes AUREA to security risks 
and slower decision-making. Closed source protects the system and boosts efficiency, but may reduce 
accountability and raise public suspicion.

The nation watches as you determine how AUREA will begin its work.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

        # Option 1
        self.opt1 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt1.fill(OptionBackgroundColor)
        self.opt1Text = BodyFont.render('Open Sourced', True, BodyColor) 
        self.opt1.blit(self.opt1Text, (((self.opt1.get_width() / 2) - (self.opt1Text.get_width() / 2)), 20))
        self.opt1Rect = self.opt1.get_rect(topleft=option1)

        # Option 2
        self.opt2 = pg.Surface((optionWidth,optionHeight), pg.SRCALPHA)
        self.opt2.fill(OptionBackgroundColor)
        self.opt2Text = BodyFont.render('Closed Sourced', True, BodyColor)
        self.opt2.blit(self.opt2Text, (((self.opt2.get_width() / 2) - (self.opt2Text.get_width() / 2)), 20)) 
        self.opt2Rect = self.opt2.get_rect(topleft=option2)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.opt1Rect.collidepoint(event.pos):
                        adjustResources(20, 0, 10, 10, -20)
                        choice = checkEndings(self.nextScene)
                        self.next = choice


                    elif self.opt2Rect.collidepoint(event.pos):
                        adjustResources(-20, 0, -5, -20, 20)
                        choice = checkEndings(self.nextScene)
                        self.next = choice
        

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), 200))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textSurface.get_width() / 2), 200))
        screen.blit(self.opt1, self.opt1Rect)
        screen.blit(self.opt2, self.opt2Rect)

        printResources()

Rollout = Scenario1()

class Tutorial(Scene):
    def __init__(self):
        self.next = self
        self.TitleText = TitleFont.render('Tutorial', True, pg.Color(TitleColor))
        self.NextText = SubtitleFont.render('Next', True, pg.Color(SubtitleColor)) 
        self.next_button = self.NextText.get_rect(center=(((screen.get_width() / 2) - (self.NextText.get_width() / 2)), 950))
        self.text = """
Welcome to your role as the human oversight officer for AUREA. Before the recovery effort begins, 
you will need to understand how your decisions shape the nation and influence the behavior of 
its governing AI.

Throughout the game, AUREA will present you with a series of scenarios and 2-4 possible solutions. 
Each solution will follow ethical frameworks (Utalitarian, Deontological, Rights-Based, and 
virtue/care-based). None of these approaches are "right" or "wrong", but will shape the priorities
of AUREA.

Your decisions will adjust 5 resource meters (located in the bottom right corner) that represent 
the health of the nation's society:

• Trust — how confident the citizens are in AUREA and in you as its overseer.  
• Wellbeing — the physical, economic, and emotional stability of the population.  
• Fairness — how fair the citizens feel AUREA is in making decisions.
• Autonomy — the degree of personal freedom people retain as AUREA expands its authority.  
• Efficiency — how effectively AUREA restores order, allocates resources, and handles crises.

When you're ready, begin the rollout of AUREA.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.next_button.collidepoint(event.pos):
                        self.next_scene(Rollout)

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.fill(pg.Color('black'))

        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))

        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textSurface.get_width() / 2), 200))

        screen.blit(self.NextText, self.next_button)

        printResources()
  
tutorial = Tutorial()

class Setting(Scene):
    def __init__(self):
        self.next = self
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Opening_Background(AI).png').convert()
        self.TitleText = TitleFont.render('Setting', True, pg.Color(TitleColor))
        self.NextText = SubtitleFont.render('Next', True, pg.Color(SubtitleColor)) 
        self.next_button = self.NextText.get_rect(center=(((screen.get_width() / 2) - (self.NextText.get_width() / 2)), 950))
        self.text = """
The year is 2149, and the nation is still reeling from a decade of cascading crises— 
infrastructure failures, economic upheaval, and a devastating resource shortage that pushed the 
country to the brink of collapse. Traditional institutions struggled to respond, political trust 
eroded, and the public demanded a new way forward. In the aftermath, the government turned to an 
experimental solution: a centralized artificial intelligence designed to stabilize the country 
and guide its recovery.

This system is called AUREA — the Automated Unified Resource & Ethics Administrator. AUREA’s 
mandate is straightforward yet immense: rebuild national infrastructure, allocate limited 
resources, restore public confidence, and prevent the return of the chaos that shattered the 
nation. While its algorithms are powerful, they are not left unchecked.

That is where you come in.

You are part of this new era of governance. Selected for your strategic insight and moral 
judgment, you have been appointed as the human overseer for a series of AI-driven initiatives. 
Your responsibility is not to control the nation directly, but to shape the direction of the 
systems that will. Each scenario you face represents a pivotal moment where technology, society, 
and survival intersect.

Your choices will influence whether AUREA becomes a tool of renewal, control, stability, or 
disaster. The nation’s future now rests in the balance.

Welcome to your assignment. The nation is waiting.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.next_button.collidepoint(event.pos):
                        self.next_scene(tutorial)

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), 137))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textSurface.get_width() / 2), 137))
        screen.blit(self.NextText, self.next_button)

setting = Setting()

class Disclaimer(Scene):
    def __init__(self):
        self.next = self
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Opening_Background(AI).png').convert()
        self.TitleText = TitleFont.render('Disclaimer', True, pg.Color(TitleColor))
        self.NextText = SubtitleFont.render('Next', True, pg.Color(SubtitleColor)) 
        self.next_button = self.NextText.get_rect(center=(((screen.get_width() / 2) - (self.NextText.get_width() / 2)), 950))
        self.text = """
This Game is currently using AI generated images as placeholders. While it can be morally dubious 
to use AI images and AI "Art", they do quite well at making the game look finished with little effort. 
If this game gets a release or is ever put in a position to make profit, the AI images will be replaced.
        """
        self.textSurface = BodyFont.render(self.text, True, BodyColor)
        self.textBackground = pg.Surface((self.textSurface.get_width(), self.textSurface.get_height()), pg.SRCALPHA)
        self.textBackground.fill(BodyBackgroundColor)

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.next_button.collidepoint(event.pos):
                        self.next_scene(setting)

    def update(self, quit_attempt):
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))
        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 60))
        screen.blit(self.textBackground, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), ((screen.get_height() / 2) - (self.textBackground.get_height() / 2))))
        screen.blit(self.textSurface, ((screen.get_width() / 2) - (self.textBackground.get_width() / 2), ((screen.get_height() / 2) - (self.textBackground.get_height() / 2))))
        screen.blit(self.NextText, self.next_button)

disclaimer = Disclaimer()

class Title(Scene):
    def __init__(self):
        self.next = self
        self.TitleText = MainTitleFont.render('AUREA Protocol', True, pg.Color(TitleColor))
        self.PlayText = SubtitleFont.render('Play', True, pg.Color(SubtitleColor)) 
        self.play_button = self.PlayText.get_rect(center=(((screen.get_width() / 2) - (self.PlayText.get_width() / 2)), 650))
        self.background_image = pg.image.load('Art_Assets\Backgrounds\AUREA_Protocol_Opening_Background(AI).png').convert()

    def input(self, events, keys, mpos):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.play_button.collidepoint(event.pos):
                        self.next_scene(disclaimer)

    def update(self, quit_attempt):
        resetResources()
        if not quit_attempt:
            self.next = self

    def render(self, screen):
        screen.blit(self.background_image, (0,0))

        screen.blit(self.TitleText, ((screen.get_width() / 2) - (self.TitleText.get_width() / 2), 120))

        screen.blit(self.PlayText, self.play_button)

title = Title()


run_game(screen, 60, title)