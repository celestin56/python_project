import pygame
import random
import time
import numpy as np
import math

# Initialisation de Pygame et du Mixer Audio
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Tailles de l'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (30, 144, 255)
DARK_BLUE = (20, 20, 60)
GRAY = (200, 200, 200)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu d'avion - World Music Edition")

# Polices
font_small = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 64)


# --- SYNTHÉTISEUR AUDIO EN MÉMOIRE ---

def create_sound_from_array(array):
    """Convertit un tableau numpy d'échantillons audio en Pygame Sound."""
    stereo_array = np.column_stack((array, array))
    return pygame.sndarray.make_sound(stereo_array.astype(np.int16))

def generate_laser_sound():
    duration = 0.12
    sample_rate = 44100
    n_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, n_samples, False)
    freq = np.linspace(900, 300, n_samples)
    waveform = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-t * 25)
    return create_sound_from_array((waveform * envelope * 12000).astype(np.int16))

def generate_explosion_sound():
    duration = 0.35
    sample_rate = 44100
    n_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, n_samples, False)
    noise = np.random.uniform(-1, 1, n_samples)
    envelope = np.exp(-t * 12)
    return create_sound_from_array((noise * envelope * 16000).astype(np.int16))

def generate_powerup_sound():
    duration = 0.2
    sample_rate = 44100
    n_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, n_samples, False)
    freq = np.linspace(400, 1000, n_samples)
    waveform = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-t * 8)
    return create_sound_from_array((waveform * envelope * 14000).astype(np.int16))

def generate_gameover_sound():
    duration = 0.6
    sample_rate = 44100
    n_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, n_samples, False)
    freq = np.linspace(250, 80, n_samples)
    waveform = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-t * 4)
    return create_sound_from_array((waveform * envelope * 18000).astype(np.int16))


# --- GÉNÉRATEURS DE STYLES MUSICAUX ---

def generate_rock_loop():
    sample_rate = 44100
    bpm = 130
    beat_duration = 60 / bpm
    total_duration = beat_duration * 16
    n_samples = int(total_duration * sample_rate)
    t = np.linspace(0, total_duration, n_samples, False)
    track = np.zeros(n_samples)
    
    notes = [82.41, 82.41, 98.00, 110.00, 82.41, 82.41, 130.81, 146.83]
    samples_per_note = n_samples // len(notes)
    
    for i, freq in enumerate(notes):
        start = i * samples_per_note
        end = (i + 1) * samples_per_note
        t_note = t[start:end] - t[start]
        wave = np.sin(2 * np.pi * freq * t_note) + 0.5 * np.sin(2 * np.pi * freq * 2 * t_note)
        wave = np.clip(wave * 2.0, -1.0, 1.0)
        env = np.exp(-t_note * 3)
        track[start:end] += wave * env * 7000

    beat_samples = int(beat_duration * sample_rate)
    for step in range(16):
        idx = step * beat_samples
        if idx < n_samples:
            length = min(beat_samples, n_samples - idx)
            t_perc = np.linspace(0, length / sample_rate, length, False)
            if step % 2 == 0:
                kick = np.sin(2 * np.pi * np.linspace(150, 40, length) * t_perc) * np.exp(-t_perc * 15)
                track[idx:idx+length] += kick * 10000
            else:
                snare = np.random.uniform(-1, 1, length) * np.exp(-t_perc * 20)
                track[idx:idx+length] += snare * 7000

    return create_sound_from_array(track.astype(np.int16))

