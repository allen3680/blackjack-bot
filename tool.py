import pyautogui
import pytesseract
import cv2 as cv
import numpy as np
import mss.tools
import random
from PIL import ImageGrab, Image
from functools import partial
from my_enum import *
import pygetwindow as gw
from time import sleep

pyautogui.FAILSAFE= False

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'


def screenshot(region1, region2, region3, region4, location):
    region1 = int(region1)
    region2 = int(region2)
    region3 = int(region3)
    region4 = int(region4)
    monitor_number = 1
    if region1 > 1920:
        monitor_number = 2
    with mss.mss() as sct:
        monitor = {"top": region2, "left": region1,
                   "width": region3, "height": region4, "mon": monitor_number}
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=location)


def super_screenshot(coordinate_dict, name):
    temp = coordinate_dict[name].split(',')
    screenshot(temp[0], temp[1], temp[2], temp[3],
               './screenshot/' + name + '_new.png')


def screenshot_img(region1, region2, region3, region4):
    region1 = int(region1)
    region2 = int(region2)
    region3 = int(region3)
    region4 = int(region4)
    monitor_number = 1
    if region1 > 1920:
        monitor_number = 2
    with mss.mss() as sct:
        monitor = {"top": region2, "left": region1,
                   "width": region3, "height": region4, "mon": monitor_number}
        sct_img = sct.grab(monitor)
        return mss.tools.to_png(sct_img.rgb, sct_img.size, output=None)


def screenshotfullscreen(location):
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(location)


def click(coordinate_dict: list, name):
    region = coordinate_dict[name].split(',')
    temp = int(region[0])
    pyautogui.click(temp, int(region[1]))

def displayMousePosition():
    pyautogui.displayMousePosition()


def match(new_pic, original_pic):
    image1 = cv.imread(original_pic)
    image2 = cv.imread(new_pic)
    difference1 = cv.subtract(image1, image2)
    difference2 = cv.subtract(image2, image1)
    if (not np.any(difference1)) & (not np.any(difference2)):
        return 1
    else:
        return 0


def super_match(coordinate_dict, name) -> bool:
    temp_region = coordinate_dict[name].split(',')
    screenshot(temp_region[0], temp_region[1], temp_region[2],
               temp_region[3], './screenshot/' + name + '_new.png')
    return match('./screenshot/' + name + '_new.png',
                 './screenshot/original/' + name + '_original.png')


def black_match(new_pic, original_pic):
    image1 = cv.imread(original_pic)
    image2 = cv.imread(new_pic)
    difference = cv.subtract(image2, image1)
    return not np.any(difference)


def super_black_match(coordinate_dict, name) -> bool:
    temp_region = coordinate_dict[name].split(',')
    screenshot(temp_region[0], temp_region[1], temp_region[2],
               temp_region[3], './screenshot/' + name + '_new.png')
    return black_match('./screenshot/' + name + '_new.png',
                       './screenshot/original/' + name + '_original.png')


def rgb_match(new_pic, original_pic):
    im_new = Image.open(new_pic)
    rgb_im_new = im_new.convert('RGB')
    r1, g1, b1 = rgb_im_new.getpixel((0, 0))

    im_original = Image.open(original_pic)
    rgb_im_original = im_original.convert('RGB')
    r2, g2, b2 = rgb_im_original.getpixel((0, 0))

    if (r1 == r2) & (g1 == g2) & (b1 == b2):
        return 1
    else:
        return 0


def super_rgb_match(coordinate_dict, name) -> bool:
    temp_region = coordinate_dict[name].split(',')
    screenshot(temp_region[0], temp_region[1], temp_region[2],
               temp_region[3], './screenshot/' + name + '_new.png')
    return rgb_match('./screenshot/' + name + '_new.png',
                     './screenshot/original/' + name + '_original.png')


def ocr(img_path) -> str:
    # read the image
    img = cv.imread(img_path)

    # convert the BGR image to HSV colour space
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # set the lower and upper bounds for the green hue
    lower = np.array([10, 100, 100])
    upper = np.array([30, 255, 255])

    # create a mask for green colour using inRange function
    mask = cv.inRange(hsv, lower, upper)

    invertimg = cv.bitwise_not(mask)

    custom_config = r'--oem 3 --psm 6'

    return pytesseract.image_to_string(invertimg, lang='eng', config=custom_config).strip()


def ocr_basic(img_path) -> str:
    # read the image
    img = cv.imread(img_path)

    custom_config = r'--oem 3 --psm 6'

    # return pytesseract.image_to_string(img, lang='eng')
    return pytesseract.image_to_string(img, lang='eng', config=custom_config).strip()

def ocr_basic_rotate(img_path) -> str:
    # read the image
    img = cv.imread(img_path)
    rot_img = cv.rotate(img,cv.ROTATE_90_COUNTERCLOCKWISE)

    custom_config = r'--oem 3 --psm 6'

    # return pytesseract.image_to_string(img, lang='eng')
    return pytesseract.image_to_string(rot_img, lang='eng', config=custom_config).strip()


def super_ocr(coordinate_dict, name, method):
    location = './screenshot/' + name + '_new.png'
    temp = coordinate_dict[name].split(',')
    screenshot(temp[0], temp[1], temp[2], temp[3], location)
    if method == 'basic':
        return ocr_basic(location)
    else:
        return ocr(location)


def ocr_invert(img_path):
    # read the image
    img = cv.imread(img_path)

    # convert the BGR image to HSV colour space
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # set the lower and upper bounds for the green hue
    lower = np.array([10, 100, 100])
    upper = np.array([30, 255, 255])

    # create a mask for green colour using inRange function
    mask = cv.inRange(hsv, lower, upper)

    cv.imwrite('./screenshot/color.png', mask)

    return mask


def match_template(image, template_img):
    cv.matchTemplate(image, template_img, 0)


def random_action(probability):
    action = random.choices((Action.Raise.name, Action.Call.name,
                            Action.Check.name, Action.Fold.name), probability)[0]
    return action

def random_action_no_name(probability):
    action = random.choices((Action.Raise, Action.Call,
                            Action.Check, Action.Fold), probability)[0]
    return action
    
def random_check(probability):
    return random.choices((Action.Bet.name, Action.Check.name), [1 - probability, probability])[0]

def get_focus(computer_team, bot_no):
    win = gw.getWindowsWithTitle(computer_team+str(bot_no))[0]
    count = 0
    while win.isActive == False:
        if count >= 10:
            break
        count += 1
        try:
            win.activate()
        except:
            sleep(1)
            if bot_no == 1:
                pyautogui.click(220, 57)
            elif bot_no == 2:
                pyautogui.click(700, 57)
            elif bot_no == 3:
                pyautogui.click(1180, 57)
            elif bot_no == 4:
                pyautogui.click(1660, 57)
            elif bot_no == 5:
                pyautogui.click(2151, 57)
            elif bot_no == 6:
                pyautogui.click(2620, 57)
            elif bot_no == 7:
                pyautogui.click(3100, 57)
            elif bot_no == 8:
                pyautogui.click(3594, 57)
    if win.isActive == True:
        return True
    else:
        return False
