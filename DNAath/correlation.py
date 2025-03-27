import numpy as np
import librosa
import scipy.signal
import soundfile as sf

def correlation_adjacent_samples(audio_file):
    y, sr = librosa.load(audio_file, sr=None)  # Đọc file âm thanh
    indices = np.random.randint(0, len(y) - 1, 2048)  # Chọn ngẫu nhiên 2048 mẫu
    x1 = y[indices]
    x2 = y[indices + 1]
    corr = np.corrcoef(x1, x2)[0, 1]
    print(f"Hệ số tương quan giữa các mẫu (samples) liền kề: {corr}")
    


def correlation_audio_frames(audio_file, frame_size=1024):
    y, sr = librosa.load(audio_file, sr=None)
    num_frames = len(y) // frame_size
    frames = np.array_split(y[:num_frames * frame_size], num_frames)

    corr_values = []
    for i in range(len(frames) - 1):
        corr = np.corrcoef(frames[i], frames[i + 1])[0, 1]
        corr_values.append(corr)

    avg_corr = np.mean(corr_values)
    print(f"Hệ số tương quan trung bình giữa các đoạn: {avg_corr}")


def correlation_stereo_channels(audio_file):
    y, sr = sf.read(audio_file)  # Đọc file âm thanh
    if len(y.shape) == 1:
        print("File chỉ có một kênh (mono), không thể tính tương quan giữa kênh trái và phải.")
        return

    left_channel = y[:, 0]  # Kênh trái
    right_channel = y[:, 1]  # Kênh phải
    corr = np.corrcoef(left_channel, right_channel)[0, 1]
    print(f"Hệ số tương quan giữa kênh trái và phải: {corr}")


# Gọi hàm
correlation_adjacent_samples("D:\DNAath\original_audio\leadpipe-91195.wav")
correlation_adjacent_samples("D:\DNAath\encrypted_audio\encrypted_audio.wav")
correlation_stereo_channels("D:\DNAath\original_audio\leadpipe-91195.wav")
correlation_stereo_channels("D:\DNAath\encrypted_audio\encrypted_audio.wav")
