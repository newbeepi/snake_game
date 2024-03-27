names = {
    1: "field",
    2: "fieldzone",
    3: "body",
    4: "head_l",
    5: "head_u",
    6: "head_r",
    7: "head_d",
    8: "tail_l",
    9: "tail_u",
    10: "tail_r",
    11: "tail_d",
    12: "cherry",
    13: "lemon",
    14: "banana"
}

from PIL import Image

if __name__ == "__main__":
    boxes_count = 27
    with Image.open("Spritesheet.png") as sheet:
        for i in range(boxes_count):
            if i%2:
                continue
            x = 36 * i
            y = 0
            img = sheet.crop((x, y, x + 36, y + 36))
            img.save(f"icons/{names[i//2+1]}.png")