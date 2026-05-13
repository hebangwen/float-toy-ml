#!/usr/bin/env python3
"""Fix FP8/FP4 conversion functions in index.html and push to GitHub."""
import re

with open("/tmp/float-toy-ml/index.html", "r") as f:
    html = f.read()

# Fix: numberToFp8E4M3 - infinity should use mant=0 (0x78 not 0x7C)
html = html.replace(
    'return x < 0 ? 0xFF : 0x7C; // -Inf: 1_1111_100, +Inf: 0_1111_100',
    'return x < 0 ? 0xF8 : 0x78; // -Inf: 1_1111_000, +Inf: 0_1111_000'
)
html = html.replace(
    "if (exp > 8) return sign | 0x7C;",
    "if (exp > 8) return sign | 0x78;"
)
html = html.replace(
    "if (normalExp > 14) return sign | 0x7C;",
    "if (normalExp > 14) return sign | 0x78;"
)

# Fix: numberToFp8E5M2 - infinity fix (should use mant=0)
html = html.replace(
    "return x < 0 ? 0xFF : 0x7C; // -Inf: 1_11111_00, +Inf: 0_11111_00",
    "return x < 0 ? 0xFC : 0x7C; // -Inf: 1_11111_00, +Inf: 0_11111_00"
)

# Fix: numberToFp8E5M2 overflow to inf should also use mant=0 (E5M2 mant=0 means 0x7C = 0_11111_00)
html = html.replace(
    "if (exp > 16) return sign | 0x7C;",
    "if (exp > 16) return sign | 0x7C;"
)

with open("/tmp/float-toy-ml/index.html", "w") as f:
    f.write(html)

print("Fixed!")
