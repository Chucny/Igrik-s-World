

from tkinter import *
from time import time
from math import floor

# --- CONFIG ---
WIDTH, HEIGHT = 1000, 1000
FPS = 60

TILE_SIZE = 40
MAP_W, MAP_H = 256, 14
VIEW_W, VIEW_H = WIDTH, HEIGHT

# physics
GRAVITY = 1600.0
MAX_FALL = 1500.0
WALK_ACCEL = 3600.0
MAX_RUN = 330.0
FRICTION = 3800.0
JUMP_SPEED = 900
JUMP_CUTOFF = 0.45

LIVES_START = 20

# tile colors (keeps original tile letters)
TILE_COLORS = {
    'r': 'firebrick',
    'g': 'forestgreen',
    's': 'gold',        # start tile
    'f': 'darkorange',  # finish / goal
    'o': 'orange',
    'b': 'blue',
    'p': 'purple',
    'y': 'yellow',
    'c': 'cyan',
    'w': 'white',
    'b': 'black',
    'q': 'brown',
    'c': 'cyan',
    'x': 'lightblue',
    't': 'grey',
    ' ': None
}

# --- helper to make levels consistent width/height ---
def make_level(rows):
    new = []
    for r in rows:
        if len(r) > MAP_W:
            r = r[:MAP_W]
        new.append(r + ' ' * (MAP_W - len(r)))
    while len(new) < MAP_H:
        new.insert(0, ' ' * MAP_W)
    if len(new) > MAP_H:
        new = new[-MAP_H:]
    return new

# --- ORIGINAL 12 LEVELS (preserved) ---
levels = []

# Level 1
levels.append([
    make_level([
        "                                  ",
        "                                  ",
        "                                  ",
        "                      gg          ",
        "                    gggggg         ",
        "                   gggggggg       ",
        "                       q          ",
        "s                      q                             g     f",
        "ggggggggg  gggggg gggggggggggggggg    g  ggg   g     q     q",
        "qqqqqqqqq  qqqqqq qqqqqqqqqqqqqqqq    q  qqq   q     q     q"
    ]),
    "skyblue",
    False
])

# Level 2
levels.append([
    make_level([
        "                                 ",
        "                                 ",
        "                                                                            ",
        "                            gggg                                      ggg    ",
        "                          gggggggg                                  gggggg   ",
        "                            w                                         b     ",
        "                            b                                         w     ",
        "                            w                  ggg                    b              ",
        "sggggggg    g      gggggggggggggggggggg        qqq         ggg       ggg        ggggf",
        "qqqqqqqq    q      qqqqqqqqqqqqqqqqqqqq        qqq         qqq       qqq        qqqqq"
    ]),
    "skyblue",
    False
])

# Level 3
levels.append([
    make_level([
        "                               ",
        "                                ",
        "                                 ",
        "                                                                 gg ",
        "                     gggg                                      ggggg ",
        "                   ggggggg                                       b  ",
        "                     qqq                                         w   ",
        "                     qqq                             ggg    gggggggg     ggf",
        "sgggggggg   ggggggggggggggggggggg     ggg    gggg    qqq    qqqqqqqq     qqq",
        "qqqqqqqqq   qqqqqqqqqqqqqqqqqqqqq     qqq    qqqq    qqq    qqqqqqqq     qqq"
    ]),
    "skyblue",
    False
])

# Level 4
levels.append([
    make_level([
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                          gg    ",
        "                        ggggg    ",
        "                          q     ",
        "                          q                       ggg   ggggf",
        "ggggggggg   g    ggggggggggggggggg   ggggg   g    qqq   qqqqq",
        "qqqqqqqqq   q    qqqqqqqqqqqqqqqqq   qqqqq   q    qqq   qqqqq"
    ]),
    "skyblue",
    False
])

# Level 5
levels.append([
    make_level([
        "                                ",
        "                                ",
        "                                                                         ggg",
        "                          ggg                                          gggggg",
        "                        gggggg                                           w",
        "                          b                                              b ",
        "                          w                                              w",
        "                          b                       ggggg   ggggg  gggggggggggggggggg   ggggf",
        "ggggggggg   g    ggggggggggggggggg   ggggg   gg   qqqqq   qqqqq  qqqqqqqqqqqqqqqqqq   qqqqq",
        "qqqqqqqqq   q    qqqqqqqqqqqqqqqqq   qqqqq   qq   qqqqq   qqqqq  qqqqqqqqqqqqqqqqqq   qqqqq"
    ]),
    "skyblue",
    False
])

