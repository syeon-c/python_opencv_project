import os
import shutil
from distutils.dir_util import copy_tree
import cv2, numpy as np
import matplotlib.pylab as plt
import pyautogui
from pywinauto import Application
import time


###########################################
# 스크립트 동작 순서
# 1. 기본 스킨 > 기본 화이트 스킨 변경 후 비교
# 2. 기본 화이트 스킨 > 터치 스킨 변경 후 비교
# 3. 터치 스킨 > 기본 스킨 변경 후 비교
###########################################

def captureScreen(fileName):
    # 캡처 프로그램 실행
    pyautogui.hotkey("winleft", "altleft", "printscreen")
    time.sleep(5)

    tmpList = os.listdir(captureDir)

    # 캡처 이미지 이름 변경
    os.rename(captureDir + "/" + tmpList[0],
              captureDir + "/" + fileName)
    time.sleep(3)

    # 캡처 이미지 위치 testDir 로 이동
    copy_tree(captureDir, testDir)
    time.sleep(3)

    # captureDir 존재하는 파일 제거
    os.remove(captureDir + '/' + fileName)
    time.sleep(3)


def compareImages(sample, test):
    # 샘플 이미지 set 불러오기
    sample_source = cv2.imread(sample)
    qc_source = cv2.imread(test)

    imgs = [sample_source, qc_source]
    hists = []

    # 이미지 그래프 생성 및 histogram 계산
    for i, img in enumerate(imgs):
        plt.subplot(1, len(imgs), i + 1)
        if i == 0:
            plt.title(sample.split('/')[-1] + '_sample_source')
        elif i == 1:
            plt.title(test.split('/')[-1] + '_qc_source')
        plt.axis('off')
        plt.imshow(img[:, :, ::-1])

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

        cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
        hists.append(hist)

    query = hists[0]
    methods = {'CORREL': cv2.HISTCMP_CORREL, 'CHISQR': cv2.HISTCMP_CHISQR,
               'INTERSECT': cv2.HISTCMP_INTERSECT, 'BHATTACHARYYA': cv2.HISTCMP_BHATTACHARYYA}

    print('==============함수별 이미지 유사도 결과=============')

    # histogram 비교를 통한 이미지 유사도 측정
    for j, (name, flag) in enumerate(methods.items()):
        print('%-10s' % name, end='\t')
        for i, (hist, img) in enumerate(zip(hists, imgs)):
            ret = cv2.compareHist(query, hist, flag)
            if flag == cv2.HISTCMP_INTERSECT:
                ret = ret / np.sum(query)
            if flag == cv2.HISTCMP_CORREL or flag == cv2.HISTCMP_INTERSECT:
                retRatio = ret * 100
                if retRatio > 50:
                    result = 'PASS'
                else:
                    result = 'FAIL'
            print("img%d:%7.2f" % (i + 1, ret), end='\t')
            if i == 1:
                print(result, end='\t')
        print()
    plt.show()


# 스킨 변경 순서: 기본_화이트 -> 터치 -> 기본
# sampleDir: 스킨 이미지 유사도 비교할 이미지 샘플 경로
skins = ["BasicWhiteSkin", "TouchSkin", "DefaultSkin"]
sampleDir = "C:/Users/gkdlt_orjarjt/Desktop/AutomationScript_test/GomPlayerSkin/sample"
captureDir = 'C:/Users/gkdlt_orjarjt/Videos/Captures'
testDir = 'C:/Users/gkdlt_orjarjt/Desktop/AutomationScript_test/GomPlayerSkin/test'

for i in range(3):
    fileName = skins[i] + ".png"
    sample = sampleDir + '/' + fileName
    test = testDir + '/' + fileName
    print(sample)
    print(test)

    # 곰플레이어 실행 및 환경 설정 이동
    app = Application(backend="uia").start("C://Program Files (x86)//GOM//GOMPlayer//GOM.EXE ")
    dig = app.window(title_re=".*곰플레이어")
    time.sleep(10)

    # 터치스킨 -> 자동 전체화면 설정 -> 전체화면 해제
    if i == 2:
        pyautogui.hotkey("enter")

    # 환경설정 > 스킨 설정
    pyautogui.hotkey("Alt", "F10")
    time.sleep(3)

    # 스크롤 내리고 스킨 선택
    if i == 0:
        pyautogui.moveTo(1457, 527)
        time.sleep(3)

        pyautogui.drag(0, 150, duration=0.5)
        time.sleep(3)

    elif i == 1:
        pyautogui.moveTo(1457, 527)
        time.sleep(3)

        pyautogui.drag(0, 350, duration=0.5)
        time.sleep(3)

    pyautogui.moveTo(972, 597)
    pyautogui.click(clicks=2)
    time.sleep(3)

    # 스킨 설정 창 닫음
    pyautogui.hotkey("esc")
    time.sleep(3)

    # 선택한 스킨이 적용된 곰플레이어 화면 캡처
    captureScreen(fileName)
    time.sleep(5)

    # 곰플레이어 종료
    os.system("taskkill /f /im GOM.EXE")

    # test 이미지와 sample 이미지 비교 통한 스킨 적용 여부 검사
    compareImages(sample, test)
