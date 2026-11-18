#!/usr/bin/env python3
"""news-image-20261117 - sum up 17 November 2026 world news in one image.

Draws a 1024x1024 PNG newspaper front page, procedurally, with only the
Python standard library. No network, no files read, no randomness, no
timestamps: two runs produce byte-identical output.

Usage:  MAKEFUN_OUTPUT_DIR=/output python3 main.py
Writes entry.png into MAKEFUN_OUTPUT_DIR (default: ./output).
"""
import math
import os
import struct
import zlib

# ---------------------------------------------------------------- font (5x7)
FONT = {
    'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    'C': ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    'D': ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    'G': ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    'I': ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    'J': ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    'K': ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    'M': ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    'N': ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    'O': ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    'P': ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    'Q': ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    'R': ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    'U': ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    'V': ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    'W': ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    'X': ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    'Y': ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    'Z': ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    '0': ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    '1': ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    '2': ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    '3': ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    '4': ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    '5': ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    '6': ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    '7': ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    '8': ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    '9': ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    ' ': ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    '.': ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ',': ["00000", "00000", "00000", "00000", "01100", "00100", "01000"],
    "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
    '-': ["00000", "00000", "00000", "01110", "00000", "00000", "00000"],
    ':': ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    ';': ["00000", "01100", "01100", "00000", "01100", "00100", "01000"],
    '/': ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    '&': ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    '(': ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ')': ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    '%': ["11001", "11010", "00010", "00100", "01000", "01011", "10011"],
    '$': ["00100", "01111", "10100", "01110", "00101", "11110", "00100"],
    '!': ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    '?': ["01110", "10001", "00001", "00110", "00100", "00000", "00100"],
    '+': ["00000", "00100", "00100", "01110", "00100", "00100", "00000"],
    '=': ["00000", "00000", "01110", "00000", "01110", "00000", "00000"],
    '"': ["01010", "01010", "00000", "00000", "00000", "00000", "00000"],
}

# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * w * h * 3)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        for yy in range(max(0, y), min(self.h, y + h)):
            for xx in range(max(0, x), min(self.w, x + w)):
                self.set(xx, yy, c)

    def circle(self, cx, cy, r, c, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill and d <= r * r:
                    self.set(xx, yy, c)
                elif not fill and abs(d - r * r) <= r * 2:
                    self.set(xx, yy, c)

    def line(self, x0, y0, x1, y1, c, thick=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            for a in range(thick):
                for b in range(thick):
                    self.set(x + a, y + b, c)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def tri(self, pts, c):
        (x0, y0), (x1, y1), (x2, y2) = pts
        minx, maxx = min(x0, x1, x2), max(x0, x1, x2)
        miny, maxy = min(y0, y1, y2), max(y0, y1, y2)

        def sign(ax, ay, bx, by, cx, cy):
            return (ax - cx) * (by - cy) - (bx - cx) * (ay - cy)

        d = sign(x0, y0, x1, y1, x2, y2)
        for yy in range(miny, maxy + 1):
            for xx in range(minx, maxx + 1):
                s1 = sign(xx, yy, x0, y0, x1, y1)
                s2 = sign(xx, yy, x1, y1, x2, y2)
                s3 = sign(xx, yy, x2, y2, x0, y0)
                if (d > 0 and s1 >= 0 and s2 >= 0 and s3 >= 0) or \
                   (d < 0 and s1 <= 0 and s2 <= 0 and s3 <= 0):
                    self.set(xx, yy, c)

    def text(self, x, y, s, scale, c):
        cx = x
        for ch in s.upper():
            g = FONT.get(ch, FONT[' '])
            for r in range(7):
                for cc in range(5):
                    if g[r][cc] == '1':
                        self.rect(cx + cc * scale, y + r * scale, scale, scale, c)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s.upper()) * 6 * scale - scale

    def wrap(self, s, maxw, scale):
        lines, cur = [], ""
        for w in s.upper().split():
            t = (cur + " " + w).strip()
            if self.text_w(t, scale) <= maxw or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def png(self):
        raw = b"".join(
            b"\x00" + bytes(self.px[y * self.w * 3:(y + 1) * self.w * 3])
            for y in range(self.h))

        def chunk(t, d):
            c = t + d
            return (struct.pack(">I", len(d)) + c +
                    struct.pack(">I", zlib.crc32(c) & 0xffffffff))

        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
                chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))

