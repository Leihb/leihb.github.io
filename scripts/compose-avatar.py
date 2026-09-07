#!/usr/bin/env python3
"""把精灵图里的人物抠出来贴到一张场景背景上，生成头像（仅依赖 Pillow）。

用法: python3 scripts/compose-avatar.py <背景.png> <精灵图.png> <格子: tl|tr|bl|br> <输出.png>

- 背景是单独文生图的无人场景（提示词见 design/paper-journey-prompts/avatar-bg.txt）
- 人物取精灵图指定格子，只保留最大的连通块（去掉相邻格子渗进来的碎纸），并抹掉残余洋红
- 人物按画面高度 74% 缩放，靠右下放置
"""
import sys
from collections import deque
from PIL import Image

def main(bg_path, sheet_path, which, out_path):
    bg = Image.open(bg_path).convert("RGBA")
    sheet = Image.open(sheet_path).convert("RGBA")
    cell = sheet.width // 2
    ox, oy = {"tl": (0, 0), "tr": (cell, 0), "bl": (0, cell), "br": (cell, cell)}[which]
    fr = sheet.crop((ox, oy, ox + cell, oy + cell))
    w, h = fr.size; px = fr.load()
    seen = bytearray(w * h); best = []
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if seen[i] or px[x, y][3] <= 8: continue
            comp = []; dq = deque([(x, y)]); seen[i] = 1
            while dq:
                cx, cy = dq.popleft(); comp.append((cx, cy))
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < w and 0 <= ny < h:
                        j = ny * w + nx
                        if not seen[j] and px[nx, ny][3] > 8: seen[j] = 1; dq.append((nx, ny))
            if len(comp) > len(best): best = comp
    keep = set(best)
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if not a: continue
            if (x, y) not in keep: px[x, y] = (0, 0, 0, 0); continue
            ex = max(0, min(r, b) - g)
            if ex: px[x, y] = (r - ex, g, b - ex, a)
    fr = fr.crop(fr.getbbox())
    target_h = int(bg.height * 0.74); scale = target_h / fr.height
    fr = fr.resize((int(fr.width * scale), target_h), Image.LANCZOS)
    out = bg.copy()
    out.alpha_composite(fr, (bg.width - fr.width - int(bg.width * 0.03), bg.height - fr.height - int(bg.height * 0.02)))
    out.convert("RGB").save(out_path, optimize=True)
    print("wrote", out_path)

if __name__ == "__main__":
    main(*sys.argv[1:5])
