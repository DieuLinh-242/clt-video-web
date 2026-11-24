"""Tạo video static/video/clt_simulation.mp4 mô phỏng Định lí Giới hạn Trung tâm.

Chạy:  python scripts/make_video.py
Yêu cầu: numpy, matplotlib và ffmpeg (cài trên máy hoặc Colab).
Phân phối gốc: Exp(1) (mu = 1, sigma = 1), lệch phải.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter

OUT = Path(__file__).resolve().parent.parent / "static" / "video" / "clt_simulation.mp4"
OUT.parent.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(2026)
MU, SIGMA = 1.0, 1.0
N_LIST = [1, 2, 5, 10, 30, 100]
N_REPS = 5000            # số mẫu lặp cho mỗi n
FPS = 20
FRAMES_GROW = 60         # số khung để histogram "lớn dần"
FRAMES_HOLD = 30         # số khung giữ nguyên kết quả
BINS = np.linspace(-4, 4, 41)
CENTERS = (BINS[:-1] + BINS[1:]) / 2
WIDTH = BINS[1] - BINS[0]
XS = np.linspace(-4, 4, 400)
NORMAL_PDF = np.exp(-XS**2 / 2) / np.sqrt(2 * np.pi)

# Tính trước Z_n cho từng n
Z = {}
for n in N_LIST:
    means = rng.exponential(MU, size=(N_REPS, n)).mean(axis=1)
    Z[n] = (means - MU) / (SIGMA / np.sqrt(n))

fig, (ax0, ax1) = plt.subplots(
    1, 2, figsize=(9.6, 5.4), dpi=100, gridspec_kw={"width_ratios": [1, 1.6]}
)
fig.patch.set_facecolor("white")

# Panel trái: phân phối gốc
x0 = np.linspace(0, 6, 300)
ax0.fill_between(x0, np.exp(-x0), color="#f4a261", alpha=0.85)
ax0.set_title("Phân phối gốc: Exp(1)", fontsize=12)
ax0.set_xlabel("x")
ax0.set_ylabel("mật độ")
ax0.set_xlim(0, 6)
ax0.set_ylim(0, 1.05)
ax0.text(3.0, 0.7, "Lệch phải,\nkhông phải\nphân phối chuẩn",
         fontsize=11, ha="center", color="#7a3b00")

# Panel phải: histogram của Z_n
bars = ax1.bar(CENTERS, np.zeros_like(CENTERS), width=WIDTH * 0.95,
               color="#0b79d0", alpha=0.85, label="Histogram của $Z_n$")
ax1.plot(XS, NORMAL_PDF, "--", color="#c1121f", lw=2, label="Mật độ $N(0,1)$")
ax1.set_xlim(-4, 4)
ax1.set_ylim(0, 0.95)
ax1.set_xlabel(r"$Z_n=(\bar X_n-\mu)/(\sigma/\sqrt{n})$")
ax1.set_ylabel("mật độ")
ax1.legend(loc="upper right", fontsize=9)
title = ax1.set_title("", fontsize=13)
counter = ax1.text(0.02, 0.95, "", transform=ax1.transAxes, fontsize=11, va="top")

fig.suptitle("Định lí Giới hạn Trung tâm", fontsize=15, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.94))


def draw(n, m):
    """Vẽ histogram từ m trung bình mẫu đầu tiên của cỡ mẫu n."""
    z = Z[n][:max(m, 1)]
    dens, _ = np.histogram(z, bins=BINS, density=True)
    # density=True chia theo số quan sát nằm trong [-4,4]; đủ chính xác cho minh hoạ
    for b, h in zip(bars, dens):
        b.set_height(h)
    title.set_text(f"Cỡ mẫu n = {n}")
    counter.set_text(f"Số trung bình mẫu: {m:,}")


writer = FFMpegWriter(
    fps=FPS,
    codec="libx264",
    extra_args=["-pix_fmt", "yuv420p", "-crf", "26", "-movflags", "+faststart"],
)

with writer.saving(fig, str(OUT), dpi=100):
    for n in N_LIST:
        for k in range(1, FRAMES_GROW + 1):
            # tăng số mẫu theo thang gần-căn để lúc đầu thay đổi nhanh
            m = int(N_REPS * (k / FRAMES_GROW) ** 1.5)
            draw(n, m)
            writer.grab_frame()
        draw(n, N_REPS)
        for _ in range(FRAMES_HOLD):
            writer.grab_frame()

print("Đã tạo:", OUT, f"({OUT.stat().st_size / 1e6:.2f} MB)")
