import serial


class SerialReader:
    def __init__(self, port, baud_rate):
        self.ser = serial.Serial(port, baud_rate, timeout=0.05)
        self.ser.reset_input_buffer()

    def read_line(self):
        """
        Đọc dòng mới nhất từ STM32.
        Nếu buffer có nhiều dòng cũ, bỏ qua dòng cũ để graph không bị lag.
        """

        raw = self.ser.readline()

        if not raw:
            return ""

        latest = raw

        while self.ser.in_waiting:
            latest = self.ser.readline()

        return latest.decode("utf-8", errors="ignore").strip()

    def parse(self, line):
        """
        STM32 format:
        time,AX_i,AY_i,AZ_i,roll_i,pitch_i,yaw_i,GX_i,GY_i,GZ_i

        Scale:
        AX_i AY_i AZ_i = acceleration * 1000
        roll_i pitch_i yaw_i = angle * 100
        GX_i GY_i GZ_i = gyro * 100
        """

        if not line:
            return None

        line = line.replace("STM32:", "").strip()
        parts = [p.strip() for p in line.split(",")]

        if len(parts) != 10:
            print("Invalid data:", line)
            return None

        try:
            time_ms = int(parts[0])

            ax = int(parts[1]) / 1000.0
            ay = int(parts[2]) / 1000.0
            az = int(parts[3]) / 1000.0

            roll = int(parts[4]) / 100.0
            pitch = int(parts[5]) / 100.0
            yaw = int(parts[6]) / 100.0

            gx = int(parts[7]) / 100.0
            gy = int(parts[8]) / 100.0
            gz = int(parts[9]) / 100.0

            return time_ms, ax, ay, az, roll, pitch, yaw, gx, gy, gz

        except ValueError:
            print("Invalid data:", line)
            return None

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()