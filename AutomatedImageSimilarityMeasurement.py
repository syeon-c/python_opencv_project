import cv2, numpy as np
import matplotlib.pylab as plt
import pyautogui
import tkinter
from tkinter import *
from tkinter import filedialog
from pywinauto.application import Application
import time
import os
import threading


def selectDir():
    global fileDirectory
    # tkinter 이용해서 사용할 파일 디렉토리 경로 선택
    root = Tk()
    root.title("Select Directory")
    root.geometry("300x300+100+100")
    root.resizable(False, False)

    root.dirName = filedialog.askdirectory()

    if len(os.listdir(root.dirName)) == 0:
        tkinter.messagebox.showwarning("Value Error", "해당 경로에 파일이 존재하지 않습니다")
        os.exit()

    # fileDirectory 변수에 사용할 파일이 담긴 경로 입력
    fileDirectory = root.dirName

    root.mainloop()


# resultDirectory: 곰플 캡쳐본이 저장되는 경로 (\ -> / 로 변경 필수)
# sampleDirectory: 곰플 캡처본과 이미지 유사도를 비교할 이미지 파일이 있는 폴더 경로
# videoTime: 검증할 특정 video 타임 구간
resultDirectory = "C:/Users/gre508/Desktop/AutomationScript_test/Kaze_Feature_Matching_project/img"
sampleDirectory = "C:/Users/gre508/Desktop/AutomationScript_test/Kaze_Feature_Matching_project/sample_img"
fileDirectory = ""
videoTime = "00:03:00"

thread = threading.Thread(target=selectDir)
thread.daemon = True
thread.start()

time.sleep(15)

fileList = os.listdir(fileDirectory)

# 해당 경로의 파일 자동 실행
for file in fileList:

    fileName = fileDirectory + "/" + file
    print(file)

    # 파일 실행 및 설정
    app = Application(backend="uia").start("C://Program Files (x86)//GOM//GOMPlayer//GOM.EXE " + fileName)
    dig = app.window(title_re=".*곰플레이어")

    dig.wait('ready', timeout=10)

    # 특정 구간 이동 후 화면 캡쳐
    # 곰플레이서 캡처 화면 저장 경로 > resultDirectory 사전 설정
    pyautogui.hotkey('g')
    dig.Edit.type_keys(videoTime + "{ENTER}")
    pyautogui.hotkey('ctrl', 'e')

    time.sleep(3)

    # 캡쳐 파일 이름 변경
    # 캡쳐된 파일은 일괄적으로 qc_source.png로 변경
    # 검증에 쓰일 sample 다른 경로에 sample_source.png로 미리 저장 필요
    fileList = os.listdir(resultDirectory)
    oldFileName = os.path.join(resultDirectory, fileList[0])
    newFilename = os.path.join(resultDirectory, file.split('.')[0] + '_qc_source.png')
    os.rename(oldFileName, newFilename)

    sample_source_location = os.path.join(sampleDirectory, file.split('.')[0] + '_sample_source.png')

    time.sleep(3)

    # 샘플 이미지 set 불러오기
    sample_source = cv2.imread(sample_source_location)
    qc_source = cv2.imread(newFilename)

    imgs = [sample_source, qc_source]
    hists = []

    # 이미지 그래프 생성 및 histogram 계산
    for i, img in enumerate(imgs):
        plt.subplot(1, len(imgs), i + 1)
        if i == 0:
            plt.title(fileName + '_sample_source')
        elif i == 1:
            plt.title(fileName + '_qc_source')
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

    # 생성된 캡쳐파일 삭제
    os.remove(newFilename)

    # 곰플레이어 종료
    os.system("taskkill /f /im GOM.EXE")

    time.sleep(5)
