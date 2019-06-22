from time import sleep
from picamera import PiCamera
from picamera.color import Color
from io import BytesIO
from PIL import Image, ImageDraw
import numpy as np
from pyzbar.pyzbar import decode as qrdecode

class Scanner():
    def __init__(self, overlay, qr_validator):
        self.overlay = overlay
        self.qr_validator = qr_validator

    def run(self):
        # Write captures to memory
        stream = BytesIO()

        # Init camera
        camera = PiCamera()
        camera.sensor_mode = 2
        camera.resolution = (2592,1944)
        camera.framerate = 12
        camera.hflip = True
        camera.annotate_text_size = 100

        # Add overlay
        o = camera.add_overlay(self.overlay.padded.tobytes(), layer=3, alpha=255, size=self.overlay.image.size)

        RED = Color('#ff0000')
        GREEN = Color('#00ff00')
        BLUE = Color('#0000ff')

        camera.annotate_text = 'SCANNING'
        camera.annotate_background = BLUE
        camera.start_preview()

        try:
            while True:
                camera.annotate_text = 'SCANNING'
                camera.annotate_background = BLUE
                sleep(3)
                stream.seek(0)
                camera.capture(stream, format='jpeg', resize=(self.overlay.image.size[0], self.overlay.image.size[1]))
                stream.seek(0)
                image = Image.open(stream)
                image = image.crop(self.overlay.roi_a + self.overlay.roi_b)
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
                qr = qrdecode(image)
                print(qr)
                if len(qr) != 0:
                    if self.qr_validator(qr[0][0].decode()):
                        camera.annotate_text = 'AUTHORIZED'
                        camera.annotate_background = GREEN;
                    else:
                        camera.annotate_text = 'NOT AUTHORIZED'
                        camera.annotate_background = RED;
                    sleep(3)
        finally:
            camera.remove_overlay(o)
            camera.close()
