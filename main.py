import sys
import pygame


pygame.init()


GENISLIK = 800
YUKSEKLIK = 600
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("SinglePlayer Pong")


SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)


saat = pygame.time.Clock()


RAKET_GENISLIK = 15
RAKET_YUKSEKLIK = 100
raket_x = 30
raket_y = YUKSEKLIK // 2 - RAKET_YUKSEKLIK // 2
raket_hizi = 7


TOP_BOYUT = 15
top_x = GENISLIK // 2
top_y = YUKSEKLIK // 2
BASLANGIC_HIZI = 5
top_hizi_x = BASLANGIC_HIZI
top_hizi_y = BASLANGIC_HIZI
HIZLANMA_ORANI = 1.08  


skor = 0
font = pygame.font.SysFont("Arial", 36)
oyun_bitti_font = pygame.font.SysFont("Arial", 48)

oyun_bitti = False


while True:
    for etkinlik in pygame.event.get():
        if etkinlik.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

      
        if oyun_bitti and etkinlik.type == pygame.KEYDOWN:
            if etkinlik.key == pygame.K_r:
                oyun_bitti = False
                skor = 0
                top_x = GENISLIK // 2
                top_y = YUKSEKLIK // 2
                top_hizi_x = BASLANGIC_HIZI
                top_hizi_y = BASLANGIC_HIZI

    if not oyun_bitti:
        
        tuslar = pygame.key.get_pressed()
        if (tuslar[pygame.K_UP] or tuslar[pygame.K_w]) and raket_y > 0:
            raket_y -= raket_hizi
        if (
            tuslar[pygame.K_DOWN] or tuslar[pygame.K_s]
        ) and raket_y < YUKSEKLIK - RAKET_YUKSEKLIK:
            raket_y += raket_hizi

        
        top_x += top_hizi_x
        top_y += top_hizi_y

        
        if top_y <= 0 or top_y >= YUKSEKLIK - TOP_BOYUT:
            top_hizi_y *= -1

        
        if top_x >= GENISLIK - TOP_BOYUT:
            top_hizi_x *= -1

        
        raket_kutusu = pygame.Rect(
            raket_x, raket_y, RAKET_GENISLIK, RAKET_YUKSEKLIK
        )
        top_kutusu = pygame.Rect(top_x, top_y, TOP_BOYUT, TOP_BOYUT)

        if top_kutusu.colliderect(raket_kutusu) and top_hizi_x < 0:
            top_hizi_x *= -1

           
            top_hizi_x *= HIZLANMA_ORANI
            top_hizi_y *= HIZLANMA_ORANI

           
            skor += 1

       
        if top_x < 0:
            oyun_bitti = True

   
    ekran.fill(SIYAH)

    
    pygame.draw.rect(
        ekran, BEYAZ, (raket_x, raket_y, RAKET_GENISLIK, RAKET_YUKSEKLIK)
    )
    pygame.draw.ellipse(ekran, BEYAZ, (top_x, top_y, TOP_BOYUT, TOP_BOYUT))

    
    skor_yazisi = font.render(f"Score: {skor}", True, BEYAZ)
    ekran.blit(skor_yazisi, (GENISLIK // 2 - 50, 20))

    
    if oyun_bitti:
        mesaj1 = oyun_bitti_font.render("GAME OVER!", True, BEYAZ)
        mesaj2 = font.render("FOR RESTART PRESS 'R'", True, BEYAZ)
        ekran.blit(
            mesaj1, (GENISLIK // 2 - 130, YUKSEKLIK // 2 - 50)
        )
        ekran.blit(
            mesaj2, (GENISLIK // 2 - 180, YUKSEKLIK // 2 + 10)
        )

    pygame.display.flip()
    saat.tick(60)