def generate_rnb_loop():
    sample_rate = 44100
    bpm = 90
    beat_duration = 60 / bpm
    total_duration = beat_duration * 16
    n_samples = int(total_duration * sample_rate)
    t = np.linspace(0, total_duration, n_samples, False)
    track = np.zeros(n_samples)

    chords = [[146.83, 174.61, 220.00, 261.63], [130.81, 164.81, 196.00, 246.94]]
    samples_per_chord = n_samples // 4

    for i in range(4):
        chord = chords[i % 2]
        start = i * samples_per_chord
        end = (i + 1) * samples_per_chord
        t_chord = t[start:end] - t[start]
        for freq in chord:
            wave = np.sin(2 * np.pi * freq * t_chord) * np.exp(-t_chord * 1.5)
            track[start:end] += wave * 2500

    beat_samples = int(beat_duration * sample_rate)
    for step in range(16):
        idx = step * beat_samples
        if idx < n_samples:
            length = min(beat_samples, n_samples - idx)
            t_perc = np.linspace(0, length / sample_rate, length, False)
            if step in [0, 6, 10]:
                kick = np.sin(2 * np.pi * np.linspace(100, 30, length) * t_perc) * np.exp(-t_perc * 10)
                track[idx:idx+length] += kick * 12000
            elif step in [4, 12]:
                rim = np.sin(2 * np.pi * 800 * t_perc) * np.exp(-t_perc * 40)
                track[idx:idx+length] += rim * 8000

    return create_sound_from_array(track.astype(np.int16))

def generate_chinese_loop():
    sample_rate = 44100
    bpm = 110
    beat_duration = 60 / bpm
    total_duration = beat_duration * 16
    n_samples = int(total_duration * sample_rate)
    t = np.linspace(0, total_duration, n_samples, False)
    track = np.zeros(n_samples)

    pentatonic = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25]
    samples_per_note = n_samples // 16

    for i in range(16):
        freq = pentatonic[(i * 3 + (i % 5)) % len(pentatonic)]
        start = i * samples_per_note
        end = (i + 1) * samples_per_note
        t_note = t[start:end] - t[start]
        
        wave = np.sin(2 * np.pi * freq * t_note) + 0.3 * np.sin(2 * np.pi * freq * 3 * t_note)
        env = np.exp(-t_note * 5)
        track[start:end] += wave * env * 6000

    beat_samples = int(beat_duration * sample_rate)
    for step in range(0, 16, 4):
        idx = step * beat_samples
        if idx < n_samples:
            length = min(beat_samples, n_samples - idx)
            t_perc = np.linspace(0, length / sample_rate, length, False)
            woodblock = np.sin(2 * np.pi * 1200 * t_perc) * np.exp(-t_perc * 30)
            track[idx:idx+length] += woodblock * 5000

    return create_sound_from_array(track.astype(np.int16))

