import time
from ppadb.client import Client
import os
import threading
import cv2

cv2.namedWindow('Cards', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Cards', 900,1090)
cv2.moveWindow('Cards', 1020, -50)
black = cv2.imread(f'assets/black.jpg')
cv2.imshow('Cards', black)
cv2.waitKey(1)

os.system('adb devices')
adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()
if len(devices) == 0:
    print('no device attached')
    quit()
device = devices[0]
print("Connected!")

first_name = ""
last_name = ""
street = ""
house = ""
city = ""
zip = ""
apk_path = "assets/dfb_6.apk"
package_name = "com.rewe.wmapp"

def getPixelColor(x, y):
    offset=1080*y+x+4
    cmd = f"dd if='/sdcard/screen.dump' bs=4 count=1 skip={offset} 2>/dev/null | xxd -p"
    device.shell("screencap /sdcard/screen.dump")
    out = device.shell(cmd)
    return str(out).strip()[:-2]

def waitForPixel(x, y, hex):
    while True:
        if getPixelColor(x, y) == hex:
            break
        time.sleep(0.05)

def pressInstallButton():
    while True:
        if getPixelColor(885, 1993) == "0073dd":
            device.shell("input tap 338 2024")
            break
        time.sleep(0.1)

def scanCard(card_number):
    device.shell("input tap 650 1788")
    if card_number == 1:
        waitForPixel(543, 1165, "ffd6f7")
        device.shell("input tap 543 1165")
    time_waited = 0
    while True:
        if getPixelColor(104, 172) == "ffffff":
            break
        time.sleep(0.05)
        time_waited = time_waited+1
        if time_waited >= 500:
            print("App crashed while starting camera, retrying")
            device.shell("monkey -p com.rewe.wmapp -c android.intent.category.LAUNCHER 1")
            waitForPixel(874, 640, "363d40")
            time.sleep(1)
            waitForPixel(922, 1772, "cc071e")
            time.sleep(0.2)
            device.shell("input tap 650 1788")
    img = cv2.imread(f'assets/{str(card_number)}.jpg')
    black = cv2.imread(f'assets/black.jpg')
    scanned = False
    while not scanned:
        cv2.imshow('Cards', img)
        cv2.waitKey(1)
        for i in range(10):
            if getPixelColor(222, 1538) == "363d40":
                scanned = True
                break
            time.sleep(0.01)
        if scanned == False:
            print(f"Card {card_number} not scanned yet")
            cv2.imshow('Cards', black)
            cv2.waitKey(1)
            time.sleep(0.1)
            if device.shell("pidof com.rewe.wmapp") == "":
                print("App crashed while scanning, retrying")
                device.shell("monkey -p com.rewe.wmapp -c android.intent.category.LAUNCHER 1")
                waitForPixel(874, 640, "363d40")
                time.sleep(1)
                waitForPixel(922, 1772, "cc071e")
                time.sleep(0.2)
                device.shell("input tap 650 1788")
            if getPixelColor(838, 1900) == "ffffff":
                device.shell("input tap 838 1900")
    waitForPixel(540, 1981, "ffffff")
    device.shell("input tap 550 1994")
    time.sleep(1)

    while True:
        hex = getPixelColor(1010, 1800)
        if hex == "f2f3ee":
            device.shell("input tap 555 1971")
        elif hex == "111415" or card_number == 35:
            break
        time.sleep(0.1)

while True:
    try:
        device.uninstall(package_name)
        print("Uninstalled APK")
    except:
        print("Could not find package to uninstall")
    while True:
        try:
            threading.Thread(target=pressInstallButton).start()
            device.install(apk_path)
        except:
            os.system('adb kill-server')
            os.system('adb devices')
            adb = Client(host='127.0.0.1', port=5037)
            devices = adb.devices()
            if len(devices) == 0:
                print('no device attached')
                quit()
            device = devices[0]
        finally:
            if device.is_installed(package_name) == True:
                print("Installed APK")
                break
            input("Something went wrong while installing")

    device.shell("monkey -p com.rewe.wmapp -c android.intent.category.LAUNCHER 1")
    waitForPixel(846, 1825, "757d3b")
    device.shell("input tap 565 1998")
    waitForPixel(547, 1258, "d1b653")
    device.shell("input tap 565 1998")
    waitForPixel(500, 740, "df4b4e")
    device.shell("input tap 565 1998")
    waitForPixel(890, 1252, "8d1813")
    device.shell("input tap 565 1998")
    waitForPixel(850, 1750, "cc071e")
    device.shell("input tap 550 1950")
    waitForPixel(679, 1200, "181a1b")
    device.shell("input tap 562 2007")
    waitForPixel(817, 1125, "757d3b")
    device.shell("input tap 817 1125")
    time.sleep(0.3)
    device.shell("input tap 544 1550")
    waitForPixel(639, 1218, "495052")
    print("Finished Setup, starting to scan cards")
    for i in range(35):
        scanCard(i+1)
        print(f"Scanned card: {i+1}")
    print("Scanned all Cards")
    device.shell("input tap 509 555")
    waitForPixel(782, 1717, "cc071e")
    device.shell("input tap 555 1720")
    waitForPixel(767, 2052, "cc071e")
    device.shell("input tap 250 1074")
    time.sleep(1)
    device.shell(f"input text {first_name}")
    time.sleep(1)
    device.shell("input tap 1000 2140")
    time.sleep(1)
    device.shell("input tap 250 1250")
    time.sleep(1)
    device.shell(f"input text {last_name}")
    time.sleep(1)
    device.shell("input tap 1000 2140")
    time.sleep(1)
    device.shell("input tap 290 1465")
    time.sleep(1)
    device.shell(f"input text {street}")
    time.sleep(1)
    device.shell("input tap 1000 2140")
    time.sleep(1)
    device.shell("input tap 810 1465")
    time.sleep(1)
    device.shell(f"input text {house}")
    time.sleep(1)
    device.shell("input tap 1000 2140")
    time.sleep(1)
    device.shell("input tap 250 1660")
    time.sleep(1)
    device.shell(f"input text {city}")
    time.sleep(1)
    device.shell("input tap 1000 2140")
    time.sleep(1)
    device.shell("input tap 865 1595")
    time.sleep(1)
    device.shell(f"input text {zip}")
    time.sleep(1)
    device.shell("input tap 1000 2140")
    time.sleep(1)
    device.shell("input tap 550 2000")
    waitForPixel(754, 1800, "cc071e")
    device.shell("input tap 754 1800")
    waitForPixel(788, 1950, "fafafa")
    device.shell("input tap 788 1950")
    print(f"Ordered Golden Card!")