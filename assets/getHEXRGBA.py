from ppadb.client import Client

adb = Client(host="127.0.0.1", port=5037)
device = adb.devices()[0]

def getPixelColor(x, y):
    offset=1080*y+x+4
    cmd = f"dd if='/sdcard/screen.dump' bs=4 count=1 skip={offset} 2>/dev/null | xxd -p"
    device.shell("screencap /sdcard/screen.dump")
    out = device.shell(cmd)
    return str(out).strip()[:-2]

x, y = 862, 1100

print(f'waitForPixel({x}, {y}, "{getPixelColor(x, y)}")')