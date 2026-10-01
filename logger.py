import csv
import os
from datetime import datetime


class DataLogger:
    def __init__(self, filename):
        self.filename = filename
        file_exists = os.path.exists(filename)

        self.file = open(filename, "a", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file)

        if not file_exists:
            self.writer.writerow([
                "pc_time",
                "time_ms",
                "AX_g",
                "AY_g",
                "AZ_g",
                "roll_deg",
                "pitch_deg",
                "yaw_deg",
                "GX_deg_s",
                "GY_deg_s",
                "GZ_deg_s"
            ])
            self.file.flush()

    def save(self, time_ms, ax, ay, az, roll, pitch, yaw, gx, gy, gz):
        pc_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        self.writer.writerow([
            pc_time,
            time_ms,
            ax,
            ay,
            az,
            roll,
            pitch,
            yaw,
            gx,
            gy,
            gz
        ])

        self.file.flush()

    def close(self):
        if self.file:
            self.file.close()