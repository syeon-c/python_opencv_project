import cv2, numpy as np
import matplotlib.pylab as plt
import pyautogui
from pywinauto.application import Application
import pywinauto.keyboard as keyboard
import time

## 파일 이름 및 시간 설정 변수
fileName = "sample.avi"
videoTime = "00:03:00"

## 파일 실행 및 설정
app = Application(backend="uia").start(r"C:/Program Files (x86)/GRETECH/GOMPlayer/GOM.EXE")
dig = app.window(title_re=".*곰플레이어")

## 파일 열기
dig.type_keys('{F2}')

## 검증 파일 재생
app.파일_열기.Edit13.type_keys(fileName+"{ENTER}")

## 특정 구간 이동 후 화면 캡쳐
pyautogui.hotkey('g')

time.sleep(3)

dig.Edit.type_keys(videoTime+"{ENTER}")
pyautogui.hotkey('ctrl','e')

#-- 샘플 이미지 set 불러오기
sample_source = cv2.imread(r'C:/Users/gre508/Desktop/GomPlayer_Script/Kaze_Feature_Matching_project/img/sample.avi_000120411.png')
qc_source = cv2.imread(r'C:/Users/gre508/Desktop/GomPlayer_Script/Kaze_Feature_Matching_project/img/Screenshot_1.png')

#-- query 이름으로 사진 띄워줌
cv2.imshow('query', sample_source)

imgs = [sample_source, qc_source]
hists = []

for i, img in enumerate(imgs):
    plt.subplot(1,len(imgs),i+1)
    plt.title('img%d'% (i+1))
    plt.axis('off')
    plt.imshow(img[:,:,::-1])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hist = cv2.calcHist([hsv], [0,1], None, [180,256], [0,180,0,256])

    cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
    hists.append(hist)

query = hists[0]
methods = {'CORREL': cv2.HISTCMP_CORREL, 'CHISQR': cv2.HISTCMP_CHISQR,
'INTERSECt': cv2.HISTCMP_INTERSECT, 'BHATTACHARYYA': cv2.HISTCMP_BHATTACHARYYA}

for j, (name, flag) in enumerate(methods.items()):
    print('%-10s'%name, end='\t')
    for i, (hist, img) in enumerate(zip(hists, imgs)):
        ret = cv2.compareHist(query, hist, flag)
        if flag == cv2.HISTCMP_INTERSECT:
            ret = ret/np.sum(query)
        print("img%d:%7.2f"% (i+1, ret), end='\t')
    print()
plt.show()            