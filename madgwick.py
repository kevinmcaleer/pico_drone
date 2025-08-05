import math

class MadgwickAHRS:
    def __init__(self, sample_period=1/256, beta=0.1):
        self.sample_period = sample_period
        self.beta = beta
        self.q0 = 1.0
        self.q1 = 0.0
        self.q2 = 0.0
        self.q3 = 0.0
        self.q = [1.0, 0.0, 0.0, 0.0]

    def update(self, gx, gy, gz, ax, ay, az, mx, my, mz):
        q0, q1, q2, q3 = self.q0, self.q1, self.q2, self.q3

        gx = math.radians(gx)
        gy = math.radians(gy)
        gz = math.radians(gz)

        norm = math.sqrt(ax * ax + ay * ay + az * az)
        if norm == 0.0:
            return
        ax /= norm
        ay /= norm
        az /= norm

        norm = math.sqrt(mx * mx + my * my + mz * mz)
        if norm == 0.0:
            return
        mx /= norm
        my /= norm
        mz /= norm

        _2q0mx = 2.0 * q0 * mx
        _2q0my = 2.0 * q0 * my
        _2q0mz = 2.0 * q0 * mz
        _2q1mx = 2.0 * q1 * mx
        _2q0 = 2.0 * q0
        _2q1 = 2.0 * q1
        _2q2 = 2.0 * q2
        _2q3 = 2.0 * q3
        _2q0q2 = 2.0 * q0 * q2
        _2q2q3 = 2.0 * q2 * q3
        q0q0 = q0 * q0
        q0q1 = q0 * q1
        q0q2 = q0 * q2
        q0q3 = q0 * q3
        q1q1 = q1 * q1
        q1q2 = q1 * q2
        q1q3 = q1 * q3
        q2q2 = q2 * q2
        q2q3 = q2 * q3
        q3q3 = q3 * q3

        # Reference direction of Earth's magnetic field
        hx = mx * q0q0 - _2q0my * q3 + _2q0mz * q2 + mx * q1q1 + _2q1 * my * q2 + _2q1 * mz * q3 - mx * q2q2 - mx * q3q3
        hy = _2q0mx * q3 + my * q0q0 - _2q0mz * q1 + _2q1mx * q2 - my * q1q1 + my * q2q2 + _2q2 * mz * q3 - my * q3q3
        _2bx = math.sqrt(hx * hx + hy * hy)
        _2bz = -_2q0mx * q2 + _2q0my * q1 + mz * q0q0 + _2q1mx * q3 - mz * q1q1 + _2q2 * my * q3 - mz * q2q2 + mz * q3q3
        _4bx = 2.0 * _2bx
        _4bz = 2.0 * _2bz

        s0 = (-_2q2 * (2.0 * q1q3 - _2q0q2 - ax) + 
              _2q1 * (2.0 * q0q1 + _2q2q3 - ay) - 
              _2bz * q2 * (_2bx * (0.5 - q2q2 - q3q3) + 
              _2bz * (q1q3 - q0q2) - mx) + 
              (-_2bx * q3 + _2bz * q1) * 
              (_2bx * (q1q2 - q0q3) + 
              _2bz * (q0q1 + q2q3) - my) + 
              _2bx * q2 * 
              (_2bx * (q0q2 + q1q3) + 
              _2bz * (0.5 - q1q1 - q2q2) - mz))
        
        s1 = (_2q3 * (2.0 * q1q3 - _2q0q2 - ax) + 
              _2q0 * (2.0 * q0q1 + _2q2q3 - ay) - 
              4.0 * q1 * (1 - 2.0 * q1q1 - 2.0 * q2q2 - az) + 
              _2bz * q3 * 
              (_2bx * (0.5 - q2q2 - q3q3) + 
              _2bz * (q1q3 - q0q2) - mx) + 
              (_2bx * q2 + _2bz * q0) * 
              (_2bx * (q1q2 - q0q3) + 
              _2bz * (q0q1 + q2q3) - my) + 
              (_2bx * q3 - _4bz * q1) * 
              (_2bx * (q0q2 + q1q3) + 
              _2bz * (0.5 - q1q1 - q2q2) - mz))
        
        s2 = (-_2q0 * (2.0 * q1q3 - _2q0q2 - ax) + 
              _2q3 * (2.0 * q0q1 + _2q2q3 - ay) - 
              4.0 * q2 * (1 - 2.0 * q1q1 - 2.0 * q2q2 - az) + 
              (-_4bx * q2 - _2bz * q0) * 
              (_2bx * (0.5 - q2q2 - q3q3) + 
              _2bz * (q1q3 - q0q2) - mx) + 
              (_2bx * q1 + _2bz * q3) * 
              (_2bx * (q1q2 - q0q3) + 
              _2bz * (q0q1 + q2q3) - my) + 
              (_2bx * q0 - _4bz * q2) * 
              (_2bx * (q0q2 + q1q3) + 
              _2bz * (0.5 - q1q1 - q2q2) - mz))
        
        s3 = (_2q1 * (2.0 * q1q3 - _2q0q2 - ax) + 
              _2q2 * (2.0 * q0q1 + _2q2q3 - ay) + 
              (-_4bx * q3 + _2bz * q1) * 
              (_2bx * (0.5 - q2q2 - q3q3) + 
              _2bz * (q1q3 - q0q2) - mx) + 
              (-_2bx * q0 + _2bz * q2) * 
              (_2bx * (q1q2 - q0q3) + 
              _2bz * (q0q1 + q2q3) - my) + 
              _2bx * q1 * 
              (_2bx * (q0q2 + q1q3) + 
              _2bz * (0.5 - q1q1 - q2q2) - mz))

        norm = math.sqrt(s0 * s0 + s1 * s1 + s2 * s2 + s3 * s3)
        s0 /= norm
        s1 /= norm
        s2 /= norm
        s3 /= norm

        # Apply feedback step
        qDot1 = 0.5 * (-q1 * gx - q2 * gy - q3 * gz) - self.beta * s0
        qDot2 = 0.5 * (q0 * gx + q2 * gz - q3 * gy) - self.beta * s1
        qDot3 = 0.5 * (q0 * gy - q1 * gz + q3 * gx) - self.beta * s2
        qDot4 = 0.5 * (q0 * gz + q1 * gy - q2 * gx) - self.beta * s3

        # Integrate rate of change of quaternion
        q0 += qDot1 * self.sample_period
        q1 += qDot2 * self.sample_period
        q2 += qDot3 * self.sample_period
        q3 += qDot4 * self.sample_period

        # Normalise quaternion
        norm = math.sqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3)
        self.q0 = q0 / norm
        self.q1 = q1 / norm
        self.q2 = q2 / norm
        self.q3 = q3 / norm

    def update_imu(self, gx, gy, gz, ax, ay, az):
        q1, q2, q3, q4 = self.q
        sample_period = self.sample_period
        beta = self.beta

        # Normalize accelerometer
        norm = math.sqrt(ax * ax + ay * ay + az * az)
        if norm == 0:
            return
        ax /= norm
        ay /= norm
        az /= norm

        # Gradient descent algorithm corrective step
        f1 = 2*(q2*q4 - q1*q3) - ax
        f2 = 2*(q1*q2 + q3*q4) - ay
        f3 = 1 - 2*(q2*q2 + q3*q3) - az
        J_11or24 = 2*q3
        J_12or23 = 2*q4
        J_13or22 = 2*q1
        J_14or21 = 2*q2
        J_32 = 2*J_14or21
        J_33 = 2*J_11or24

        # Compute gradient
        grad1 = J_14or21*f2 - J_11or24*f1
        grad2 = J_12or23*f1 + J_13or22*f2 - J_32*f3
        grad3 = J_12or23*f2 - J_33*f3 - J_13or22*f1
        grad4 = J_14or21*f1 + J_11or24*f2

        # Normalize gradient
        norm_grad = math.sqrt(grad1*grad1 + grad2*grad2 + grad3*grad3 + grad4*grad4)
        grad1 /= norm_grad
        grad2 /= norm_grad
        grad3 /= norm_grad


    def get_euler(self):
        roll = math.atan2(2 * (self.q0 * self.q1 + self.q2 * self.q3),
                          1 - 2 * (self.q1 * self.q1 + self.q2 * self.q2))
        pitch = math.asin(2 * (self.q0 * self.q2 - self.q3 * self.q1))
        yaw = math.atan2(2 * (self.q0 * self.q3 + self.q1 * self.q2),
                         1 - 2 * (self.q2 * self.q2 + self.q3 * self.q3))
        return math.degrees(roll), math.degrees(pitch), math.degrees(yaw)
