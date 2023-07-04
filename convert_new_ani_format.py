import os
import shutil

to_convert = ["p1", "tombstone"]
for root, dirs, files in os.walk("assets/spells"):
    to_convert.extend([f"spells/{i}" for i in dirs])
    break

for folder in to_convert:
    for direction in ["n", "e", "s", "w"]:
        os.mkdir(f"assets/{folder}/{direction}")
        shutil.move(f"assets/{folder}/{direction}.png", f"assets/{folder}/{direction}/0")

