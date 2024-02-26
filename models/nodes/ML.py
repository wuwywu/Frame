# encoding: utf-8
# Author    : WuY<wuyong@mails.ccnu.edu.com>
# Datetime  : 2024/2/25
# User      : WuY
# File      : ML.py
# Morris–Lecar(ML) 模型

from base import Neurons
import os
import sys
import copy
import numpy as np
import matplotlib.pyplot as plt

seed = 0
np.random.seed(seed)                # 给numpy设置随机种子

class ML(Neurons):
    """
    N : 建立神经元的数量
    method ： 计算非线性微分方程的方法，（"eluer", "rk4"）
    dt ： 计算步长
    神经元的膜电位都写为：mem
    """
    def __init__(self, N=1, method="euler", dt=0.01):
        super().__init__(N, method=method, dt=dt)
        # self.num = N  # 神经元数量
        self._params()
        self._vars()

    def _params(self):
        # Parameters for the Morris-Lecar model
        # 不同的分岔，改变下列值
        self.phi = 0.04  # Parameter for the gating variable
        self.gCa = 4.4  # Maximum conductance for Ca++ channels
        self.V3 = 2  # Parameter for the activation of K+ channels
        self.V4 = 30  # Parameter for the activation of K+ channels
        # 不变值
        self.VCa = 120  # Potential for Ca++ ions
        self.VK = -84  # Potential for K+ ions
        self.VL = -60  # Potential for leak channels
        self.gK = 8  # Maximum conductance for K+ channels
        self.gL = 2  # Maximum conductance for leak channels
        self.V1 = -1.2  # Parameter for the activation of Ca++ channels
        self.V2 = 18  # Parameter for the activation of Ca++ channels
        self.C = 20  # Membrane capacitance

        self.Iex = 100  # 恒定的外部激励
        self.th_up = 10.  # 放电阈值
        self.th_dowm = 10.  # 停止放电阈值

    def _vars(self):
        # Model variables
        self.mem = np.random.rand(self.num) * 100 - 50  # Membrane potential, initialized randomly
        self.W = np.random.rand(self.num)  # Probability for K+ channel activation, initialized randomly

    def _ml(self, I):
        M_inf = 0.5 * (1 + np.tanh((self.mem - self.V1) / self.V2))
        W_inf = 0.5 * (1 + np.tanh((self.mem - self.V3) / self.V4))
        tau_W = 1 / np.cosh((self.mem - self.V3) / (2 * self.V4))

        dmem_dt = (1 / self.C) * (I - self.gCa * M_inf * (self.mem - self.VCa)
                                  - self.gK * self.W * (self.mem - self.VK)
                                  - self.gL * (self.mem - self.VL))
        dW_dt = self.phi * (W_inf - self.W) / tau_W

        return dmem_dt, dW_dt

    def __call__(self):
        I = self.Iex  # External current
        # Update the variables using the chosen numerical method
        self.method(self._ml, I, self.mem, self.W)
        # Evaluation of spikes
        self._spikes_eval(self.mem)  # 放电测算

        self.t += self.dt  # Time step forward


if __name__ == "__main__":
    N = 1
    method = "eluer"  # "rk4", "eluer"
    models = ML(N=N, method=method, dt=0.01)
    # models.Iex = 3.
    time = []
    mem = []

    for i in range(100000):
        models()
        time.append(models.t)
        mem.append(models.mem[0])

    plt.plot(time, mem)

    plt.show()

