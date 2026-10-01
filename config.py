from pathlib import Path

# Sửa COM ở đây
SERIAL_PORT = "COM17"

# Phải giống STM32
BAUD_RATE = 115200

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "mpu6050_log.csv"

# Số điểm hiện trên graph
MAX_POINTS = 300

# Tốc độ update graph
PLOT_INTERVAL_MS = 30

# In terminal mỗi mấy dòng
PRINT_EVERY_N_LINES = 5

# Giới hạn trục Y cho graph
ACC_YLIM = (-2.0, 2.0)
GYRO_YLIM = (-250.0, 250.0)
ANGLE_YLIM = (-180.0, 180.0)