# Level 6
levels.append([
    make_level([
        "                                ",
        "                                ",
        "                                                ",
        "                                      ggg       ",
        "                   ggg        gg    gggggg   gg",
        "                  ggggg     ggggg     b    ggggg  ",
        "                    q         q       w      q   ",
        "                    q         q       b      q   ",
        "sggggggggg  ggggggggggggg    ggg     ggg    ggg     ggggf     ",
        "qqqqqqqqqq  qqqqqqqqqqqqq    qqq     qqq    qqq     qqqqq      "
    ]),
    "skyblue",
    False
])

# Level 7
levels.append([
    make_level([
        "                                ",
        "                                ",
        "                                                                      ",
        "                                                                       ggg",
        "                           gg                     gg                 ggggggg                      ",
        "                         ggggg                  ggggg                   w                          ",
        "                           q                      w                     b                         ",
        "                           q                      b                     w                         ",
        "gggggggggg    ggggg   gggggggggg    ggggg   gggggggggg    ggggg   gggggggggg    ggggg   gggggggggf",
        "qqqqqqqqqq    qqqqq   qqqqqqqqqq    qqqqq   qqqqqqqqqq    qqqqq   qqqqqqqqqq    qqqqq   qqqqqqqqqq"
    ]),
    "skyblue",
    False
])

