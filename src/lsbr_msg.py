"""
Simple implementation of Least Significant Bit Replacement(LSBR) message steganography.
"""

import numpy as np
from PIL import Image


def load_image(img_file: str) -> tuple[tuple, np.ndarray]:
    """
    Load image as flatten numpy array.

    Args:
        img_file (str):  Path to image file

    Returns:
        out1 (tuple):       Shape of the image; (width, height).

        out2 (np.ndarray): Flatten image pixels into 1D.
    """
    img = Image.open(img_file)
    arr = np.array(img)
    return arr.shape, arr.flatten()


def convert_msg(msg: str) -> str:
    """
    Convert (each character in) message to binary strings.
    E.g 'hello' -> '0110100001100101011011000110110001101111'.
    Add '1' at the end- this indicates the end of message.
    NOTE: Standard ASCII character has value from 0 to 127.
    Binary of characters wouldn't start with 1 (since it cannot go to 128).

    Args:
        msg (str):  Message to be converted into binary.

    Returns:
        out (str):  Message converted into binary.
    """
    binary_msg = ""
    for i in msg:
        binary_msg += format(ord(i), "08b")
    binary_msg += "1"
    return binary_msg


def change_bit(img_pix: str, msg_bit: str) -> int:
    """
    Change the last bit of image pixel (regardless if last bit
    is the same as `msg_bit`.)

    Args:
        img_pix (str):  Image pixel (in binary string).
        msg_bit (str):  Message bit (in binary string).

    Returns:
        out (int):  Updated image pixel after embedding message bit.
    """
    new_pix = int(img_pix[:-1] + str(msg_bit), 2)
    return new_pix


def encode_msg(msg: str, img_file: str) -> Image.Image:
    """
    Encode message to image.

    Args:
        msg (str):  Message to be encoded to image.
        img_file (str): Path to image file for encoding.

    Returns:
        out (Image.Image): Image with encoded message.
    """
    binary_msg = convert_msg(msg)
    shape, img = load_image(img_file)
    # Hide message in last bit of image pixel
    for i in range(len(binary_msg)):
        img[i] = change_bit(format(img[i], "08b"), binary_msg[i])
    return Image.fromarray(np.reshape(img, shape))


def decode_msg(img_file: str) -> str:
    """
    Decode (any) message, that is encoded in image.
    Stop decoding when met with binary that starts with '1'.
    NOTE: Standard ASCII character has value from 0 to 127.
    Binary of characters wouldn't start with 1 (since it cannot go to 128).

    Args:
        img_file (str): Path to image file for decoding.

    Returns:
        out (str): Decoded message.
    """
    img = load_image(img_file)[-1]
    extract_char = ""
    decoded_msg = ""
    for i in range(len(img)):
        extract_char += bin(img[i])[-1]
        # This indicates a non-ascii character.
        # This is likely the '1' placed during encoding,
        # to indicate end of message.
        if len(extract_char) == 1 and extract_char[0] == "1":
            break
        # Convert the 8-bit binary into character and append
        if len(extract_char) == 8:
            decoded_msg += chr(int(extract_char, 2))
            # Reset variable to get the 8-bit binary
            extract_char = ""
    return decoded_msg


if __name__ == "__main__":
    opt = input("1: Encode, 2: Decode\n")
    if opt == "1":
        img = input("Enter image to be encoded(with extension): ")
        msg = input("Enter secret message to encode: ")
        img = encode_msg(msg, img)
        img.save(
            input("Enter filename to save encoded image(without extension): ") + ".png"
        )
    elif opt == "2":
        img = input("Enter image to be decoded(with extension): ")
        print(f"Secret Message: {decode_msg(img)}")
