#-*- coding: utf-8 -*-

import argparse
from PIL import Image
from pathlib import Path


def str2bin(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def bin2str(binary, encoding='utf-8', errors='surrogatepass'):
    n = int(binary, 2)
    return n.to_bytes(
        (n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def encode(path_to_image, text_to_encode=None, path_to_text=None):

    if path_to_text is not None:
        text_to_encode = open(path_to_text).read()
    elif text_to_encode is None:
        text_to_encode = input("Enter the message you want to hide: ")

    path_to_image = Path(path_to_image)
    new_path_to_image = Path(
        path_to_image.parent, "{}_{}".format(path_to_image.stem, "1") + ".png")

    img = Image.open(path_to_image)

    secret = str2bin(text_to_encode) + '1111111111111110'

    if len(secret) > img.size[0] * img.size[1]:
        print("You need a bigger image to hide your dirty secret!")
        return

    pixels = img.getdata()
    new_pixels = []
    digit = 0

    for pixel in pixels:
        pixel_R = pixel[0]
        pixel_G = pixel[1]
        pixel_B = pixel[2]

        if digit < len(secret):
            new_pixel_R = bin(pixel_R)[:-1] + secret[digit]
            new_pixel_R = int(new_pixel_R, 2)
            new_pixels.append((new_pixel_R, pixel_G, pixel_B))
            digit += 1
        else:
            new_pixels.append(pixel)

    img.putdata(new_pixels)
    img.save(new_path_to_image)
    print("Your secret is well hidden.")


def decode(path_to_image, path_to_txt):
    path_to_image = Path(path_to_image)
    path_to_txt = Path(path_to_txt)

    img = Image.open(path_to_image)
    pixels = img.getdata()
    binary_text = ""

    for pixel in pixels:
        pixel_R = pixel[0]
        binary_text += bin(pixel_R)[-1]
        try:
            if binary_text[-16:] == "1111111111111110":
                with open(path_to_txt, "w") as f:
                    f.write(bin2str(binary_text[:-16]))
                print("Secret message is located at {}".format(
                    path_to_txt.absolute()))
                return
        except UnicodeDecodeError:
            break
    print("There is no such thing as secret message")


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("--mode", "-m", choices=['hide', 'reveal'],
                       required=True, help="hide/reveal secret in picture")
    parse.add_argument("--image_path", "-i", action="store",
                       required=True, help="path to image(with extension)")
    parse.add_argument("--secret_txt_path", "-e", action="store", default=None,
                       help="path to txt file that contains secret")
    parse.add_argument("--reveal_txt_path", "-d", action="store",
                       default="./reveal_doc.txt",
                       help="path to save the reveal document")
    parse.add_argument("--secret", "-s", action="store", default=None,
                       help="message that you want to hide")

    args = parse.parse_args()

    if args.mode == "hide":
        encode(path_to_image=args.image_path, text_to_encode=args.secret,
               path_to_text=args.secret_txt_path)
    else:
        decode(path_to_image=args.image_path,
               path_to_txt=args.reveal_txt_path)


if __name__ == "__main__":
    main()
