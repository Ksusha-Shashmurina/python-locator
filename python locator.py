import numpy as np
import matplotlib.pyplot as plt
import turtle as t
import random
import math

class Common():
    def __init__(self, fd=80000, fs=21000, ti=0.1, Tc=2, d=0.2):
        self.fd = fd
        self.fs = fs
        self.ti = ti
        self.Tc = Tc
        self.d = d

#получение и построение сигналов
class Water(Common):
    def __init__(self, submarine, objects, fd=80000, fs=21000, ti=0.1, Tc=2, d=0.2):
        Common.__init__(self)
        self.submarine = submarine
        self.objects = objects

    def get_signal(self, r, phi):
#       [xs, ys] = self.submarine.get_coord()
        r = 1000
        time = np.arange(0, self.Tc, 1/self.fd)
        signal_left = 10 * np.sin(2 * np.pi * self.fs * time) + np.random.randn(time.size)
        signal_right = 10 * np.sin(2 * np.pi * self.fs * time+np.pi/4) + np.random.randn(time.size)/10

        delay = r / 1500
        dt = self.d / 1500 * np.sin(phi / 180.0 * np.pi)
        for i in range(time.size):
            if time[i] > delay and time[i] < delay + self.ti:
                signal_left[i] += np.sin(2 * np.pi * self.fs * time[i])
                signal_right[i] += np.sin(2 * np.pi * self.fs * time[i] - dt)
        plt.plot(time, signal_left, time, signal_right)
        plt.show()
        return ((time, signal_left, signal_right))


"""
class Submarine:
    def __init__(self, x, y, phi, V, time):
        self.update(time)
        self.get_position
"""
#обработка сигнала (направление и расстоние до цели)
class Sonar(Common): #определение дистанции и пеленг сигналу
    def get_coordinates (self, signalLeft, signalRight):
        spectrumLeft = np.fft.fft(signalLeft)
        spectrumRight = np.fft.fft(signalRight)

        n = spectrumLeft.size
        spectrumLeft[int(n/2):] = 0 #сбрасываем у массива половина спектра
        zLeft = np.abs(np.fft.ifft(spectrumLeft))
        sigma = np.sqrt((np.sum(np.sqrt(zLeft))/n)) #уровень порога обнаружения
        detection_level = np.where(zLeft >= sigma) #сравнение порога
        distance = ((detection_level[0][0])/self.fd)*1650 #определение дистанции
        print(distance)
        phi1 = np.angle(signal_left)
        phi2 = np.angle(signal_right)
        dphi = phi1 - phi2

        dphi = np.angle(np.exp( 1j * dphi) )

        #dphi[np.where( dphi > np.pi )] -= 2 * np.pi
        #dphi[np.where( dphi < -np.pi)] += 2 * np.pi

        dphi_mean = sum(dphi)/dphi.size #среднее значение фи
        peleng = np.arcsin( np.sin(dphi_mean) )
        print(dphi_mean)

        plt.figure(2)
        plt.plot( dphi * 180/np.pi )

        plt.show()


submarine = 0
objects = []
water = Water(submarine, objects, fs=20000, Tc=2)
(time, signal_left, signal_right) = water.get_signal(1100, 40)

sonar = Sonar()
sonar.get_coordinates(signal_left, signal_right)

