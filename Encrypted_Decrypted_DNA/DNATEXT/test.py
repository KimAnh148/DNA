import math
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

# ================================
# 1. TÍNH ENTROPY CHO BYTES
# ================================
def calculate_entropy(data: bytes) -> float:
    if len(data) == 0:
        return 0.0
    freq = Counter(data)
    n = len(data)
    probs = [count / n for count in freq.values()]
    entropy = -sum(p * math.log2(p) for p in probs)
    return entropy


# ================================
# 2. VẼ HISTOGRAM
# ================================
def plot_histogram(data: bytes, title="Histogram"):
    freq = Counter(data)
    x = list(range(256))
    y = [freq.get(i, 0) for i in x]

    plt.figure(figsize=(10, 4))
    plt.bar(x, y, width=1.0)
    plt.title(title)
    plt.xlabel("Giá trị byte (0–255)")
    plt.ylabel("Tần suất")
    plt.tight_layout()
    plt.show()


# ================================
# 3. TÍNH HỆ SỐ TƯƠNG QUAN NGANG
# ================================
def correlation_horizontal(data):

    # Nếu là chuỗi (text/DNA)
    if isinstance(data, str):
        if set(data).issubset({'0', '1'}):
            numeric = np.array([int(c) for c in data], dtype=np.float64)
        else:
            numeric = np.array([ord(c) for c in data], dtype=np.float64)

    # Nếu là list hoặc numpy array
    elif isinstance(data, (list, np.ndarray)):
        numeric = np.array(data, dtype=np.float64)

    else:
        raise TypeError("Unsupported data type for correlation.")

    if len(numeric) < 2:
        return 0.0

    x = numeric[:-1]
    y = numeric[1:]

    numerator = np.mean((x - np.mean(x)) * (y - np.mean(y)))
    denominator = np.std(x) * np.std(y)

    if denominator == 0:
        return 0.0

    return numerator / denominator


# ================================
# 4. HÀM ĐỌC FILE & TÍNH TOÁN
# ================================
def evaluate_files(original_path, encrypted_path):

    # Đọc file dạng bytes cho ENTROPY + HISTOGRAM
    with open(original_path, "rb") as f:
        original_bytes = f.read()

    with open(encrypted_path, "rb") as f:
        encrypted_bytes = f.read()

    # CHUYỂN bytes → string để tính CORRELATION
    original_str = original_bytes.decode("utf-8", errors="ignore")
    encrypted_str = encrypted_bytes.decode("utf-8", errors="ignore")

    # ===== ENTROPY =====
    print("===== ENTROPY =====")
    print("Entropy (gốc):     ", round(calculate_entropy(original_bytes), 4))
    print("Entropy (mã hóa):  ", round(calculate_entropy(encrypted_bytes), 4))

    # ===== CORRELATION =====
    print("\n===== CORRELATION =====")
    print("Corr (gốc):        ", round(correlation_horizontal(original_str), 6))
    print("Corr (mã hóa):     ", round(correlation_horizontal(encrypted_str), 6))

    # ===== HISTOGRAM =====
    print("\n===== HISTOGRAM =====")
    plot_histogram(original_bytes, "Histogram - Original Text (bytes)")
    plot_histogram(encrypted_bytes, "Histogram - Encrypted Text (bytes)")


# ================================
# CHẠY THỬ
# ================================
evaluate_files(
    original_path=r"D:/Encrypted_Decrypted_DNA/DNATEXT/text_11B.txt",
    encrypted_path=r"D:/Encrypted_Decrypted_DNA/DNATEXT/encrypted_dna/encrypted.txt"
)
