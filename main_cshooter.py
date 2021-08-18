## import semua module yang diperlukan
import pygame, random
from os import path

## Definisi variabel untuk lokasi folder gambar dan folder suara
img_dir = path.join(path.dirname(__file__), 'assets')
sound_folder = path.join(path.dirname(__file__), 'sounds')

## Definisi variabel untuk lebar dan tinggi layar
WIDTH = 480
HEIGHT = 600

## Definisi variabel untuk pengaturan frame untuk kebutuhan loop game
FPS = 60 #FPS=Frame Per Second

## Definisi variabel untuk lama waktu kekuatan level tembakan akan bertahan
POWERUP_TIME = 4000

## Definisi variabel untuk ukuran bar penanda sisa shield
BAR_LENGTH = 100
BAR_HEIGHT = 10

## Definisi warna berdasarkan triplet RGB
DARK_BLUE=(9,20,60)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#################################### INISIASI ################################
pygame.init() # Inisiasi pygame
pygame.mixer.init() #inisiasi sound
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Mengatur ukuran layar
pygame.display.set_caption("C - SHOOTER") #Mengatur caption sesuai nama game
clock = pygame.time.Clock()  # Untuk mengatur time sesuai FPS
font_name = pygame.font.match_font('arial') #Choose font berdasarkan nama font terdekat

def main_menu():
    global screen
    ## Pengaturan suara
    menu_song = pygame.mixer.music.load(path.join(sound_folder, "menu.ogg")) #load suara
    pygame.mixer.music.play(-1) #-1 agar musik diputar secara berulang
    pygame.mixer.music.set_volume(0.3) #atur volume
    
    ## Pengaturan latar belakang gambar layar
    title = pygame.image.load(path.join(img_dir, "fight (1).png")).convert() #load gambar latar belakang
    title = pygame.transform.scale(title, (WIDTH, HEIGHT), screen) #scaling gambar sesuai ukuran layar
    screen.blit(title, (0, 0)) #flip gambar
    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN: #cek apakah ada tombol yang ditekan
            if ev.key == pygame.K_RETURN: #ketika tombol enter ditekan akan masuk ke layar get ready
                break
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
        elif ev.type == pygame.QUIT:
                pygame.quit()
                quit()

    ready = pygame.mixer.Sound(path.join(sound_folder, 'getready.ogg')) #load suara get ready
    ready.play() #memutar suara get ready
    screen.fill(DARK_BLUE) #mengatur warna layar
    draw_text(screen, "GET READY!!!", 40, WIDTH/2, HEIGHT*0.25) #menambah tulisan di layar
    draw_text(screen, "PRESS RIGHT AND LEFT ARROW KEYS TO MOVE", 20, WIDTH/2, HEIGHT*0.5)
    draw_text(screen, "PRESS SPACE TO SHOOT", 20, WIDTH/2, HEIGHT*0.6)
    pygame.display.update()


def draw_text(surf, text, size, x, y): #fungsi untuk membuat tulisan
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE) #True=anti-aliazed, warna tulisan: putih
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    pct = max(pct, 0) #shield tidak dapat bernilai<0
    fill = (pct / 100) * BAR_LENGTH #Mengatur panjang shield bar agar sesuai dengan sisa shield
    
    #perbaharui shield bar: indicator bar(fill) dan outline bar)
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT) #outline shield bar
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT) #indicator shield bar
    
    pygame.draw.rect(surf, GREEN, fill_rect) #warna hijau untuk indikator shield
    pygame.draw.rect(surf, WHITE, outline_rect, 2) #warna putih untuk outline shield bar (ketebalan 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives): #menggambar jumlah pesawat sesuai sisa nyawa (lives)
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i #mengatur jarak antar gambar pesawat
        img_rect.y = y
        surf.blit(img, img_rect)
        
def newvirus(): #fungsi untuk generate virus baru
    virus_element = virus()
    all_sprites.add(virus_element) #menambahkan virus dalam sprite group
    viruses.add(virus_element)

################################ DEFINISI KELAS ##############################

