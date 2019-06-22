from PIL import Image, ImageDraw

class Overlay():
    def update(self):
        # Paste the original image into the padded one
        self.padded.paste(self.image, (0, 0))

    def __init__(self, resolution):
        # Create the base overlay
        self.image = Image.new('RGBA', resolution, (0,0,0,64))
        # Create an image padded to the required size with
        # mode 'RGBA'
        self.padded = Image.new('RGBA', (
            ((self.image.size[0] + 31) // 32) * 32,
            ((self.image.size[1] + 15) // 16) * 16,
            ))
        self.update()


class ROIOverlay(Overlay):
    def __init__(self, resolution, roi, opacity):
        Overlay.__init__(self, resolution)

        self.drawable = ImageDraw.Draw(self.image)

        self.roi = roi
        self.roi = roi

        # Size in pixel of ROI
        self.roi_size = (round(resolution[0]*self.roi[0]), round(resolution[0]*self.roi[0]))
        # Upper-left corner of ROI
        # (x-x0, y-y0) where (x0,y0) is image center
        self.roi_a = (resolution[0]//2 - self.roi_size[0]//2, resolution[1]//2 - self.roi_size[1]//2)
        # Bottom-right corner of ROI
        self.roi_b = (self.roi_a[0] + self.roi_size[0], self.roi_a[1] + self.roi_size[1])

        self.drawable.rectangle([(0,0), (resolution[0]-1, resolution[1]-1)], fill=(0,0,0, opacity))
        self.drawable.rectangle([self.roi_a, self.roi_b], fill=(0,0,0,0), outline=(0,255,0,255), width=2)
        self.update()
