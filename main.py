import pygame
import time

W = 800
H = 600

pygame.init()
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption("Biconvex lens simulator")

fps = 60
clock = pygame.time.Clock()

# lens image and position
lens_center = pygame.rect.Rect(390,200,1,200)
img1 = pygame.image.load("lens.png")

# points 
center_y = lens_center.h+100
focus = 100
image_height = 50
c1 = (90+focus,center_y)
f1 = (c1[0]+focus,center_y)
o = (f1[0]+focus,center_y)
f2 = (o[0]+focus,center_y)
c2 = (f2[0]+focus,center_y)

vel_x = 0.5
image = [100,center_y-image_height]
megnifacation = 0

def txt_screen(text,color,x,y):
    font = pygame.font.Font("font/AGENCYR.TTF", 32)
    screen_txt=font.render(text,True,color)
    screen.blit(screen_txt,[x,y])

# Function to find the intersection point
def find_intersection(p1, p2, p3, p4):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    
    # Line equations
    A1 = y2 - y1
    B1 = x1 - x2
    C1 = A1 * x1 + B1 * y1
    
    A2 = y4 - y3
    B2 = x3 - x4
    C2 = A2 * x3 + B2 * y3
    
    # Calculate determinant
    det = A1 * B2 - A2 * B1
    
    # Check if lines are parallel
    if det == 0:
        print("parallel")
        return None
    
    # Find intersection point
    x = (B2 * C1 - B1 * C2) / det
    y = (A1 * C2 - A2 * C1) / det
    
    # Check if intersection point lies within line segments
    if (min(x1, x2) <= x <= max(x1, x2) and
        min(y1, y2) <= y <= max(y1, y2) and
        min(x3, x4) <= x <= max(x3, x4) and
        min(y3, y4) <= y <= max(y3, y4)):
        return (int(x), int(y))
    else:
        return None

while True:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

    # start and end points of rays    
    ray1_start = image
    image_distance = lens_center.topleft[0] - ray1_start[0]
    x = 500
    r = image_distance/image_height
    y = (x/r)
    y1 = (focus/image_height)
    ray1_end = [o[0]+x,o[1]+y]
    ray2_start = image
    ray2_end = [image[0]+image_distance,image[1]]
    ray2_end2 = [f2[0]+x,f2[1]+(x/(y1))]
    ray2_end_virual = [ray2_end[0]-x,ray2_end[1]-x/(y1)]
    image_end_virtual = [image[0]-x,image[1]-x/(r)]
    megnifacation = None

    # controling image movement
    if r <=0.2:
        vel_x = -0.5
    if image[0] <= 0:
        vel_x = 0.5

    if image[0] == f1[0]:
        time.sleep(1)
    if image[0] == c1[0]:
        time.sleep(1)
    if image[0] == (c1[0]+f1[0])/2:
        time.sleep(1)
    if image[0] == (c1[0]-50):
        time.sleep(1)
   
    # moving image
    image[0]+=vel_x
    
    # text
    txt_screen("F","white",f1[0],f1[1])
    txt_screen("F","white",f2[0],f2[1])
    txt_screen("2F","white",c1[0],c1[1])
    txt_screen("2F","white",c2[0],c2[1])

    
    # image of lens
    screen.blit(img1,(lens_center[0]-25,lens_center[1]))
    
    # lense
    pygame.draw.rect(screen,"green",lens_center)
    
    # line of sight
    pygame.draw.line(screen,"yellow",(c1[0]-200,c1[1]),(c2[0]+200,c2[1]))

    # object
    pygame.draw.line(screen,"white",(image[0],center_y),image)
    
    # image
    inter_point = find_intersection(ray1_start,ray1_end,ray2_end,ray2_end2)
    if inter_point:
        height = inter_point[1] - center_y
        megnifacation = height/image_height
        pygame.draw.circle(screen,"red",inter_point,3)
        pygame.draw.line(screen,"white",(inter_point[0],center_y),inter_point)
    
    # points
    pygame.draw.circle(screen,"red",c1,3)
    pygame.draw.circle(screen,"red",c2,3)
    pygame.draw.circle(screen,"red",f1,3)
    pygame.draw.circle(screen,"red",f2,3)
    pygame.draw.circle(screen,"red",image,3)

    # rays
    pygame.draw.line(screen,"green",ray1_start,ray1_end)
    pygame.draw.line(screen,"green",ray2_start,ray2_end)
    pygame.draw.line(screen,"green",ray2_end,ray2_end2)
    
    # virtual image
    if image[0] > f1[0] :
        pygame.draw.line(screen,"green",ray2_end,ray2_end_virual)
        pygame.draw.line(screen,"green",image,image_end_virtual)
        inter_point_virtual = find_intersection(ray2_end,ray2_end_virual,image,image_end_virtual)
        if inter_point_virtual:
            height_virtual = center_y - inter_point_virtual[1]
            megnifacation = height_virtual/image_height
            pygame.draw.circle(screen,"red",inter_point_virtual,3)
            pygame.draw.line(screen,"white",(inter_point_virtual[0],center_y),inter_point_virtual)
        fps = 24

    if megnifacation:
        txt_screen(f"magnification = {megnifacation}","white",300,500)
    else:
        txt_screen("magnification = very high","white",300,500)
    
    pygame.display.update()
    clock.tick(fps)