class ledakan(pygame.sprite.Sprite): #Ledakan dalam bentuk animasi/pergantian gambar
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = ledakan_anim[self.size][0] #Ambil image ke-0 dlm list sebagai gambar awal
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75 #Mengatur rate untuk keperluan animasi ledakan

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate: #Perubahan frame
            self.last_update = now
            self.frame += 1
            
            #Mengatur animasi ledakan
            if self.frame == len(ledakan_anim[self.size]): #apabila seluruh frame sudah ditampilkan, hapus ledakan
                self.kill()
            else:   #Pindah frame/gambar berikutnya
                center = self.rect.center #Atur pusat gambar agar konsisten (tidak berpindah posisi antar gambar)
                self.image = ledakan_anim[self.size][self.frame] 
                self.rect = self.image.get_rect()
                self.rect.center = center


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (70, 50)) #scaling gambar pesawat
        self.image.set_colorkey(BLACK) #menghilangkan bayangan hitam
        self.rect = self.image.get_rect()
        
        ## Mengatur circle dari player
        self.radius = 20
        #pygame.draw.circle(self.image,RED, self.rect.center,self.radius) #checking circle size
        
        ## Mengatur letak awal pesawat
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        
        
        ## Pengaturan awal pesawat
        self.speedx = 0 #mengatur agar objek diam saat tombol tidak ditekan
        
        self.shield = 100 #mengatur nilai awal shield, yaitu 100
        
        self.shoot_delay = 250 #jeda antar tembakan apabila tombol space terus ditekan
        self.last_shot = pygame.time.get_ticks()
        
        self.lives = 3 #Jumlah nyawa yang disediakan
        
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        
        self.power = 1 #Menetapkan kekuatan tembakan pada awal permainan
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        ## Penurunan kekuatan tembakan apabila waktu(POWER_TIME) habis
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        ## Memunculkan pesawat setelah nyawa baru digunakan
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0  #mengatur default speed agar objek pesawat diam saat tombol tidak ditekan

        ## Cek tombol yang ditekan oleh pemain game, dan disimpan dalam variabel keystate
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]: #jika panah kiri -> pergerakan ke sumbu negatif x
            self.speedx = -5
        elif keystate[pygame.K_RIGHT]: #jika panah kanan -> pergerakan ke sumbu positif x
            self.speedx = 5

        ## Memastikan pesawat tidak bergeser hingga keluar dari layar kiri / kanan
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
        #Menembak ketika tombol space ditekan
        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay: #memastikan jeda antar tembakan
            self.last_shot = now
            if self.power == 1: #kekuatan tembakan level 1: satu peluru
                bullet = Bullet(self.rect.centerx, self.rect.top) #atur arah datang peluru
                all_sprites.add(bullet)
                bullets.add(bullet)
                shooting_sound.play()
                
            if self.power == 2: #kekuatan tembakan level 2:dua peluru kanan dan kiri pesawat
                bullet1 = Bullet(self.rect.left, self.rect.centery) #atur arah datang peluru
                bullet2 = Bullet(self.rect.right, self.rect.centery) #atur arah datang peluru
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shooting_sound.play()
                
            if self.power >= 3: #dua peluru kanan dan kiri pesawat + misile/suntikan
                bullet1 = Bullet(self.rect.left, self.rect.centery) #arah datang peluru
                bullet2 = Bullet(self.rect.right, self.rect.centery) #arah datang peluru
                suntikan1 = suntikan(self.rect.centerx, self.rect.top) #arah datang suntikan
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(suntikan1)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(suntikan1)
                shooting_sound.play()
                suntikan_sound.play()

    def powerup(self):
        self.power += 1 #menambah kekuatan tembakan apabila pesawat mengenai simbol petir
        self.power_time = pygame.time.get_ticks()

    def hide(self): #pesawat disembunyikan setelah mengalami ledakan
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200) #disembunyikan di bawah layar

class virus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image= random.choice(virusc_images) #memilih secara acak gambar virus
        self.image.set_colorkey(BLACK) #menghapus bayangan hitam pada gambar virus
        self.rect = self.image.get_rect()
        
        ## Mengatur ukuran circle virus(berguna untuk deteksi tumbukan)
        self.radius = int(self.rect.width * .80 / 2)
        #pygame.draw.circle(self.image,RED, self.rect.center,self.radius) #checking circle size
        
        ## Menetapkan secara acak lokasi virus muncul (dalam bentuk koordinat x,y)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        
        ## Menentukan  secara acak kecepatan gerak virus (sumbu y)
        self.speedy = random.randrange(5, 20)

        ## Menentukan  secara acak kecepatan gerak virus (sumbu x)
        self.speedx = random.randrange(-3, 3)
        
        ## Note: karena kecepatan x dan y ditentukan, memungkinakan virus bergerak turun secara diagonal

    def update(self):       
        #Update posisi virus sesuai kecepatan yang telah ditentukan (x dan y)
        self.rect.x += self.speedx 
        self.rect.y += self.speedy
        
        #Ketika virus bergerak keluar dari salah satu 3 sisi layar (kanan, kiri, bawah)
        #virus akan dimunculkan kembali dengan koordinat posisi acak
        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8) #random kecepatan pergerakan virus


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'tbolt']) #memilih acak power yang dihasilkan (shield atau bolt)
        self.image = powerup_images[self.type] #ambil image dari dictionary (lihat bagian load gambar)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2 #kecepatan jatuh

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > HEIGHT: ## hapus ketika menyentuh layar bawah
            self.kill()


