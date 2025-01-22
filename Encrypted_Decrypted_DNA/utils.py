import re
import random
import math
import binascii
from PIL import Image
import numpy as np
import os

# delimiters
# use smaller delimiters encoding for saving space (e.g. <key> -> <k>)
key_del = "<key>"
no_rounds_del = "<no_rounds>"
round_del = "<round>"
reshape_del = "<reshape>"
crossover_del = "<crossover>"
crossover_type_del = "<type>"
single_point_crossover_del = "<single_point>"
rotate_crossover_del = "<rotate>"
rotation_offset_del = "<rotation_offset>"
rotation_types_del = "<rotation_types>"
mutation_del = "<mutation>"
complement_mutation_del = "<complement_mutation>"
alter_mutation_del = "<alter_mutation>"
mutation_table_del = "<mutation_table>"
chromosome_del = "<chromosome>"

# generate encoding tables domains
two_bit_list = ['00', '01', '10', '11']
dna_bases = ['A', 'C', 'G', 'T']

four_bit_list = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100',
                 '1101', '1110', '1111']
two_dna_bases = ['TA', 'TC', 'TG', 'TT', 'GA', 'GC', 'GG', 'GT', 'CA', 'CC', 'CG', 'CT', 'AA', 'AC', 'AG', 'AT']

# encoding tables and their reversal
two_bits_to_dna_base_table = None
dna_base_to_two_bits_table = None

four_bits_to_two_dna_base_table = None
two_dna_base_to_four_bits_table = None

key_filename = "key_mandrill.txt"
original_filename = "original_binary_data_mandrill.txt"
encrypted_filename = "encrypted_mandrill.txt"
decrypted_filename = "decrypted_binary_mandrill.txt"

destination_path_key = os.path.join("key", key_filename)
destination_path_original_bin = os.path.join("original_binary", original_filename)
destination_path_encrypted = os.path.join("encrypted_dna", encrypted_filename)
destination_path_decrypted_bin = os.path.join("decrypted_binary", decrypted_filename)


def str2bin(sstring):
    """
    Transform a string (e.g. 'Hello') into a string of bits
    """
    bs = ''
    for c in sstring:
        bs = bs + bin(ord(c))[2:].zfill(8)
    return bs


def bin2str(bs):
    """
      Transform a binary string into an ASCII string
    """
    n = int(bs, 2)
    return binascii.unhexlify('%x' % n)


def byte2bin(byte_val):
    """
    Transform a byte (8-bit) value into a bitstring
    """
    return bin(byte_val)[2:].zfill(8)


def bitxor(a, b):
    """
    Xor two bit strings (trims the longer input)
    """
    return "".join([str(int(x) ^ int(y)) for (x, y) in zip(a, b)])


def divisors(n):
    """
    Get the divisors of a natural number.
    :param n: the number
    :return: list of divisors
    """
    divs = []
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divs.extend([i, n / i])

    divs = [int(d) for d in divs]
    return list(set(divs))


def generate_pre_processing_tables():
    """
    Generate the 2 bits to dna bases encoding table (e.g. '01'->C)
    """
    global two_bits_to_dna_base_table
    global dna_base_to_two_bits_table

    # if you want random table
    # random.shuffle(dna_bases)
    two_bits_to_dna_base_table = dict(zip(two_bit_list, dna_bases))
    dna_base_to_two_bits_table = dict(zip(two_bits_to_dna_base_table.values(), two_bits_to_dna_base_table.keys()))


def generate_mutation_tables():
    """
    Generate the 4 bits to 2 dna bases encoding table (e.g. '0101'->CG)
    """
    global four_bits_to_two_dna_base_table
    global two_dna_base_to_four_bits_table

    # if you want random table
    # random.shuffle(two_dna_bases)
    four_bits_to_two_dna_base_table = dict(zip(four_bit_list, two_dna_bases))
    two_dna_base_to_four_bits_table = dict(
        zip(four_bits_to_two_dna_base_table.values(), four_bits_to_two_dna_base_table.keys()))


def group_bits(byte, step=2):
    """
    Group the bits from a byte / bigger sequence of bits into groups by length "step"
    :return: a list of groups
    """
    bits_groups = []
    for i in range(0, len(byte), step):
        bits_groups.append(byte[i:i + step])
    return bits_groups


