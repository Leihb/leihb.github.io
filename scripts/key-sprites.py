#!/usr/bin/env python3
"""把文生图产出的洋红/粉底 2x2 精灵图抠成透明底 RGBA PNG（仅依赖 Pillow）。

用法: python3 scripts/key-sprites.py <in.png> <out.png>

背景色不假设是纯 #FF00FF：取四角像素的中位色当背景，按色距平方做软抠图，
再在半透明边缘把粉色溢色去掉（R/B 超过 G 的部分压回去）。
"""
import sys
from statistics import median
from PIL import Image, ImageMath

def ev(expr, **kw):
    """Pillow 12 去掉了 ImageMath.eval，用 lambda_eval 代替。"""
    return ImageMath.lambda_eval(lambda a: eval(expr, {"min": a["min"], "max": a["max"]}, a), **kw)


SOFT, HARD = 28, 70  # 色距阈值：<=SOFT 全透明，>=HARD 全保留

def key(src, dst):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    corners = [im.getpixel(p) for p in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
    bg = tuple(int(median(c[i] for c in corners)) for i in range(3))
    r, g, b = im.split()
    br, bgc, bb = bg
    d2 = ev("(r-br)*(r-br)+(g-bg)*(g-bg)+(b-bb)*(b-bb)",
                        r=r.convert("I"), g=g.convert("I"), b=b.convert("I"), br=br, bg=bgc, bb=bb)
    s2, h2 = SOFT * SOFT, HARD * HARD
    alpha = ev("min(max((d - s2) * 255 / (h2 - s2), 0), 255)", d=d2, s2=s2, h2=h2).convert("L")
    # 去粉色溢色：只在 0<alpha<255 的边缘处理
    excess = ev("max(min(r, b) - g, 0)", r=r.convert("I"), g=g.convert("I"), b=b.convert("I"))
    edge = ev("(a > 0) & (a < 255)", a=alpha.convert("I"))
    r2 = ev("r - e * m", r=r.convert("I"), e=excess, m=edge).convert("L")
    b2 = ev("b - e * m", b=b.convert("I"), e=excess, m=edge).convert("L")
    out = Image.merge("RGBA", (r2, g, b2, alpha))
    # 网站加载器把每格归一化到 512px，源图 1024 足够，体积省一半以上
    if out.width > 1024:
        out = out.resize((1024, 1024), Image.LANCZOS)
    out.save(dst, optimize=True)
    kept = sum(1 for v in alpha.get_flattened_data() if v) / (w * h)
    print(f"{dst}: bg={bg} kept={kept:.1%}")

if __name__ == "__main__":
    key(sys.argv[1], sys.argv[2])