# ------------------------------------------------------- stories: 17 Nov 2026
# (tag, icon, headline, one-line summary) - researched from world news
# reports of Tuesday 17 November 2026.
STORIES = [
    ("US-IRAN", "MISSILE",
     "US JETS STRIKE IRAN",
     "US jets hit a missile site on Qeshm Island after Iran fired drones "
     "at a US radar base in Bahrain."),
    ("KERCH BRIDGE", "BRIDGE",
     "KERCH BRIDGE HIT AGAIN",
     "Ukraine strikes the Crimea bridge a second day; a road section "
     "falls into the strait."),
    ("SUMMIT", "GLOBE",
     "TRUMP HEADS TO ASIA",
     "Trump flies to Shenzhen for talks on Thursday with China's Xi "
     "and Russia's Putin."),
    ("NVIDIA", "CHIP",
     "NVIDIA: $115.8BN, NO COMEBACK",
     "Revenue doubles in Q3, but the board says ousted CEO Jensen Huang "
     "will not return."),
    ("FRANCE", "GAVEL",
     "DEPARDIEU PLEADS GUILTY",
     "Actor Gerard Depardieu admits a sexual assault charge and drops "
     "his appeal in Paris."),
    ("JAPAN", "JET",
     "JAPAN SCRAMBLES JETS",
     "Tokyo protests after Russian aircraft enter Japanese airspace; "
     "fighters are sent up."),
    ("GAZA", "AID",
     "WEST URGES: OPEN GAZA AID",
     "UK, Australia, Canada and Italy call on Israel to let humanitarian "
     "aid flow into Gaza."),
    ("EBOLA", "VIRUS",
     "EBOLA PASSES 11,000 CASES",
     "Outbreak in DR Congo grows past 11,000 cases, with 5,400 deaths "
     "reported."),
]
FOOTER = "ALSO: US LOSES MEASLES-FREE STATUS  -  NEPAL FIRST FOR UN LOSS-AND-DAMAGE FUNDS"

WHITE = (255, 255, 255)
INK = (18, 24, 38)
GREY = (70, 76, 92)
PAPER = (247, 243, 233)
GOLD = (212, 160, 32)
RED = (198, 32, 32)
TEAL = (0, 110, 110)
NAVY = (13, 27, 62)


