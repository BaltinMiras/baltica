import pygame
import sys
import os
from datetime import datetime
from tools import flood_fill

pygame.init()
W, H, BAR = 1100, 750, 100
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("TSIS 2 Paint")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 17)
small = pygame.font.SysFont("arial", 13)
text_font = pygame.font.SysFont("arial", 24)
WHITE, BLACK = (255,255,255), (0,0,0)
canvas = pygame.Surface((W, H-BAR))
canvas.fill(WHITE)
palette = [BLACK,(128,128,128),(220,220,220),WHITE,(255,0,0),(255,128,0),(255,255,0),(0,180,0),(0,120,255),(0,0,180),(128,0,180),(255,105,180),(139,69,19),(0,200,200),(120,80,40),(255,220,180)]
tools = [("Pencil","pencil"),("Line","line"),("Rect","rectangle"),("Circle","circle"),("Square","square"),("Right Tri","right_triangle"),("Triangle","triangle"),("Rhombus","rhombus"),("Fill","fill"),("Text","text"),("Eraser","eraser"),("Picker","picker")]
active, color, sizes, size_index = "pencil", BLACK, [2,5,10], 1
drawing, start, last, end = False, None, None, None
typing, typed, text_pos = False, "", None

def draw_toolbar():
    screen.fill((225,225,225), (0,0,W,BAR))
    for i,(label,name) in enumerate(tools):
        r = pygame.Rect(7+i*90,8,84,30)
        pygame.draw.rect(screen,(170,205,245) if active==name else (250,250,250),r)
        pygame.draw.rect(screen,BLACK,r,1)
        screen.blit(small.render(label,True,BLACK),(r.x+5,r.y+8))
    screen.blit(font.render("Size:",True,BLACK),(8,52))
    for i,s in enumerate(sizes):
        r=pygame.Rect(60+i*54,48,48,27)
        pygame.draw.rect(screen,(170,205,245) if size_index==i else WHITE,r)
        pygame.draw.rect(screen,BLACK,r,1)
        screen.blit(small.render(f"{s}px",True,BLACK),(r.x+12,r.y+7))
    screen.blit(font.render("Colors:",True,BLACK),(235,52))
    for i,c in enumerate(palette):
        r=pygame.Rect(300+i*29,48,23,27)
        pygame.draw.rect(screen,c,r)
        pygame.draw.rect(screen,BLACK,r,1)
        if c==color: pygame.draw.rect(screen,(0,100,255),r,3)
    screen.blit(small.render("1/2/3 sizes | Ctrl+S save | Enter confirm text | Esc cancel",True,BLACK),(790,55))

def shape(tool,a,b):
    x1,y1=a; x2,y2=b
    l,t=min(x1,x2),min(y1,y2)
    w,h=abs(x2-x1),abs(y2-y1)
    if tool=="rectangle": return pygame.Rect(l,t,w,h)
    if tool=="square":
        side=max(w,h)
        xx=x1+side*(1 if x2>=x1 else -1)
        yy=y1+side*(1 if y2>=y1 else -1)
        return pygame.Rect(min(x1,xx),min(y1,yy),abs(xx-x1),abs(yy-y1))
    if tool=="circle": return (l,t,w,h)
    if tool=="right_triangle": return [(x1,y1),(x1,y2),(x2,y2)]
    if tool=="triangle": return [((x1+x2)//2,y1),(x1,y2),(x2,y2)]
    if tool=="rhombus": return [((x1+x2)//2,y1),(x2,(y1+y2)//2),((x1+x2)//2,y2),(x1,(y1+y2)//2)]

def draw_shape(surf,tool,a,b,c,width):
    if tool=="line": pygame.draw.line(surf,c,a,b,width)
    elif tool in ("rectangle","square"): pygame.draw.rect(surf,c,shape(tool,a,b),width)
    elif tool=="circle":
        x,y,w,h=shape(tool,a,b)
        if w and h: pygame.draw.ellipse(surf,c,(x,y,w,h),width)
    elif tool in ("right_triangle","triangle","rhombus"):
        pygame.draw.polygon(surf,c,shape(tool,a,b),width)

def save():
    os.makedirs("saves",exist_ok=True)
    name=datetime.now().strftime("saves/paint_%Y%m%d_%H%M%S_%f.png")
    pygame.image.save(canvas,name)
    print("Saved:",name)

running=True
while running:
    draw_toolbar()
    screen.blit(canvas,(0,BAR))
    if drawing and start and end and active not in ("pencil","eraser"):
        preview=canvas.copy()
        draw_shape(preview,active,start,end,color,sizes[size_index])
        screen.blit(preview,(0,BAR))
    if typing and text_pos is not None:
        screen.blit(text_font.render(typed,True,color),(text_pos[0],text_pos[1]+BAR))
    for e in pygame.event.get():
        if e.type==pygame.QUIT: running=False
        elif e.type==pygame.KEYDOWN:
            if typing:
                if e.key==pygame.K_RETURN:
                    if typed: canvas.blit(text_font.render(typed,True,color),text_pos)
                    typing=False; typed=""; text_pos=None
                elif e.key==pygame.K_ESCAPE: typing=False; typed=""; text_pos=None
                elif e.key==pygame.K_BACKSPACE: typed=typed[:-1]
                elif e.unicode and e.unicode.isprintable(): typed+=e.unicode
            else:
                if e.key in (pygame.K_1,pygame.K_2,pygame.K_3): size_index=int(e.unicode)-1
                elif e.key==pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL: save()
                elif e.key==pygame.K_ESCAPE: drawing=False; start=None
        elif e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
            mx,my=e.pos
            if my<BAR:
                for i,(_,name) in enumerate(tools):
                    if pygame.Rect(7+i*90,8,84,30).collidepoint(e.pos): active=name
                for i in range(3):
                    if pygame.Rect(60+i*54,48,48,27).collidepoint(e.pos): size_index=i
                for i,c in enumerate(palette):
                    if pygame.Rect(300+i*29,48,23,27).collidepoint(e.pos): color=c
            else:
                p=(mx,my-BAR)
                if active=="text": typing=True; typed=""; text_pos=p
                elif active=="picker":
                    if 0<=p[0]<W and 0<=p[1]<H-BAR: color=canvas.get_at(p)[:3]
                elif active=="fill": flood_fill(canvas,p,color)
                else:
                    drawing=True; start=p; last=p; end=p
                    if active in ("pencil","eraser"):
                        pygame.draw.circle(canvas,color if active=="pencil" else WHITE,p,max(1,sizes[size_index]//2))
        elif e.type==pygame.MOUSEMOTION and drawing:
            p=(e.pos[0],e.pos[1]-BAR); end=p
            if active in ("pencil","eraser"):
                pygame.draw.line(canvas,color if active=="pencil" else WHITE,last,p,sizes[size_index])
                last=p
        elif e.type==pygame.MOUSEBUTTONUP and e.button==1 and drawing:
            p=(e.pos[0],e.pos[1]-BAR)
            if active not in ("pencil","eraser"): draw_shape(canvas,active,start,p,color,sizes[size_index])
            drawing=False; start=None; last=None; end=None
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()