## defines the sprite for bullets
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        
        #Atur posisi keluarnya peluru
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10 #minus=bergerak ke atas

    def update(self):
        self.rect.y += self.speedy #bergerak lurus ke atas (speednya minus)
        
        ## hapus ketika peluru sudah menyentuh atas layar
        if self.rect.bottom < 0:
            self.kill()

class suntikan(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = suntikan_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        
        #Atur posisi keluarnya suntikan
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10 #minus=bergerak ke atas

    def update(self):        
        self.rect.y += self.speedy #bergerak lurus ke atas (speednya minus)
        
        ## hapus ketika peluru sudah menyentuh atas layar
        if self.rect.bottom < 0:
            self.kill()


################################ LOAD GAMBAR ################################

## Latar belakang utama game
background = pygame.image.load(path.join(img_dir, 'background1.png')).convert()
background_rect = background.get_rect()

## Pemain/Pesawat merah putih
player_img = pygame.image.load(path.join(img_dir, 'plane.png')).convert_alpha()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

## Tembakan/laser
bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()
bullet_img = pygame.transform.scale(bullet_img , (5,29 ))

## missile/suntikan
suntikan_img = pygame.image.load(path.join(img_dir, 'injection.png')).convert_alpha()
suntikan_img  = pygame.transform.scale(suntikan_img , (30, 80))

## virus
virusc_images = []
virusc_list = [
    'virus-1.png',
    'virus-2.png',
    'virus-3.png',
    'virus-4.png',
    'virus-5.png',
    'virus-6.png',
    'virus-7.png'
]
m=[0.8,1,1.2,1.3,1.4,1.5,1.6] #untuk scale ukuran virus agar bervariasi
i=0
for image in virusc_list:
    virusc_im=pygame.image.load(path.join(img_dir, image))
    virusc_im= pygame.transform.scale(virusc_im, (int(60*m[i]), int(55*m[i]))).convert_alpha()
    virusc_images.append( virusc_im)
    i=i+1

## ledakan
ledakan_anim = {} #disimpan dalam bentuk dictionary
ledakan_anim['lg'] = [] # untuk tumbukan peluru dengan virus (lg:large)
ledakan_anim['sm'] = [] #untuk tumbukan pesawat dengan virus (sm: small)
ledakan_anim['player'] = [] #untuk tumbukan yang menyebabkan pesawat hilang nyawa
for i in range(9):
    ## Load gambar ledakan "lg" dan s"m"
    filename = 'regularexplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    
    ## Penyesuaian ukuran ledakan
    img_lg = pygame.transform.scale(img, (75, 75)) #large/besar
    ledakan_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (40, 40)) #small/kecil
    ledakan_anim['sm'].append(img_sm)

    ## Load gambar ledakan untuk player
    filename = 'sonicexplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    ledakan_anim['player'].append(img)

## Power ups (shield dan thunder bolt)
powerup_images = {} #disimpan dalam bentuk dictionary
powerup_images['shield'] = pygame.image.load(
    path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['tbolt'] = pygame.image.load(
    path.join(img_dir, 'bolt_gold.png')).convert()

############################## LOAD SUARA ####################################
#tembakan
shooting_sound = pygame.mixer.Sound(path.join(sound_folder, 'pew.wav'))

#suntikan
suntikan_sound = pygame.mixer.Sound(path.join(sound_folder, 'rocket.ogg'))

#ledakan
expl_sounds = []
for sound in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(sound_folder, sound)))
    
#power-shield
shield_sound=pygame.mixer.Sound(path.join(sound_folder, 'pshield.wav'))

#power-thunderbolt
tbolt_sound=pygame.mixer.Sound(path.join(sound_folder, 'ppower.wav'))
    