def generate_indian_loop():
    sample_rate = 44100
    bpm = 120
    beat_duration = 60 / bpm
    total_duration = beat_duration * 16
    n_samples = int(total_duration * sample_rate)
    t = np.linspace(0, total_duration, n_samples, False)
    track = np.zeros(n_samples)

    drone = np.sin(2 * np.pi * 130.81 * t) * 0.4 + np.sin(2 * np.pi * 196.00 * t) * 0.3
    track += drone * 2000

    raga_notes = [261.63, 277.18, 329.63, 349.23, 392.00, 415.30, 493.88, 523.25]
    samples_per_note = n_samples // 16

    for i in range(16):
        freq = raga_notes[(i * 5) % len(raga_notes)]
        start = i * samples_per_note
        end = (i + 1) * samples_per_note
        t_note = t[start:end] - t[start]
        wave = np.sin(2 * np.pi * freq * t_note) + 0.6 * np.sin(2 * np.pi * freq * 2 * t_note)
        env = np.exp(-t_note * 8)
        track[start:end] += wave * env * 5000

    beat_samples = int(beat_duration * sample_rate // 2)
    for step in range(32):
        idx = step * beat_samples
        if idx < n_samples:
            length = min(beat_samples, n_samples - idx)
            t_perc = np.linspace(0, length / sample_rate, length, False)
            if step % 2 == 0:
                tabla_low = np.sin(2 * np.pi * np.linspace(160, 90, length) * t_perc) * np.exp(-t_perc * 12)
                track[idx:idx+length] += tabla_low * 7000
            else:
                tabla_hi = np.sin(2 * np.pi * 500 * t_perc) * np.exp(-t_perc * 25)
                track[idx:idx+length] += tabla_hi * 5000

    return create_sound_from_array(track.astype(np.int16))

def generate_african_loop():
    sample_rate = 44100
    bpm = 135
    beat_duration = 60 / bpm
    total_duration = beat_duration * 16
    n_samples = int(total_duration * sample_rate)
    t = np.linspace(0, total_duration, n_samples, False)
    track = np.zeros(n_samples)

    balafon_scale = [220.00, 246.94, 277.18, 329.63, 370.00, 440.00]
    samples_per_note = n_samples // 16

    for i in range(16):
        if i % 3 != 0:
            freq = balafon_scale[(i * 2) % len(balafon_scale)]
            start = i * samples_per_note
            end = (i + 1) * samples_per_note
            t_note = t[start:end] - t[start]
            wave = np.sin(2 * np.pi * freq * t_note)
            env = np.exp(-t_note * 10)
            track[start:end] += wave * env * 5500

    sub_beat = int(beat_duration * sample_rate // 4)
    for step in range(64):
        idx = step * sub_beat
        if idx < n_samples:
            length = min(sub_beat, n_samples - idx)
            t_perc = np.linspace(0, length / sample_rate, length, False)
            
            if step % 8 in [0, 3]:
                djembe = np.sin(2 * np.pi * np.linspace(130, 50, length) * t_perc) * np.exp(-t_perc * 14)
                track[idx:idx+length] += djembe * 9000
            elif step % 4 in [1, 2]:
                slap = np.random.uniform(-1, 1, length) * np.exp(-t_perc * 30)
                track[idx:idx+length] += slap * 6000

    return create_sound_from_array(track.astype(np.int16))


# Chargement des effets et musiques
sound_laser = generate_laser_sound()
sound_explosion = generate_explosion_sound()
sound_powerup = generate_powerup_sound()
sound_gameover = generate_gameover_sound()

playlist = [
    generate_rock_loop(),
    generate_rnb_loop(),
    generate_chinese_loop(),
    generate_indian_loop(),
    generate_african_loop()
]

music_channel = pygame.mixer.Channel(0)


# --- DESSINS VECTORIELS DYNAMIQUES ---

def create_plane_surface():
    surface = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.polygon(surface, BLUE, [(25, 0), (15, 40), (35, 40)])
    pygame.draw.polygon(surface, DARK_BLUE, [(25, 15), (0, 35), (50, 35)])
    pygame.draw.ellipse(surface, WHITE, (20, 10, 10, 15))
    return surface

def generate_obstacle_images():
    images = []

    asteroid = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.polygon(asteroid, (120, 110, 100), [(10, 0), (30, 5), (40, 20), (30, 38), (10, 35), (0, 20)])
    pygame.draw.circle(asteroid, (80, 70, 60), (15, 15), 5)
    pygame.draw.circle(asteroid, (80, 70, 60), (28, 25), 4)
    images.append(asteroid)

    missile = pygame.Surface((20, 45), pygame.SRCALPHA)
    pygame.draw.polygon(missile, RED, [(10, 0), (0, 15), (0, 40), (20, 40), (20, 15)])
    pygame.draw.polygon(missile, ORANGE, [(5, 40), (10, 45), (15, 40)])
    images.append(missile)

    mine = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(mine, (50, 50, 50), (20, 20), 12)
    for angle_pos in [(20, 2), (20, 38), (2, 20), (38, 20), (7, 7), (33, 33), (7, 33), (33, 7)]:
        pygame.draw.line(mine, RED, (20, 20), angle_pos, 3)
    images.append(mine)

    return images


# --- FONDS D'ÉCRAN HAUTEMENT DISTINCTIFS ---

def create_themed_background(theme_index):
    bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    # 0: ROCK - Feu / Enfer rouge & noir
    if theme_index == 0:
        bg.fill((20, 5, 5))
        for _ in range(60):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(2, 5)
            pygame.draw.circle(bg, (255, random.randint(50, 150), 0), (x, y), size)
        # Nébuleuse magma
        for _ in range(8):
            cx, cy = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
            r = random.randint(100, 200)
            s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (220, 30, 10, 35), (r, r), r)
            bg.blit(s, (cx - r, cy - r))
        # Flammes en bas
        for x in range(0, SCREEN_WIDTH, 20):
            h = random.randint(40, 90)
            pygame.draw.polygon(bg, (255, 80, 0), [(x, SCREEN_HEIGHT), (x + 10, SCREEN_HEIGHT - h), (x + 20, SCREEN_HEIGHT)])

    # 1: RNB - Néon / Synthwave mauve et cyan
    elif theme_index == 1:
        bg.fill((15, 5, 30))
        # Étoiles brillantes
        for _ in range(80):
            x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
            color = CYAN if random.random() > 0.5 else (255, 100, 255)
            pygame.draw.circle(bg, color, (x, y), random.randint(1, 3))
        # Grille Néon
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(bg, (80, 20, 120), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(bg, (80, 20, 120), (0, y), (SCREEN_WIDTH, y), 1)

    # 2: CHINOIS - Rouge Impérial & Doré
    elif theme_index == 2:
        bg.fill((80, 10, 15))
        # Particules dorées
        for _ in range(100):
            x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
            pygame.draw.circle(bg, (255, 215, 0), (x, y), random.randint(1, 4))
        # Montagnes stylisées en bas
        points = [(0, SCREEN_HEIGHT)]
        for x in range(0, SCREEN_WIDTH + 100, 100):
            points.append((x, SCREEN_HEIGHT - random.randint(80, 160)))
        points.append((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.polygon(bg, (40, 5, 8), points)

    # 3: INDIEN - Safran, Ambre & Mandalas
    elif theme_index == 3:
        # Dégradé safran
        for y in range(SCREEN_HEIGHT):
            r = int(120 + (y / SCREEN_HEIGHT) * 80)
            g = int(40 + (y / SCREEN_HEIGHT) * 40)
            bg.fill((r, g, 10), (0, y, SCREEN_WIDTH, 1))
        # Poussière d'or
        for _ in range(90):
            x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
            pygame.draw.circle(bg, (255, 230, 150), (x, y), random.randint(1, 3))
        # Motifs circulaires (Mandalas en filigrane)
        for cx, cy in [(150, 150), (650, 450)]:
            for rad in range(30, 120, 20):
                s = pygame.Surface((rad*2, rad*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 255, 200, 25), (rad, rad), rad, 2)
                bg.blit(s, (cx - rad, cy - rad))

    # 4: AFRICAIN - Savane / Coucher de soleil
    else:
        # Dégradé coucher de soleil
        for y in range(SCREEN_HEIGHT):
            r = int(220 - (y / SCREEN_HEIGHT) * 120)
            g = int(100 - (y / SCREEN_HEIGHT) * 80)
            bg.fill((r, g, 20), (0, y, SCREEN_WIDTH, 1))
        # Grand Soleil
        s = pygame.Surface((180, 180), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 220, 100, 120), (90, 90), 90)
        bg.blit(s, (SCREEN_WIDTH // 2 - 90, 180))
        # Silhouette d'Acacia / Arbres
        pygame.draw.rect(bg, (20, 10, 5), (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        for x_pos in [150, 600]:
            pygame.draw.rect(bg, (20, 10, 5), (x_pos, SCREEN_HEIGHT - 120, 15, 70))
            pygame.draw.ellipse(bg, (20, 10, 5), (x_pos - 50, SCREEN_HEIGHT - 140, 115, 30))

    return bg


# --- CLASSES ---

class ScrollingBackground:
    def __init__(self, bg_image, speed=3):
        self.set_image(bg_image)
        self.speed = speed
        self.y1 = 0
        self.y2 = -SCREEN_HEIGHT

    def set_image(self, new_bg_image):
        self.bg_image = new_bg_image

    def update(self):
        self.y1 += self.speed
        self.y2 += self.speed
        if self.y1 >= SCREEN_HEIGHT:
            self.y1 = -SCREEN_HEIGHT
        if self.y2 >= SCREEN_HEIGHT:
            self.y2 = -SCREEN_HEIGHT

    def draw(self, surface):
        surface.blit(self.bg_image, (0, self.y1))
        surface.blit(self.bg_image, (0, self.y2))

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x=0, speed_y=-12):
        super().__init__()
        self.image = pygame.Surface((6, 20), pygame.SRCALPHA)
        self.image.fill(CYAN)
        pygame.draw.rect(self.image, WHITE, (1, 2, 4, 16))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["HEALTH", "TRIPLE"])
        self.image = pygame.Surface((26, 26), pygame.SRCALPHA)
        
        color = GREEN if self.type == "HEALTH" else YELLOW
        pygame.draw.circle(self.image, color, (13, 13), 12)
        pygame.draw.circle(self.image, WHITE, (13, 13), 12, 2)

        if self.type == "HEALTH":
            pygame.draw.line(self.image, WHITE, (13, 7), (13, 19), 3)
            pygame.draw.line(self.image, WHITE, (7, 13), (19, 13), 3)
        else:
            pygame.draw.polygon(self.image, WHITE, [(10, 6), (16, 6), (13, 19)])

        self.rect = self.image.get_rect(center=(random.randint(30, SCREEN_WIDTH - 30), -30))
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = random.randint(3, 7)
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        color = random.choice([RED, YELLOW, ORANGE])
        pygame.draw.circle(self.image, color, (self.size, self.size), self.size)
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.lifetime = random.randint(15, 30)

    def update(self):
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, lasers_group, all_sprites):
        super().__init__()
        self.image = create_plane_surface()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.speed = 6
        self.hp = 3
        self.lasers_group = lasers_group
        self.all_sprites = all_sprites
        self.last_shot_time = 0
        self.shoot_cooldown = 150
        self.triple_shot_until = 0

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            if current_time < self.triple_shot_until:
                l1 = Laser(self.rect.centerx, self.rect.top, speed_x=0, speed_y=-12)
                l2 = Laser(self.rect.left, self.rect.top + 10, speed_x=-3, speed_y=-11)
                l3 = Laser(self.rect.right, self.rect.top + 10, speed_x=3, speed_y=-11)
                self.lasers_group.add(l1, l2, l3)
                self.all_sprites.add(l1, l2, l3)
            else:
                l_left = Laser(self.rect.left + 8, self.rect.top + 15)
                l_right = Laser(self.rect.right - 8, self.rect.top + 15)
                self.lasers_group.add(l_left, l_right)
                self.all_sprites.add(l_left, l_right)
            
            sound_laser.play()
            self.last_shot_time = current_time

    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0:
            self.rect.y -= self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_SPACE]:
            self.shoot()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_images):
        super().__init__()
        self.obstacle_images = obstacle_images
        self.reset_obstacle()

    def reset_obstacle(self):
        self.image = random.choice(self.obstacle_images)
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH - 20), random.randint(-150, -30)))
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_obstacle()

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.high_score = 0
        self.app_running = True
        
        self.obstacle_images = generate_obstacle_images()
        
        # Pré-génération des fonds d'écran très distincts
        self.bg_surfaces = [create_themed_background(i) for i in range(len(playlist))]
        self.background = ScrollingBackground(self.bg_surfaces[0], speed=4)
        
        self.reset_game()

    def create_explosion(self, x, y):
        sound_explosion.play()
        for _ in range(20):
            particle = Particle(x, y)
            self.all_sprites.add(particle)

    def play_current_music(self):
        sound = playlist[self.current_music_index]
        music_channel.play(sound, loops=-1)

    def reset_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.all_obstacles = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        
        self.player = Player(self.lasers, self.all_sprites)
        self.all_sprites.add(self.player)
        
        for _ in range(7):
            obstacle = Obstacle(self.obstacle_images)
            self.all_sprites.add(obstacle)
            self.all_obstacles.add(obstacle)

        self.score = 0
        self.current_music_index = 0
        self.background.set_image(self.bg_surfaces[0])
        self.destroyed_count = 0
        self.start_time = time.time()
        self.last_powerup_time = time.time()
        self.game_over = False

        self.play_current_music()

    def run(self):
        while self.app_running:
            self.clock.tick(60)
            self.handle_events()

            if not self.game_over:
                self.update()
                self.draw()
            else:
                self.draw_summary()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app_running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_over and event.key in (pygame.K_SPACE, pygame.K_r):
                    self.reset_game()

    def update(self):
        self.background.update()
        self.all_sprites.update()
        
        # Génération de bonus
        if time.time() - self.last_powerup_time > 8:
            if random.random() < 0.7:
                powerup = PowerUp()
                self.powerups.add(powerup)
                self.all_sprites.add(powerup)
            self.last_powerup_time = time.time()

        # Lasers vs Obstacles
        hits = pygame.sprite.groupcollide(self.all_obstacles, self.lasers, True, True)
        for obstacle in hits:
            self.create_explosion(obstacle.rect.centerx, obstacle.rect.centery)
            self.destroyed_count += 1
            new_obstacle = Obstacle(self.obstacle_images)
            self.all_sprites.add(new_obstacle)
            self.all_obstacles.add(new_obstacle)

        # Joueur vs Bonus
        powerup_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for p in powerup_hits:
            sound_powerup.play()
            if p.type == "HEALTH":
                self.player.hp = min(3, self.player.hp + 1)
            elif p.type == "TRIPLE":
                self.player.triple_shot_until = pygame.time.get_ticks() + 6000

        # Joueur vs Obstacle
        obstacle_hits = pygame.sprite.spritecollide(self.player, self.all_obstacles, True)
        for obstacle in obstacle_hits:
            self.create_explosion(obstacle.rect.centerx, obstacle.rect.centery)
            self.player.hp -= 1
            new_obstacle = Obstacle(self.obstacle_images)
            self.all_sprites.add(new_obstacle)
            self.all_obstacles.add(new_obstacle)

            if self.player.hp <= 0:
                music_channel.stop()
                sound_gameover.play()
                self.game_over = True
                if self.score > self.high_score:
                    self.high_score = self.score

        # Calcul du score
        time_elapsed = int(time.time() - self.start_time)
        self.score = time_elapsed * 10 + self.destroyed_count * 50

        # Changement de musique ET d'arrière-plan tous les 2 000 points
        target_music_index = (self.score // 2000) % len(playlist)
        if target_music_index != self.current_music_index:
            self.current_music_index = target_music_index
            self.play_current_music()
            self.background.set_image(self.bg_surfaces[self.current_music_index])

    def draw(self):
        self.background.draw(screen)
        self.all_sprites.draw(screen)

        score_text = font_small.render(f"Score: {self.score}", True, WHITE)
        destroyed_text = font_small.render(f"Destructions: {self.destroyed_count}", True, CYAN)
        hp_text = font_small.render(f"Vie: {'♥ ' * self.player.hp}", True, RED)

        screen.blit(score_text, (10, 10))
        screen.blit(destroyed_text, (10, 45))
        screen.blit(hp_text, (SCREEN_WIDTH - 150, 10))

        # Indicateur visuel du bonus Triple Tir
        if pygame.time.get_ticks() < self.player.triple_shot_until:
            triple_text = font_small.render("TRIPLE TIR ACTIVE!", True, YELLOW)
            screen.blit(triple_text, (SCREEN_WIDTH // 2 - triple_text.get_width() // 2, 10))

        pygame.display.flip()

    def draw_summary(self):
        screen.fill(DARK_BLUE)

        title_text = font_large.render("GAME OVER", True, RED)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        score_text = font_small.render(f"Score final : {self.score}", True, WHITE)
        destroyed_text = font_small.render(f"Obstacles detruits : {self.destroyed_count}", True, CYAN)
        high_score_text = font_small.render(f"Meilleur score : {self.high_score}", True, WHITE)

        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 210))
        screen.blit(destroyed_text, (SCREEN_WIDTH // 2 - destroyed_text.get_width() // 2, 260))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 310))

        restart_text = font_small.render("Appuyez sur ESPACE ou R pour rejouer", True, GRAY)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 420))

        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()