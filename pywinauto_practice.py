import pyautogui
from pywinauto.application import Application
import pywinauto.mouse as mouse
import pywinauto.keyboard as keyboard
import time
import sys

def init():
    app = Application(backend="uia").start(r"C:/Program Files (x86)/GRETECH/GOMPlayer/GOM.EXE")
    dig = app.window(title_re=".*곰플레이어")

init()

## 파일 열기
dig.type_keys('{F2}')

## 검증 파일 재생
app.파일_열기.Edit13.type_keys("sample.avi{ENTER}")

## 특정 구간 이동 후 화면 캡쳐
pyautogui.hotkey('g')

time.sleep(3)

dig.Edit.type_keys("00:02:00{ENTER}")
pyautogui.hotkey('ctrl','e')

##dig.print_control_identifiers()
## 화면 캡쳐한 파일과 준비해둔 샘플과 이미지 유사도 비교

##dig.set_focus()
##dig.click_input(button='right')
##dig.PopupMenu.menu().get_menu_path('파일 열기\tF2')[0].click_input()