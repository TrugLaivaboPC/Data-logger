from collections import deque
import matplotlib.pyplot as plt

from config import MAX_POINTS, ACC_YLIM, GYRO_YLIM, ANGLE_YLIM


class Plotter:
    def __init__(self):
        self.sample = 0

        self.x = deque(maxlen=MAX_POINTS)

        self.ax_data = deque(maxlen=MAX_POINTS)
        self.ay_data = deque(maxlen=MAX_POINTS)
        self.az_data = deque(maxlen=MAX_POINTS)

        self.gx_data = deque(maxlen=MAX_POINTS)
        self.gy_data = deque(maxlen=MAX_POINTS)
        self.gz_data = deque(maxlen=MAX_POINTS)

        self.roll_data = deque(maxlen=MAX_POINTS)
        self.pitch_data = deque(maxlen=MAX_POINTS)
        self.yaw_data = deque(maxlen=MAX_POINTS)

        self.fig, (self.acc_plot, self.gyro_plot, self.angle_plot) = plt.subplots(
            3,
            1,
            figsize=(12, 8),
            sharex=True
        )

        self.line_ax, = self.acc_plot.plot([], [], label="AX")
        self.line_ay, = self.acc_plot.plot([], [], label="AY")
        self.line_az, = self.acc_plot.plot([], [], label="AZ")

        self.line_gx, = self.gyro_plot.plot([], [], label="GX")
        self.line_gy, = self.gyro_plot.plot([], [], label="GY")
        self.line_gz, = self.gyro_plot.plot([], [], label="GZ")

        self.line_roll, = self.angle_plot.plot([], [], label="Roll")
        self.line_pitch, = self.angle_plot.plot([], [], label="Pitch")
        self.line_yaw, = self.angle_plot.plot([], [], label="Yaw")

        self._setup_plot(
            self.acc_plot,
            "Acceleration",
            "g",
            ACC_YLIM
        )

        self._setup_plot(
            self.gyro_plot,
            "Gyroscope",
            "deg/s",
            GYRO_YLIM
        )

        self._setup_plot(
            self.angle_plot,
            "Orientation",
            "degree",
            ANGLE_YLIM
        )

        self.angle_plot.set_xlabel("Sample")

        self.status_text = self.fig.text(
            0.01,
            0.01,
            "",
            fontsize=9
        )

    def _setup_plot(self, axis, title, ylabel, ylim):
        axis.set_title(title)
        axis.set_ylabel(ylabel)
        axis.set_ylim(ylim[0], ylim[1])
        axis.grid(True, alpha=0.35)
        axis.legend(loc="upper right", ncol=3)

    def add_data(self, ax, ay, az, roll, pitch, yaw, gx, gy, gz):
        self.sample += 1

        self.x.append(self.sample)

        self.ax_data.append(ax)
        self.ay_data.append(ay)
        self.az_data.append(az)

        self.gx_data.append(gx)
        self.gy_data.append(gy)
        self.gz_data.append(gz)

        self.roll_data.append(roll)
        self.pitch_data.append(pitch)
        self.yaw_data.append(yaw)

        self.status_text.set_text(
            f"AX={ax:.3f}g  AY={ay:.3f}g  AZ={az:.3f}g     "
            f"GX={gx:.2f}  GY={gy:.2f}  GZ={gz:.2f} deg/s     "
            f"Roll={roll:.2f}°  Pitch={pitch:.2f}°  Yaw={yaw:.2f}°"
        )

    def refresh(self):
        self.line_ax.set_data(self.x, self.ax_data)
        self.line_ay.set_data(self.x, self.ay_data)
        self.line_az.set_data(self.x, self.az_data)

        self.line_gx.set_data(self.x, self.gx_data)
        self.line_gy.set_data(self.x, self.gy_data)
        self.line_gz.set_data(self.x, self.gz_data)

        self.line_roll.set_data(self.x, self.roll_data)
        self.line_pitch.set_data(self.x, self.pitch_data)
        self.line_yaw.set_data(self.x, self.yaw_data)

        if self.sample < MAX_POINTS:
            self.acc_plot.set_xlim(0, MAX_POINTS)
        else:
            self.acc_plot.set_xlim(self.sample - MAX_POINTS, self.sample)

        return (
            self.line_ax,
            self.line_ay,
            self.line_az,
            self.line_gx,
            self.line_gy,
            self.line_gz,
            self.line_roll,
            self.line_pitch,
            self.line_yaw,
        )