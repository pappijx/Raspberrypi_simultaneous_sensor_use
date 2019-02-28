#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib2
from threading import Thread
import RPi.GPIO as GPIO
import datetime, time
import csv
GPIO.setmode(GPIO.BCM)


N1 = "sensor1"
T1 = 23
D1 = 24 

N2 = "sensor2"
T2 = 7
D2 = 8

class counter(Thread):
    def __init__(self, sensor, triger, name):
        Thread.__init__(self)
        self.sensor = sensor
        self.triger = triger
        self.name = name

        GPIO.setup(self.sensor, GPIO.IN)
        GPIO.setup(self.triger, GPIO.OUT)
		

    def run(self):
        print "Run -  ", self.sensor, self.triger, self.name

        while True:
            GPIO.output(self.triger, False)
            time.sleep(0.025)
            GPIO.output(self.triger, True)
            time.sleep(0.00001)
            GPIO.output(self.triger, False)


            while (GPIO.input(self.sensor)==0):
                pulse_start1 = time.time()

            while GPIO.input(self.sensor)==1:
                pulse_end1 = time.time()

            pulse_duration1 = pulse_end1 - pulse_start1
            distance1 = pulse_duration1 * 17150
            distance1 = round(distance1, 2)
            status = 1
            if distance1 < 15:
                print str(datetime.datetime.now()), self.name, distance1,"parked"
                status = 1
                time.sleep(1)
            else
            	print str(datetime.datetime.now()), self.name, distance1,"unparked"
            	status = 0
            	time.sleep(1)
            row = [self.sensor, self.triger,self.name,status,datetime.datetime.now() ]

			with open('data.csv', 'a') as csvFile:
    			writer = csv.writer(csvFile)
    			writer.writerow(row)

			csvFile.close()

def main():
    thread1 = counter(D1,T1,N1)
    thread1.start()

    thread2 = counter(D2,T2,N2)
    thread2.start()

if __name__ == "__main__":
    main()
