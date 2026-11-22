from collections import deque

def flood_fill(surface, start, fill_color):
    x, y = start
    width, height = surface.get_size()
    if not (0 <= x < width and 0 <= y < height):
        return
    target = surface.get_at((x, y))[:3]
    fill_color = tuple(fill_color[:3])
    if target == fill_color:
        return
    stack = [(x, y)]
    surface.set_at((x, y), fill_color)
    while stack:
        px, py = stack.pop()
        for nx, ny in ((px+1,py),(px-1,py),(px,py+1),(px,py-1)):
            if 0 <= nx < width and 0 <= ny < height and surface.get_at((nx,ny))[:3] == target:
                surface.set_at((nx,ny), fill_color)
                stack.append((nx,ny))