def group_bases(dna_seq, step=2):
    """
    Group the DNA base from a sequence into groups by length "step"
    :return: a list of groups
    """
    bases_groups = []
    for i in range(0, len(dna_seq), step):
        bases_groups.append(dna_seq[i:i + step])
    return bases_groups


def generate_bits(byte_data):
    """
    Take every byte for sequence and group its bits
    :return:
    """
    grouped_bits_data = []

    for byte in byte_data:
        grouped_bits_data.extend(group_bits(byte))

    return grouped_bits_data


def binarized_data(data):
    # convert every char to ASCII and then to binary
    byte_data = [byte2bin(ord(c)) for c in data]

    return generate_bits(byte_data)


def bits_to_dna(data, conversion_table):
    # convert binary sequence to DNA sequence
    return "".join([conversion_table[bits] for bits in data])


def dna_to_bits(data, conversion_table):
    # convert DNA sequence to binary sequence
    return "".join([conversion_table[dna_base] for dna_base in data])


def get_pattern(delimiter, s):
    """
    Get the pattern info between delimiters from the string
    """
    regex = "%s(.*?)%s" % (delimiter, delimiter)
    return re.findall(regex, s)

def image_to_binary(image_path):
    """
    Chuyển đổi hình ảnh thành chuỗi nhị phân.
    :param image_path: Đường dẫn đến tệp hình ảnh.
    :return: Chuỗi nhị phân đại diện cho hình ảnh.
    """
    img = Image.open(image_path)
    img = img.convert('L')  # Đảm bảo hình ảnh ở định dạng RGB
    binary_data = ''
    
    for pixel in img.getdata():
        # Chuyển đổi từng pixel thành nhị phân (0 cho đen, 255 cho trắng)
        binary_data += format(pixel, '08b')  # Sử dụng format() để giữ 8 bit cho mỗi pixel

    return binary_data
# Hàm chuyển đổi chuỗi nhị phân thành hình ảnh
import numpy as np

# def binary_to_image(binary_string, width):
#     """
#     Chuyển đổi chuỗi nhị phân thành hình ảnh đen trắng.
#     :param binary_string: Chuỗi nhị phân đại diện cho hình ảnh.
#     :param width: Chiều rộng của hình ảnh.
#     :return: Hình ảnh đen trắng.
#     """
#     height = 256  # Tính chiều cao

#     # Tạo mảng numpy từ chuỗi nhị phân
#     pixel_array = np.zeros((height, width), dtype=np.uint8)
    
#     for i in range(height):
#         for j in range(width):
#             # Lấy 8 bit cho mỗi pixel
#             pixel_bits = binary_string[(i * width + j) * 8 : (i * width + j + 1) * 8]
#             pixel_value = int(pixel_bits, 2)  # Chuyển chuỗi nhị phân thành giá trị pixel
#             pixel_array[i, j] = pixel_value   # 255 cho trắng, 0 cho đen

#     # Tạo hình ảnh từ mảng pixel
#     image = Image.fromarray(pixel_array, mode='L')  # 'L' mode cho ảnh grayscale
#     return image
def binary_to_image(binary_string):
    """
    Chuyển đổi chuỗi nhị phân thành hình ảnh đen trắng.
    """
    width = 256
    height = 256  # hoặc tính chiều cao từ kích thước hình ảnh gốc
    expected_length = height * width * 8  # Số bit cần thiết

    # Kiểm tra độ dài của binary_string
    if len(binary_string) < expected_length:
        raise ValueError(f"Chuỗi nhị phân quá ngắn! Độ dài yêu cầu: {expected_length}, hiện tại: {len(binary_string)}")

    # Tạo mảng numpy từ chuỗi nhị phân
    pixel_array = np.zeros((height, width), dtype=np.uint8)
    
    for i in range(height):
        for j in range(width):
            pixel_bits = binary_string[(i * width + j) * 8 : (i * width + j + 1) * 8]
            pixel_value = int(pixel_bits, 2)  # Chuyển chuỗi nhị phân thành giá trị pixel
            pixel_array[i, j] = pixel_value

    image = Image.fromarray(pixel_array, mode='L')  # 'L' mode cho ảnh grayscale
    return image
