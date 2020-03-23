
from threading import Thread, Lock
import cv2
import time
import numpy as np
import datetime

def write_log(str):
    with open('cam_log.txt', 'a+') as f:
        f.write(str)
    #f.close()

class VideoGet:

    def __init__(self, src, evt):
    # def __init__(self, src):                                 # без ожидания evt
        self.e = evt                                           # без ожидания evt - закомментить
        self.source = src
        self.call_cam()

    def call_cam(self):
        self.stream = cv2.VideoCapture(self.source)
        write_log('Cam initializing: {}\n'.format(datetime.datetime.now()))
        _, self.frame = self.stream.read()
        if _:
            if np.shape(self.frame) != ():
                write_log('Cam initialized: {}\n'.format(datetime.datetime.now()))
                self.stopped = False
        else:
            self.stopped = True

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while True:
            if self.stopped != True:
                self.e.wait()                                          # без ожидания evt - закомментить
                _, frm = self.stream.read()
                if _:
                    if frm is None:
                        write_log('It was None frame: {}\n'.format(datetime.datetime.now()))
                        _, frm2 = self.stream.read()
                        if _:
                            write_log('The next frame after None frame was SUCCESSFULLY caught: {}\n'.format(
                                datetime.datetime.now()))
                        else:
                            write_log('The next frame after None frame catching FAILED: {}\n'.format(
                                datetime.datetime.now()))
                    else:
                        if np.shape(frm) != ():
                            self.frame = frm
                            time.sleep(0.00075)
                            self.e.clear()                                          # без ожидания evt - закомментить
                        else:
                            write_log('It was empty frame: {}\n'.format(datetime.datetime.now()))
                            self.e.clear()                                          # без ожидания evt - закомментить

                else:
                    write_log('VideoCapture error, stop reading: {}\n'.format(datetime.datetime.now()))
                    self.e.clear()                                          # без ожидания evt - закомментить
                    self.stopped = True

            else:
                write_log('Cam connecting error, trying to reconnect: {}\n'.format(datetime.datetime.now()))
                self.e.clear()                                          # без ожидания evt - закомментить
                self.call_cam()



    def read(self):
        frame = self.frame.copy()
        return frame

    def stop(self):
        self.stopped = True