def icon(cv, cx, cy, s, kind, accent):
    if kind == "MISSILE":
        cv.tri([(cx, cy - 26 * s), (cx - 7 * s, cy + 14 * s),
                (cx + 7 * s, cy + 14 * s)], accent)
        cv.circle(cx, cy + 20 * s, 5 * s, accent)
        cv.circle(cx - 16 * s, cy + 8 * s, 3 * s, accent)
        cv.circle(cx + 16 * s, cy + 8 * s, 3 * s, accent)
    elif kind == "BRIDGE":
        cv.line(cx - 26 * s, cy + 16 * s, cx + 26 * s, cy + 16 * s, accent, 4)
        cv.line(cx - 26 * s, cy + 16 * s, cx - 26 * s, cy - 6 * s, accent, 4)
        cv.line(cx + 26 * s, cy + 16 * s, cx + 26 * s, cy - 6 * s, accent, 4)
        for dx in (-18, -9, 0, 9, 18):
            cv.line(cx + dx * s, cy - 14 * s, cx + dx * s, cy + 16 * s, accent, 2)
        cv.line(cx - 26 * s, cy - 6 * s, cx, cy - 20 * s, accent, 3)
        cv.line(cx + 26 * s, cy - 6 * s, cx, cy - 20 * s, accent, 3)
    elif kind == "GLOBE":
        cv.circle(cx, cy, 22 * s, accent, fill=False)
        cv.line(cx - 22 * s, cy, cx + 22 * s, cy, accent, 2)
        cv.line(cx, cy - 22 * s, cx, cy + 22 * s, accent, 2)
        cv.circle(cx, cy, 11 * s, accent, fill=False)
    elif kind == "CHIP":
        cv.rect(cx - 20 * s, cy - 20 * s, 40 * s, 40 * s, accent)
        cv.rect(cx - 11 * s, cy - 11 * s, 22 * s, 22 * s, WHITE)
        for dx in (-16, -5, 6, 16):
            cv.line(cx + dx * s, cy - 28 * s, cx + dx * s, cy - 20 * s, accent, 3)
            cv.line(cx + dx * s, cy + 20 * s, cx + dx * s, cy + 28 * s, accent, 3)
    elif kind == "GAVEL":
        cv.line(cx - 18 * s, cy + 18 * s, cx + 18 * s, cy - 18 * s, accent, 5)
        cv.rect(cx - 24 * s, cy - 14 * s, 16 * s, 8 * s, accent)
        cv.rect(cx + 8 * s, cy + 6 * s, 16 * s, 8 * s, accent)
        cv.line(cx - 20 * s, cy + 24 * s, cx + 20 * s, cy + 24 * s, accent, 3)
    elif kind == "JET":
        cv.tri([(cx + 26 * s, cy), (cx - 18 * s, cy - 12 * s),
                (cx - 18 * s, cy + 12 * s)], accent)
        cv.tri([(cx + 26 * s, cy), (cx - 10 * s, cy),
                (cx - 18 * s, cy + 12 * s)], accent)
        cv.tri([(cx - 4 * s, cy - 6 * s), (cx - 20 * s, cy - 22 * s),
                (cx - 12 * s, cy - 2 * s)], accent)
    elif kind == "AID":
        cv.rect(cx - 22 * s, cy - 16 * s, 44 * s, 32 * s, accent)
        cv.rect(cx - 6 * s, cy - 8 * s, 12 * s, 16 * s, WHITE)
        cv.rect(cx - 10 * s, cy - 4 * s, 20 * s, 8 * s, WHITE)
    elif kind == "VIRUS":
        cv.circle(cx, cy, 14 * s, accent)
        for a in range(8):
            ang = a * math.pi / 4
            cv.line(cx + int(14 * s * math.cos(ang)),
                    cy + int(14 * s * math.sin(ang)),
                    cx + int(24 * s * math.cos(ang)),
                    cy + int(24 * s * math.sin(ang)), accent, 3)
            cv.circle(cx + int(24 * s * math.cos(ang)),
                      cy + int(24 * s * math.sin(ang)), 3 * s, accent)


def render():
    cv = Canvas(1024, 1024, PAPER)
    # Header: masthead + the date, big and unmissable.
    cv.rect(0, 0, 1024, 148, (24, 24, 28))
    cv.rect(0, 148, 1024, 6, GOLD)
    cv.text(36, 26, "THE WORLD IN ONE DAY", 4, WHITE)
    cv.text(36, 62, "17 NOVEMBER 2026", 7, WHITE)
    cv.text(36, 122,
            "TUESDAY  -  EIGHT STORIES THAT DEFINED THE DAY, AROUND THE WORLD",
            2, (210, 210, 200))
    # Eight stories, one row each: icon, headline, plain-language summary.
    y = 176
    for i, (tag, kind, head, sub) in enumerate(STORIES):
        accent = RED if i < 2 else TEAL if i < 4 else NAVY
        cv.rect(24, y, 976, 88, WHITE)
        cv.rect(24, y, 8, 88, accent)
        cv.rect(48, y + 14, 60, 60, (238, 240, 245))
        icon(cv, 78, y + 44, 1, kind, accent)
        cv.text(128, y + 12, tag + "  -  " + head, 3, INK)
        lines = cv.wrap(sub, 976 - 128 - 16, 2)
        cv.text(128, y + 48, lines[0] if lines else "", 2, GREY)
        if len(lines) > 1:
            cv.text(128, y + 66, lines[1], 2, GREY)
        y += 100
    # Footer strip: two more verified stories from the same day.
    cv.text(24, 980, FOOTER, 2, (90, 86, 76))
    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(render().png())
    print("wrote", path)


if __name__ == "__main__":
    main()
