import usb.core
import usb.util
from PIL import Image

class TurzxDevice:
    def __init__(self):
        self.dev = usb.core.find(idVendor=0x1f3a, idProduct=0xb240)
        if self.dev is None: return
        try:
            if self.dev.is_kernel_driver_active(0):
                self.dev.detach_kernel_driver(0)
            self.dev.set_configuration()
        except: pass

    def send_image(self, path, w, h):
        if not self.dev: return
        img = Image.open(path).convert("RGB").resize((w, h)) if path else Image.new("RGB", (w, h), (0,0,0))
        img = img.rotate(90, expand=True)
        pixels = list(img.getdata())
        data = bytearray()
        for r, g, b in pixels:
            p = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            data.append(p & 0xFF); data.append((p >> 8) & 0xFF)
        header = bytearray([0xef, 0xbe, 0x05, 0x00, 0x00, 0x58, 0x02, 0x00] + [0x00]*24)
        try:
            self.dev.write(0x01, header, 1000)
            self.dev.write(0x01, data, 5000)
        except: pass