# Level 8
levels.append([
    make_level([
        "                                ",
        "                                ",
        "                                ",
        "                          ggg   ",
        "                         ggggg   ",
        "                           w    ",
        "                           b    ",
        "                           w    ",
        "    sggggggggggggggggggggggggggf",
        "    qqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    ]),
    "lightblue",
    True
])

# Level 9, New World! Castle.
levels.append([
    make_level([
        "                                         brrrr          ",
        "                                         brrrr          ",
        "                                         b              ",
        "                               t t t t t bt t t t t t t",
        "                               tttttttttttttttttttttttttttttt      ",
        "                      t t t    t                       t    t ",
        "                      ttttt                                 t  ",
        "                      ttttt                                 t  ",
        "sttttttttt   ttttttttttttttttttttttttttt   tttt    ttttttttft",
        "tttttttttt   ttttttttttttttttttttttttttt   tttt    tttttttttt"
    ]),
    "lightskyblue",
    False
])

# Level 10
levels.append([
    make_level([
        "                                              ",
        "                                               ",
        "                      brrr                      ",
        "                      brrr                      ",
        "                      b                         ",
        "            ttttttttttttttttttttt                       ",
        "            t                   t                        ",
        "                                t                        ",
        "sgggggggggggtttttttttttttttttttotgggggggggggggg   ggg     g      gggg   ggggf",
        "qqqqqqqqqqqqtttttttttttttttttttttqqqqqqqqqqqqqq   qqq     q      qqqq   qqqqq"
    ]),
    "skyblue",
    False
])

# Level 11
levels.append([
    make_level([
        "                                              ",
        "                                               ",
        "                      brrr                      ",
        "                      brrr                      ",
        "                      b                         ",
        "            ttttttttttttttttttttt                       ",
        "            t                   t                        ",
        "                                t                        ",
        "sgggggggggggtttttttttttttttttttftgggggggggggggg   ggg     g      gggg   ggggo",
        "qqqqqqqqqqqqtttttttttttttttttttttqqqqqqqqqqqqqq   qqq     q      qqqq   qqqqq"    ]),
    "skyblue",
    False
])

# Level 12: Boss 
levels.append([
    make_level([
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                         t t t  ",
        "                         ttttt  ",
        "                         ttttt  ",
        "   sttttttttttttttttttttttttttttttttf",
        "   tttttttttttttttttttttttttttttttttt"
    ]),
    "lightblue",
    True   
])
# Level 13: Snowy Forest 
levels.append([
    make_level([
        "                                ",
        "                                ",
        "                                ",
        "                               ",
        "                          w     ",
        "                         www    ",
        "                        wwwww   ",
        "                          q     ",
        "swwwwwwww   ww   wwwwwwwwwwwwwwww    w    ww     www  wwf",
        "qqqqqqqqq   qq   qqqqqqqqqqqqqqqq    q    qq     qqq  qqq"
    ]),
    "lightblue",
    False   
])
#Level 14
levels.append([
    make_level([
        "                                        ",
        "                                        ",
        "                                        ",
        "                                        ",
        "                              w                                                                        f    ",
        "                             www                                                                      www  ",
        "                            wwwww                                                                    wwwww ",
        "                              q                                                                        q   ",
        "swwwwwwww    www     wwwwwwwwwwwwwwww   wwww   wwwwwww   wwww   wwwwwww   wwww   wwwwwww   wwwwwwwwwwwwww  ",
        "qqqqqqqqq    qqq     qqqqqqqqqqqqqqqq   qqqq   qqqqqqq   qqqq   qqqqqqq   qqqq   qqqqqqq   qqqqqqqqqqqqqq"
    ]),
    "lightblue",
    False   
])
levels.append([
    make_level([
        "                                        ",
        "                                        ",
        "                                        ",
        "                                        ",
        "                              w                                                                        w    ",
        "                             www                                                                      www  ",
        "                            wwwww                                                                    wwwww ",
        "                              q                                                                        q   ",
        "swwwwwwww    www     wwwwwwwwwwwwwwww   wwww   wwwwwww   wwww   wwwwwww   wwww   wwwwwww   wwwwwwwwwwwwwwwwwwwwwwwwww    wwwwww   www    wwwwf",
        "qqqqqqqqq    qqq     qqqqqqqqqqqqqqqq   qqqq   qqqqqqq   qqqq   qqqqqqq   qqqq   qqqqqqq   qqqqqqqqqqqqqqqqqqqqqqqqqq    qqqqqq   qqq    qqqqq"
    ]),
    "lightblue",
    False   
])
levels.append([
    make_level([
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                          w     ",
        "                         www    ",
        "                        wwwww    ",
        "                          q          ",
        "   swwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwf",
        "   qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    ]),
    "lightblue",
    True   
])
levels.append([
    make_level([
        "                                                ",
        "                                                ",
        "                                                ",
        "                                                ",
        "                                                         t ",
        "                                                        ttt         ",
        "             tt                                          t           ",
        "             tt     o                      o             t           ",
        "sgggggggggggggggggggggggggg   gg     g  gggggg   gggg  gggggg   gggggf",
        "qqqqqqqqqqqqqqqqqqqqqqqqqqq   qq     q  gggggg   qqqq  qqqqqq   qqqqqq"
    ]),
    "black",
    False   
])
levels.append([
    make_level([
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                             t  ",
        "                            ttt ",
        "                             t  ",
        "                             t       ",
        "   sggggggggggggggggggggggggggggggggggggggf",
        "   qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    ]),
    "black",
    True   
])
levels.append([
    make_level([
        "                                ",
        "     wwwww    w  w    wwwww  w   w  w w    w w   wwwww  w   w           w  wwwww  wwww  w  w w  w ",
        "       w      w  w    w   w  ww  w  ww      w    w   w  w   w           w  w      w  w  w  ww   w ",
        "       w      wwww    wwwww  w w w  w w     w    w   w  w   w           w  w  ww  www   w  ww      ",
        "       w      w  w    w   w  w  ww  w  w    w    wwwww  wwwww   w       w  wwwww  w  w  w  w w  w ",
        "                                                                w                                  ",
        "                                                                                                    ",
        "                                                                                                    ",
        "swwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
        "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"
    ]),
    "skyblue",
    False   
])


# --- GAME STATE ---
current_level_index = 0
level_map, level_bg, has_boss = levels[current_level_index]

camera_x = 0.0

player = {
    'w': int(TILE_SIZE * 0.8),
    'h': int(TILE_SIZE * 0.9),
    'x': 0.0, 'y': 0.0,
    'vx': 0.0, 'vy': 0.0,
    'on_ground': False,
    'lives': LIVES_START,
    'invuln': 0.0
}

score = 0

# Enemies and boss lists
enemies = []
projectiles = []       # hostile (boss) fireballs
player_fireballs = []  # friendly (player) fireballs — only damage boss
boss = None

# --- TKINTER UI ---
root = Tk()
root.title("Igrik's World")
canvas = Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
canvas.pack()

# HUD (created but will be hidden during gameplay)
score_id = canvas.create_text(80, 18, text="Score: 0", fill="white", anchor='w', font=("Helvetica", 14))
lives_id = canvas.create_text(80, 38, text=f"Lives: {player['lives']}", fill="white", anchor='w', font=("Helvetica", 14))
level_id = canvas.create_text(WIDTH - 10, 18, text=f"Level: 1/12", fill="white", anchor='e', font=("Helvetica", 14))

# --- INPUT ---
keys = set()
jump_pressed = False
jump_held = False
state = "title"

def on_key_press(ev):
    global jump_pressed, jump_held, state
    k = ev.keysym.lower()
    # start on Enter from title
    if state == "title" and ev.keysym == "Return":
        start_new_game()
        return
    keys.add(k)
    if k == 'space' and not jump_held:
        jump_pressed = True
        jump_held = True
    # SHIFT to shoot — only when boss alive in boss level
    if ev.keysym in ('Shift_L', 'Shift_R'):
        if has_boss and boss and boss.get('alive', False):
            # direction based on boss position relative to player
            direction = 1 if boss['x'] > player['x'] else -1
            spawn_player_fireball(player['x'] + direction*(player['w']/2 + 6), player['y'] - 8, direction * 420)

def on_key_release(ev):
    global jump_held
    k = ev.keysym.lower()
    if k in keys:
        keys.remove(k)
    if k == 'space':
        jump_held = False

root.bind_all("<KeyPress>", on_key_press)
root.bind_all("<KeyRelease>", on_key_release)

# --- TILE & COLLISION HELPERS ---
def tile_at(col, row):
    if 0 <= col < MAP_W and 0 <= row < MAP_H:
        return level_map[row][col]
    return ' '

def world_to_tile(px, py):
    return int(px // TILE_SIZE), int(py // TILE_SIZE)

def rects_overlap(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    return not (ax2 <= bx1 or ax1 >= bx2 or ay2 <= by1 or ay1 >= by2)

def get_solid_tiles(x, y, w, h):
    left = int((x - w/2) // TILE_SIZE)
    right = int((x + w/2) // TILE_SIZE)
    top = int((y - h/2) // TILE_SIZE)
    bottom = int((y + h/2) // TILE_SIZE)
    tiles = []
    for r in range(top, bottom + 1):
        for c in range(left, right + 1):
            t = tile_at(c, r)
            if t != ' ':
                tiles.append((c, r, t, c*TILE_SIZE, r*TILE_SIZE, (c+1)*TILE_SIZE, (r+1)*TILE_SIZE))
    return tiles

# --- DRAW PLAYER (Igrik) ---
def draw_igrik(px, py, w, h, tag):
    # body
    canvas.create_oval(px - w/2, py - h/2, px + w/2, py + h/2, fill="green", tags=tag, outline="")
    # eyes
    canvas.create_oval(px - w*0.2 - 7, py - h*0.15 - 7, px - w*0.2 + 7, py - h*0.15 + 7, fill="white", tags=tag, outline="")
    canvas.create_oval(px + w*0.2 - 7, py - h*0.15 - 7, px + w*0.2 + 7, py - h*0.15 + 7, fill="white", tags=tag, outline="")
    # pupils
    canvas.create_oval(px - w*0.2 - 3, py - h*0.15 - 3, px - w*0.2 + 3, py - h*0.15 + 3, fill="black", tags=tag, outline="")
    canvas.create_oval(px + w*0.2 - 3, py - h*0.15 - 3, px + w*0.2 + 3, py - h*0.15 + 3, fill="black", tags=tag, outline="")
    # mouth
    canvas.create_oval(px - w*0.25, py + h*0.08, px + w*0.25, py + h*0.3, fill="red", tags=tag, outline="")

# --- SPAWN HELPERS ---

def spawn_fireball(x, y, vx):
    projectiles.append({'x': x, 'y': y, 'vx': vx, 'r': 8})

def spawn_player_fireball(x, y, vx):
    player_fireballs.append({'x': x, 'y': y, 'vx': vx, 'r': 8})

# --- BOSS FACTORY (classic stationary arena boss) ---
def create_boss(player_x):
    # place boss a bit to the right of player start so it's visible without extra walking
    bx = player_x + 398
    by = (MAP_H - 4) * TILE_SIZE  # stand above ground row
    return {'x': bx, 'y': by, 'w': TILE_SIZE*3.6, 'h': TILE_SIZE*2.6, 'hp': 10, 'fire_timer': 0.0, 'alive': True}

# --- LEVEL LOADING / PROGRESSION ---
def find_start(maprows):
    for r_i, row in enumerate(maprows):
        c = row.find('s')
        if c != -1:
            px = c * TILE_SIZE + TILE_SIZE/2
            py = r_i * TILE_SIZE + TILE_SIZE/2
            return px, py
    return TILE_SIZE*2, (MAP_H-2)*TILE_SIZE

def load_level(index):
    global level_map, level_bg, has_boss, camera_x, enemies, projectiles, boss, player_fireballs
    enemies.clear(); projectiles.clear(); player_fireballs.clear(); boss = None
    load = levels[index]
    level_map_local = load[0]
    level_bg_local = load[1]
    has_boss_local = load[2]
    globals()['level_map'] = level_map_local
    globals()['level_bg'] = level_bg_local
    globals()['has_boss'] = has_boss_local

    
    # spawn player at start
    px, py = find_start(level_map_local)
    player['x'] = px; player['y'] = py; player['vx'] = 0; player['vy'] = 0; player['on_ground'] = False; player['invuln'] = 0
    globals()['camera_x'] = max(0.0, player['x'] - WIDTH//2)

    # boss if level requires — classic arena (stationary)
    if has_boss_local:
        boss_local = create_boss(player['x'])
        globals()['boss'] = boss_local

    # hide HUD items while playing
    canvas.itemconfigure(score_id, state='hidden')
    canvas.itemconfigure(lives_id, state='hidden')
    canvas.itemconfigure(level_id, state='hidden')

def respawn_player():
    player['lives'] -= 1
    if player['lives'] <= 0:
        show_title()
    else:
        px, py = find_start(level_map)
        player['x'] = px; player['y'] = py; player['vx'] = 0; player['vy'] = 0; player['on_ground'] = False

def next_level():
    global current_level_index
    if boss and boss.get('alive', False):
        return
    if current_level_index + 1 < len(levels):
        current_level_index += 1
        load_level(current_level_index)
    else:
        show_title()

# --- TITLE SCREEN ---
def show_title():
    global state
    state = "title"
    canvas.delete(ALL)
    canvas.configure(bg="lightblue")
    canvas.create_text(WIDTH/2, HEIGHT/4, text="IGRIK'S WORLD", font=("Helvetica", 48, "bold"), fill="white")
    canvas.create_text(WIDTH/2, HEIGHT/4 + 48, text="", font=("Helvetica", 16), fill="white")
    def button(xc, yc, txt, cmd):
        rect = canvas.create_rectangle(xc-140, yc-28, xc+140, yc+28, fill="#8b8b8b", outline="black", width=4)
        label = canvas.create_text(xc, yc, text=txt, font=("Helvetica", 20, "bold"), fill="white")
        def enter(e): canvas.itemconfig(rect, fill="#6f6f6f")
        def leave(e): canvas.itemconfig(rect, fill="#8b8b8b")
        def click(e): cmd()
        canvas.tag_bind(rect, "<Enter>", enter); canvas.tag_bind(label, "<Enter>", enter)
        canvas.tag_bind(rect, "<Leave>", leave); canvas.tag_bind(label, "<Leave>", leave)
        canvas.tag_bind(rect, "<Button-1>", click); canvas.tag_bind(label, "<Button-1>", click)
    button(WIDTH/2, HEIGHT/2 - 10, "New Game", start_new_game)
    button(WIDTH/2, HEIGHT/2 + 60, "Quit Game", root.destroy)
    canvas.create_text(WIDTH/2, HEIGHT - 30, text="Copyright (C) Chucny 2025 All rights reserved.", fill="white")

def start_new_game():
    global state, current_level_index
    state = "game"
    current_level_index = 0
    player['lives'] = LIVES_START
    canvas.delete(ALL)
    load_level(current_level_index)
    game_loop_start()

# --- ENEMY PATROL (fixed single-move per update) ---
def simulate_enemy(e, dt):
    # move
    e['x'] += e['vx'] * dt

    # decide tile ahead and tile below that tile
    sign = 1 if e['vx'] >= 0 else -1
    ahead_x = e['x'] + sign * (e['w']/2 + 2)
    foot_y = e['y'] + e['h']/2 + 2

    ac, ar = world_to_tile(ahead_x, e['y'])
    bc, br = world_to_tile(ahead_x, foot_y)

    tile_ahead = tile_at(ac, ar)
    tile_below_ahead = tile_at(bc, br)

    # reverse when wall ahead or no ground under the tile ahead
    if tile_ahead != ' ' or tile_below_ahead == ' ':
        e['vx'] *= -1
        # tiny nudge to avoid getting stuck
        e['x'] += e['vx'] * dt

# --- MAIN UPDATE LOOP ---
last_time = time()

def update(dt):
    global camera_x, score, boss
    if state != "game":
        return

    left = ('a' in keys or 'left' in keys)
    right = ('d' in keys or 'right' in keys)

    if left and not right:
        player['vx'] -= WALK_ACCEL * dt
    elif right and not left:
        player['vx'] += WALK_ACCEL * dt
    else:
        # friction
        if player['vx'] > 0:
            player['vx'] = max(0.0, player['vx'] - FRICTION * dt)
        elif player['vx'] < 0:
            player['vx'] = min(0.0, player['vx'] + FRICTION * dt)

    # clamp
    if player['vx'] > MAX_RUN: player['vx'] = MAX_RUN
    if player['vx'] < -MAX_RUN: player['vx'] = -MAX_RUN

    global jump_pressed
    if jump_pressed and player['on_ground']:
        player['vy'] = -JUMP_SPEED
        player['on_ground'] = False
    jump_pressed = False
    if (not jump_held) and player['vy'] < 0:
        player['vy'] = player['vy'] * JUMP_CUTOFF

    # gravity
    player['vy'] += GRAVITY * dt
    if player['vy'] > MAX_FALL:
        player['vy'] = MAX_FALL

    # horizontal movement & collision
    new_x = player['x'] + player['vx'] * dt
    half_w, half_h = player['w']/2, player['h']/2
    solids = get_solid_tiles(new_x, player['y'], player['w'], player['h'])
    if solids:
        for c, r, ch, tx1, ty1, tx2, ty2 in solids:
            if rects_overlap(new_x - half_w, player['y'] - half_h, new_x + half_w, player['y'] + half_h, tx1, ty1, tx2, ty2):
                if player['vx'] > 0:
                    new_x = tx1 - half_w - 0.001
                elif player['vx'] < 0:
                    new_x = tx2 + half_w + 0.001
                player['vx'] = 0.0
    player['x'] = new_x

    # vertical movement & collision
    new_y = player['y'] + player['vy'] * dt
    solids = get_solid_tiles(player['x'], new_y, player['w'], player['h'])
    player['on_ground'] = False
    if solids:
        for c, r, ch, tx1, ty1, tx2, ty2 in solids:
            if rects_overlap(player['x'] - half_w, new_y - half_h, player['x'] + half_w, new_y + half_h, tx1, ty1, tx2, ty2):
                if player['vy'] > 0:
                    new_y = ty1 - half_h - 0.001
                    player['vy'] = 0.0
                    player['on_ground'] = True
                    # finish tile finishes level only if boss not alive
                    if ch == 'f' and (not boss or not boss.get('alive', False)):
                        next_level()
                elif player['vy'] < 0:
                    new_y = ty2 + half_h + 0.001
                    player['vy'] = 0.0
    player['y'] = new_y

    # falling into void
    if player['y'] - half_h > MAP_H * TILE_SIZE + TILE_SIZE*2:
        respawn_player()
        return

    # camera center on player
    camera_x = player['x'] - WIDTH / 2
    if camera_x < 0: camera_x = 0
    max_cam = MAP_W * TILE_SIZE - WIDTH
    if camera_x > max_cam: camera_x = max_cam

    # update enemies (simulate_enemy moves them; do NOT move again)
    for e in list(enemies):
        simulate_enemy(e, dt)
        # collision with player
        if rects_overlap(e['x'] - e['w']/2, e['y'] - e['h']/2, e['x'] + e['w']/2, e['y'] + e['h']/2,
                         player['x'] - half_w, player['y'] - half_h, player['x'] + half_w, player['y'] + half_h):
            if player['vy'] > 150:
                try:
                    enemies.remove(e)
                    score += 25
                except ValueError:
                    pass
            else:
                respawn_player()
                return

    # update boss (stationary arena)
    if boss and boss.get('alive', False):
        # boss is stationary but shoots periodically
        boss['fire_timer'] += dt
        if boss['fire_timer'] > 1.2:
            boss['fire_timer'] = 0.0
            # spawn projectile toward player (direction)
            direction = -1 if boss['x'] > player['x'] else 1
            spawn_fireball(boss['x'] - direction*30, boss['y'] - boss['h']/4, direction * 260)

        # boss collision with player: if player lands on boss top while falling -> damage boss
        if rects_overlap(boss['x'] - boss['w']/2, boss['y'] - boss['h']/2, boss['x'] + boss['w']/2, boss['y'] + boss['h']/2,
                         player['x'] - half_w, player['y'] - half_h, player['x'] + half_w, player['y'] + half_h):
            if player['vy'] > 150:
                boss['hp'] -= 1
                player['vy'] = -JUMP_SPEED*0.5
                if boss['hp'] <= 0:
                    boss['alive'] = False
                    score += 500
            else:
                respawn_player()
                return

    # update hostile projectiles
    for proj in list(projectiles):
        proj['x'] += proj['vx'] * dt
        proj['y'] += 60 * dt
        # collision with player
        if rects_overlap(proj['x'] - proj['r'], proj['y'] - proj['r'], proj['x'] + proj['r'], proj['y'] + proj['r'],
                         player['x'] - half_w, player['y'] - half_h, player['x'] + half_w, player['y'] + half_h):
            if proj in projectiles: projectiles.remove(proj)
            respawn_player()
            return
        # collision with tiles
        tc, tr = world_to_tile(proj['x'], proj['y'])
        if tile_at(tc, tr) != ' ':
            if proj in projectiles: projectiles.remove(proj)
        # off-world cleanup
        if proj['x'] < -100 or proj['x'] > MAP_W*TILE_SIZE + 100 or proj['y'] > MAP_H * TILE_SIZE + 300:
            if proj in projectiles: projectiles.remove(proj)

    # update player-fired fireballs (orange) — only damage boss
    for pf in list(player_fireballs):
        pf['x'] += pf['vx'] * dt
        # boss collision
        if boss and boss.get('alive', False):
            if rects_overlap(pf['x'] - pf['r'], pf['y'] - pf['r'], pf['x'] + pf['r'], pf['y'] + pf['r'],
                             boss['x'] - boss['w']/2, boss['y'] - boss['h']/2, boss['x'] + boss['w']/2, boss['y'] + boss['h']/2):
                boss['hp'] -= 1
                if pf in player_fireballs: player_fireballs.remove(pf)
                if boss['hp'] <= 0:
                    boss['alive'] = False
                    score += 500
                continue
        # collision with tiles
        tc, tr = world_to_tile(pf['x'], pf['y'])
        if tile_at(tc, tr) != ' ':
            if pf in player_fireballs: player_fireballs.remove(pf)
            continue
        if pf['x'] < -200 or pf['x'] > MAP_W*TILE_SIZE + 200 or pf['y'] > MAP_H * TILE_SIZE + 400 or pf['y'] < -200:
            if pf in player_fireballs: player_fireballs.remove(pf)

    # DRAW
    render()

# --- RENDER ---
def render():
    canvas.delete("world")
    # background
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill=level_bg, width=0, tags="world")
    # draw visible tiles
    first_col = int(camera_x // TILE_SIZE)
    last_col = int((camera_x + WIDTH) // TILE_SIZE) + 1
    first_col = max(0, first_col)
    last_col = min(MAP_W - 1, last_col)
    for r in range(MAP_H):
        row = level_map[r]
        for c in range(first_col, last_col + 1):
            ch = row[c]
            if ch != ' ':
                color = TILE_COLORS.get(ch, 'grey')
                x1 = c * TILE_SIZE - camera_x
                y1 = r * TILE_SIZE
                x2 = x1 + TILE_SIZE
                y2 = y1 + TILE_SIZE
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags="world")
                # draw flag for finish
                if ch == 'f':
                    canvas.create_text(x1 + TILE_SIZE/2, y1 + TILE_SIZE/2, text="🏁", font=("Helvetica", 18), tags="world")

    # draw enemies
    for e in enemies:
        ex = e['x'] - camera_x
        ey = e['y']
        canvas.create_oval(ex - e['w']/2, ey - e['h']/2, ex + e['w']/2, ey + e['h']/2, fill="brown", tags="world")
        canvas.create_rectangle(ex - 6, ey + e['h']/4, ex + 6, ey + e['h']/4 + 8, fill="black", tags="world")

    # draw boss (classic stationary red dragon)
    if boss and boss.get('alive', False):
        bx = boss['x'] - camera_x
        by = boss['y']
        # body
        canvas.create_oval(bx - boss['w']/2, by - boss['h']/2, bx + boss['w']/2, by + boss['h']/2, fill="red", tags="world")
        # wings (simple polygons)
        wing_offset_y = boss['h'] * 0.15
        canvas.create_polygon(bx - boss['w']/2 + 8, by - boss['h']/4,
                              bx - boss['w']/2 - boss['w']*0.35, by - boss['h']/2 - wing_offset_y,
                              bx - boss['w']/2 + 8, by + boss['h']/6,
                              fill="darkred", tags="world", outline="")
        canvas.create_polygon(bx + boss['w']/2 - 8, by - boss['h']/4,
                              bx + boss['w']/2 + boss['w']*0.35, by - boss['h']/2 - wing_offset_y,
                              bx + boss['w']/2 - 8, by + boss['h']/6,
                              fill="darkred", tags="world", outline="")
        # eyes
        eye_x = boss['w'] * 0.18
        canvas.create_oval(bx - eye_x - 6, by - boss['h']/4 - 6, bx - eye_x + 6, by - boss['h']/4 + 6, fill="green", tags="world")
        canvas.create_oval(bx + eye_x - 6, by - boss['h']/4 - 6, bx + eye_x + 6, by - boss['h']/4 + 6, fill="green", tags="world")
        # horns
        canvas.create_polygon(bx - boss['w']/6, by - boss['h']/2, bx - boss['w']/6 - 10, by - boss['h']/2 - 20, bx - boss['w']/6 + 10, by - boss['h']/2 - 8, fill="yellow", tags="world")
        canvas.create_polygon(bx + boss['w']/6, by - boss['h']/2, bx + boss['w']/6 + 10, by - boss['h']/2 - 20, bx + boss['w']/6 - 10, by - boss['h']/2 - 8, fill="yellow", tags="world")
        # HP text above boss
        canvas.create_text(bx, by - boss['h']/2 - 12, text=f"HP: {boss['hp']}", fill="white", tags="world")

    # hostile projectiles (orange)
    for p in projectiles:
        px = p['x'] - camera_x
        py = p['y']
        canvas.create_oval(px - p['r'], py - p['r'], px + p['r'], py + p['r'], fill="orange", tags="world")

    # player fireballs (orange)
    for pf in player_fireballs:
        px = pf['x'] - camera_x
        py = pf['y']
        canvas.create_oval(px - pf['r'], py - pf['r'], px + pf['r'], py + pf['r'], fill="orange", tags="world")

    # draw player
    px_screen = player['x'] - camera_x
    py_screen = player['y']
    draw_igrik(px_screen, py_screen, player['w'], player['h'], "world")

    # ensure HUD (hidden in gameplay) is on top if title shows it
    canvas.lift(score_id)
    canvas.lift(lives_id)
    canvas.lift(level_id)

# --- MAIN LOOP CONTROL ---
def game_loop_start():
    global last_time
    last_time = time()
    _loop()

def _loop():
    global last_time
    now = time()
    dt = now - last_time
    if dt > 0.1: dt = 0.1
    last_time = now
    update(dt)
    root.after(int(1000 / FPS), _loop)

# --- INITIALIZE TITLE ---
show_title()
root.mainloop()
