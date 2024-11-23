import pygame, sys
from pygame.locals import *
import random
import time

# Kích thước cửa sổ
WINDOWWIDTH = 800
WINDOWHEIGHT = 500
pygame.init()

# Tạo cửa sổ game
w = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

# Load hình ảnh
BG = pygame.image.load('img_6.png')
BG = pygame.transform.scale(BG, (WINDOWWIDTH, WINDOWHEIGHT))
menu_BG = pygame.image.load('img_6.png')
menu_BG = pygame.transform.scale(menu_BG, (WINDOWWIDTH, WINDOWHEIGHT))

tao = pygame.image.load('img_4.png')
tao = pygame.transform.scale(tao, (40, 50))
cam = pygame.image.load('img_5.png')
cam = pygame.transform.scale(cam, (40, 50))
xoai = pygame.image.load('img_3.png')
xoai = pygame.transform.scale(xoai, (40, 50))
dua = pygame.image.load('img_2.png')
dua = pygame.transform.scale(dua, (40, 50))
chuoi = pygame.image.load('img_7.png')
chuoi = pygame.transform.scale(chuoi, (40, 50))

meo = pygame.image.load('img.png')
meo = pygame.transform.scale(meo, (50, 50))

meo1 = pygame.image.load('img_1.png')
meo1 = pygame.transform.scale(meo1, (50, 50))
meo2 = meo
FPS = 20
fpsClock = pygame.time.Clock()

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Biến lưu điểm số và cấp độ
diem = 0
level = 1  # Mặc định là Easy
target_score = 100  # Điểm cần đạt để qua cấp độ
max_time_for_promotion = 30  # Thời gian tối đa để tự động tăng cấp
max_level = 10  # Cấp độ cao nhất

# Hàm tạo nút
def draw_button(text, font, color, rect, surface):
    pygame.draw.rect(surface, color, rect)
    text_surface = font.render(text, True, WHITE)
    surface.blit(text_surface, (
        rect[0] + (rect[2] - text_surface.get_width()) // 2, rect[1] + (rect[3] - text_surface.get_height()) // 2))

# Hàm hiển thị giao diện chính
def main_menu():
    global level
    menu = True
    font = pygame.font.SysFont('Arial', 50)
    button_rect = pygame.Rect(WINDOWWIDTH // 2 - 100, WINDOWHEIGHT // 2 - 50, 200, 100)

    while menu:
        w.blit(menu_BG, (0, 0))
        draw_button('START', font, RED, button_rect, w)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    menu = False  # Thoát khỏi menu

        pygame.display.update()
        fpsClock.tick(FPS)

# Hàm khởi tạo vị trí và tốc độ ngẫu nhiên cho quả
def init_fruit(fruit_image):
    x_pos = random.randint(50, WINDOWWIDTH - 50)
    y_pos = random.randint(-100, -50)
    # Tốc độ tăng theo cấp độ
    speed = random.randint(5 + level * 2, 10 + level * 5)
    return {"image": fruit_image, "x": x_pos, "y": y_pos, "speed": speed}

# Khởi tạo danh sách các quả
def reset_fruits():
    return [init_fruit(tao), init_fruit(cam), init_fruit(xoai), init_fruit(dua), init_fruit(chuoi)]

# Hàm hiển thị GAME OVER
def show_message(message):
    font = pygame.font.SysFont('Arial', 50)
    text = font.render(message, True, RED)
    w.blit(text, (WINDOWWIDTH // 2 - text.get_width() // 2, WINDOWHEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(5000)  # Dừng lại 3 giây trước khi quay lại menu chính

# Hàm chính để chạy trò chơi
def game():
    global diem, meo2, level, target_score
    diem = 0  # Đặt lại điểm số
    meo2 = meo  # Đặt lại hình ảnh mặc định cho con mèo
    time0 = time.time()

    # Ẩn con trỏ chuột mặc định
    pygame.mouse.set_visible(False)

    # Khởi tạo lại danh sách quả
    fruits = reset_fruits()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                meo2 = meo1
                for fruit in fruits:
                    if fruit["x"] - 20 < event.pos[0] < fruit["x"] + 60 and fruit["y"] - 50 < event.pos[1] < fruit["y"] + 50:
                        diem += random.randint(5, 10)
                        fruit["y"] = random.randint(-100, -50)
                        fruit["x"] = random.randint(50, WINDOWWIDTH - 50)
            if event.type == pygame.MOUSEBUTTONUP:
                meo2 = meo

        w.blit(BG, (0, 0))

        # Di chuyển và vẽ các quả
        for fruit in fruits:
            fruit["y"] += fruit["speed"]
            w.blit(fruit["image"], (fruit["x"], fruit["y"]))
            if fruit["y"] > WINDOWHEIGHT:
                fruit["y"] = random.randint(-100, -50)
                fruit["x"] = random.randint(50, WINDOWWIDTH - 50)

        # Hiển thị hình ảnh con mèo tại vị trí chuột
        mouse_pos = pygame.mouse.get_pos()
        w.blit(meo2, (mouse_pos[0] - 25, mouse_pos[1] - 25))

        # Hiển thị thông tin level, điểm số và thời gian
        time1 = time.time()
        elapsed_time = int(time1 - time0)
        font = pygame.font.SysFont('Arial', 30)
        w.blit(font.render(f'Score: {diem}', True, RED), (50, 50))
        w.blit(font.render(f'Time: {elapsed_time}', True, RED), (50, 80))
        w.blit(font.render(f'Level: {level}', True, RED), (50, 110))

        # Tăng cấp nếu đạt điểm yêu cầu hoặc vượt qua giới hạn thời gian
        if diem >= target_score or (elapsed_time <= max_time_for_promotion and diem >= target_score):
            if level == max_level:
                pygame.mouse.set_visible(True)  # Hiện lại con trỏ chuột
                show_message("YOU WIN!")  # Hiển thị thông báo thắng
                return  # Quay lại menu chính
            level += 1
            target_score += 100  # Mục tiêu tăng thêm mỗi cấp
            fruits = reset_fruits()  # Làm mới danh sách quả

            pygame.time.wait(1000)  # Tạm dừng 1 giây để người chơi nhận biết

        # Kiểm tra điều kiện thua
        if elapsed_time >= 120 and diem < target_score:
            pygame.mouse.set_visible(True)  # Hiện lại con trỏ chuột trước khi thoát
            show_message("GAME OVER")
            return  # Trở về menu chính

        pygame.display.update()
        fpsClock.tick(FPS)

# Chạy chương trình
while True:
    main_menu()  # Hiển thị menu chính trước
    game()  # Sau khi nhấn nút START, trò chơi bắt đầu
