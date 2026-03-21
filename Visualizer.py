import pygame
import random

pygame.init()

# -------- SETTINGS --------
WIDTH = 1000
HEIGHT = 600
TOP_MARGIN = 120
N = 100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Visualizer")

clock = pygame.time.Clock()

delay = 60
ascending = True
sorted_done = False
algorithm = "quick"
sorting = False

# -------- DATA --------
def generate_data():
    step = (HEIGHT - TOP_MARGIN - 20) // N
    arr = [20 + i * step for i in range(N)]
    random.shuffle(arr)
    return arr

data = generate_data()

gap = 1
bar_width = (WIDTH - (N * gap)) // N

# -------- COLORS --------
def get_color(value, max_val):
    ratio = value / max_val
    r = int(255 * ratio)
    g = int(255 * (1 - ratio))
    return (r, g, 150)

# -------- BUTTON CLASS --------
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, selected=False):
        color = (0, 200, 255) if selected else (60, 60, 60)
        pygame.draw.rect(screen, color, self.rect, border_radius=6)

        font = pygame.font.SysFont("Arial", 14)
        txt = font.render(self.text, True, (255, 255, 255))
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 7))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# -------- BUTTONS --------
algo_buttons = [
    Button(10, 10, 100, 30, "QUICK"),
    Button(120, 10, 100, 30, "BUBBLE"),
    Button(230, 10, 100, 30, "MERGE"),
    Button(340, 10, 120, 30, "INSERT"),
    Button(470, 10, 120, 30, "SELECT"),
]

start_button = Button(610, 10, 80, 30, "START")
reset_button = Button(700, 10, 80, 30, "RESET")

speed_up = Button(790, 10, 80, 30, "SPD +")
speed_down = Button(880, 10, 80, 30, "SPD -")

asc_button = Button(10, 50, 100, 30, "ASC")
desc_button = Button(120, 50, 100, 30, "DESC")

# -------- DRAW --------
def draw(pivot=None, current=None):
    screen.fill((0, 0, 0))

    for btn in algo_buttons:
        btn.draw(selected=(btn.text.lower() == algorithm))

    start_button.draw()
    reset_button.draw()
    speed_up.draw()
    speed_down.draw()
    asc_button.draw(selected=ascending)
    desc_button.draw(selected=not ascending)

    max_val = max(data)

    for i in range(len(data)):
        x = i * (bar_width + gap)

        color = get_color(data[i], max_val)

        if i == pivot:
            color = (255, 0, 0)
        elif i == current:
            color = (255, 255, 0)

        pygame.draw.rect(
            screen,
            color,
            (x, HEIGHT - data[i], bar_width, data[i])
        )

    font = pygame.font.SysFont("Arial", 16)
    text = font.render(
        f"{algorithm.upper()} | Speed:{delay} | {'ASC' if ascending else 'DESC'}",
        True,
        (255, 255, 255)
    )
    screen.blit(text, (10, 90))

    pygame.display.update()

# -------- SORTS --------
def bubble_sort():
    for i in range(len(data)):
        if not sorting: return
        for j in range(len(data)-i-1):
            handle_events()
            draw(None, j)
            clock.tick(delay)

            if (data[j] > data[j+1] and ascending) or (data[j] < data[j+1] and not ascending):
                data[j], data[j+1] = data[j+1], data[j]

def insertion_sort():
    for i in range(1, len(data)):
        if not sorting: return
        key = data[i]
        j = i - 1

        while j >= 0 and ((data[j] > key and ascending) or (data[j] < key and not ascending)):
            handle_events()
            draw(None, j)
            clock.tick(delay)

            data[j+1] = data[j]
            j -= 1

        data[j+1] = key

def selection_sort():
    for i in range(len(data)):
        if not sorting: return
        min_idx = i

        for j in range(i+1, len(data)):
            handle_events()
            draw(min_idx, j)
            clock.tick(delay)

            if (data[j] < data[min_idx] and ascending) or (data[j] > data[min_idx] and not ascending):
                min_idx = j

        data[i], data[min_idx] = data[min_idx], data[i]

def partition(low, high):
    pivot = data[high]
    i = low - 1

    for j in range(low, high):
        if not sorting: return high
        handle_events()
        draw(high, j)
        clock.tick(delay)

        if (data[j] < pivot and ascending) or (data[j] > pivot and not ascending):
            i += 1
            data[i], data[j] = data[j], data[i]

    data[i+1], data[high] = data[high], data[i+1]
    return i+1

def quick_sort(low, high):
    if not sorting: return
    if low < high:
        pi = partition(low, high)
        quick_sort(low, pi-1)
        quick_sort(pi+1, high)

def merge_sort(l, r):
    if not sorting: return
    if l < r:
        m = (l+r)//2
        merge_sort(l, m)
        merge_sort(m+1, r)
        merge(l, m, r)

def merge(l, m, r):
    left = data[l:m+1]
    right = data[m+1:r+1]

    i=j=0
    k=l

    while i < len(left) and j < len(right):
        if not sorting: return
        handle_events()
        draw(None, k)
        clock.tick(delay)

        if (left[i] <= right[j] and ascending) or (left[i] >= right[j] and not ascending):
            data[k] = left[i]; i+=1
        else:
            data[k] = right[j]; j+=1
        k+=1

    while i < len(left):
        data[k] = left[i]; i+=1; k+=1

    while j < len(right):
        data[k] = right[j]; j+=1; k+=1

# -------- EVENTS --------
def handle_events():
    global running, sorting, ascending, data, delay, algorithm

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            for btn in algo_buttons:
                if btn.is_clicked(pos):
                    algorithm = btn.text.lower()
                    sorting = False

            if start_button.is_clicked(pos):
                data = generate_data()
                sorting = True

            if reset_button.is_clicked(pos):
                data = generate_data()
                sorting = False

            if speed_up.is_clicked(pos):
                delay = min(240, delay + 10)

            if speed_down.is_clicked(pos):
                delay = max(10, delay - 10)

            if asc_button.is_clicked(pos):
                ascending = True

            if desc_button.is_clicked(pos):
                ascending = False

# -------- MAIN --------
running = True

while running:
    handle_events()

    if sorting:
        if algorithm == "quick":
            quick_sort(0, len(data)-1)
        elif algorithm == "bubble":
            bubble_sort()
        elif algorithm == "merge":
            merge_sort(0, len(data)-1)
        elif algorithm == "insert":
            insertion_sort()
        elif algorithm == "select":
            selection_sort()

        sorting = False

    draw()
    clock.tick(60)

pygame.quit()