#musik utama
musik_utama=pygame.mixer.Sound(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
musik_utama.set_volume(0.2)  # simmered the sound down a little

#die_sound
player_die_sound = pygame.mixer.Sound(path.join(sound_folder, 'rumble1.ogg'))

################################# GAME LOOP #################################
#Kondisi awal agar masuk ke loop
running = True
menu_display = True

#Start game loop
while running:
    if menu_display:
        main_menu()
        pygame.time.wait(3000)

        #Stop musik menu
        pygame.mixer.music.stop()
        
        #Mainkan musik utama dan putar ulang secara terus menerus
        pygame.mixer.music.load(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
        pygame.mixer.music.play(loops=-1)

        menu_display = False #agar tidak masuk if condition lagi pada iterasi berikutnya

        ## Pembentukan kelompok objek
        all_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        viruses = pygame.sprite.Group()
        
        ## Pembentukan objek (pesawat dan virus)
        player = Player()
        all_sprites.add(player)
        for i in range(8):  # Membuat 8 viruses
            newvirus() #lihat fungsi ini di bagian definisi fungsi

        ### skor awal
        score = 0

 ## Game loop bagian 1: Process input/events
    clock.tick(FPS)  # atur speed agar konsisten mengikuti definisi FPS
    
    #Melacak event
    for event in pygame.event.get():
        
        ## Jika menekan tombol silang di atas
        if event.type == pygame.QUIT:
            running = False

        ## Jika menekan tombol escape
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

 ## Game loop bagian 2: Update (respon program)
    all_sprites.update()

    # Jika virus bertumbukan dengan peluru maupun suntikan....
    # True: kedua objek dihilangkan ketika bertumbukan
    hits = pygame.sprite.groupcollide(viruses, bullets, True, True) 
    #Note:Karena virus hilang ketika bertumbukan dengan tembakan, maka perlu membentuk virus baru
    
    for hit in hits: 
        # Menambahkan skor berdasarkan ukuran virus yang berhasil dilenyapkan 
        #(semakin kecil virus, skor semakin banyak karena sulit ditembak)
        score += 50 - hit.radius  
        
        random.choice(expl_sounds).play() #memainkan suara ledakan
        expl = ledakan(hit.rect.center, 'lg') #memunculkan animasi ledakan large/ "lg"
        all_sprites.add(expl) #memasukkan objek ledakan dalam group
        
        # Jika virus ditembak, maka ada 10% kemungkinan shield/thunderbolt dihasilkan
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
            
        newvirus()  #membentuk virus secara acak sesuai dengan jumlah virus yang dihilangkan (karena tertembak)

    ## Jika pesawat bertumbukan dengan virus.....
    ## True: objek virus dihilangkan ketika bertumbukan
    hits = pygame.sprite.spritecollide(player, viruses, True, pygame.sprite.collide_circle)  
    for hit in hits:
        player.shield -= hit.radius * 2 #shield pesawat akan berkurang berdasarkan radius virus yang ditumbuk
        expl = ledakan(hit.rect.center, 'sm') #memunculkan animasi ledakan small/ "sm"
        all_sprites.add(expl)  #memasukkan objek ledakan dalam group
        newvirus() #membentuk virus secara acak sesuai dengan jumlah virus yang dihilangkan (karena bertumbukan)
        
        #Jika setelah dihantam virus, shield <0 ......
        if player.shield <= 0:
            player_die_sound.play() #memainkan suara (kehilangan 1 nyawa)
            death_ledakan = ledakan(player.rect.center, 'player') #memunculkan animasi ledakan(jenis:"player")
            all_sprites.add(death_ledakan) #memasukkan objek ledakan dalam group
            
            player.hide() #menyembunyikan gambar pesawat setelah pesawat meledak
            player.lives -= 1 #pesawat kehilangan 1 nyawa
            player.shield = 100 #shield untuk nyawa baru

    ## Jika pesawat bertumbukan dengan gambar shield maupun thunderbolt....
    hits = pygame.sprite.spritecollide(player, powerups, True) #True: shield /tblot lenyap setelah bertumbukan
    for hit in hits:
        if hit.type == 'shield':
            shield_sound.play() #memainkan suara untuk objek shield
            player.shield += random.randrange(10, 30) #menambahkan shield pesawat secara random (rentang 10-30)
            if player.shield >= 100: #membatasi jumlah shield menjadi maksimum 100
                player.shield = 100
        if hit.type == 'tbolt':
            tbolt_sound.play()
            player.powerup() #peningkatan level kekuatan tembakan

    ## Jika nyawa habis, dan animasi ledakan telah selesai, kembali ke menu awal
    if player.lives == 0 and not death_ledakan.alive():
       menu_display = True
       
 ## Game loop bagian 3: Draw
    #atur gambar latar belakang
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    
    #Menggambar semua kelompok objek
    all_sprites.draw(screen)
    
    #Menggambar skor
    draw_text(screen, ("Your Score: " + str(score)), 18, WIDTH / 2, 10)
    
    #Menggambar indikator shield dalam bentuk bar
    draw_shield_bar(screen, 5, 5, player.shield)

    #Menggambar jumlah nyawa (dalam bentuk pesawat)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)

    pygame.display.flip()

pygame.quit()
