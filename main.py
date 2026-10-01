import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from config import (
    SERIAL_PORT,
    BAUD_RATE,
    CSV_FILE,
    PLOT_INTERVAL_MS,
    PRINT_EVERY_N_LINES
)
from serial_reader import SerialReader
from logger import DataLogger
from plotter import Plotter


reader = None
logger = None
plotter = Plotter()
line_count = 0


def update(frame):
    global line_count

    line = reader.read_line()

    if not line:
        return plotter.refresh()

    line_count += 1

    if line_count % PRINT_EVERY_N_LINES == 0:
        print("STM32:", line)

    data = reader.parse(line)

    if data is None:
        return plotter.refresh()

    time_ms, ax, ay, az, roll, pitch, yaw, gx, gy, gz = data

    plotter.add_data(ax, ay, az, roll, pitch, yaw, gx, gy, gz)
    logger.save(time_ms, ax, ay, az, roll, pitch, yaw, gx, gy, gz)

    return plotter.refresh()


def main():
    global reader, logger

    print("Opening serial...")
    print("Port:", SERIAL_PORT)
    print("Baud:", BAUD_RATE)
    print("Expected format:")
    print("time,AX_i,AY_i,AZ_i,roll_i,pitch_i,yaw_i,GX_i,GY_i,GZ_i")

    reader = SerialReader(SERIAL_PORT, BAUD_RATE)
    logger = DataLogger(CSV_FILE)

    print("Connected. Close graph window to stop.")

    ani = FuncAnimation(
        plotter.fig,
        update,
        interval=PLOT_INTERVAL_MS,
        blit=False,
        cache_frame_data=False
    )

    try:
        plt.tight_layout(rect=[0, 0.04, 1, 1])
        plt.show()
    finally:
        reader.close()
        logger.close()
        print("Closed.")
        print("Saved CSV:", CSV_FILE)


if __name__ == "__main__":
    main()