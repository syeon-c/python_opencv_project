import cv2, numpy as np
import matplotlib.pylab as plt
import pyautogui
from pywinauto.application import Application
import time
import os

## 영상 파일 이름 / 사진 디렉토리(곰플 캡쳐본 저장 경로) 및 시간 설정 변수
### fileDirectory: 곰플 캡쳐본이 저장되는 경로 (\ -> / 로 변경 필수)
### fileName: 검증할 영상 파일 이름 (해당 영상은 반드시 바탕화면에 배치)
### videoTime: 검증할 특정 video 타임 구간

fileDirectory = "C:/Users/gre508/Desktop/GomPlayer_Script/Kaze_Feature_Matching_project/img"
fileName = "sample.avi"
videoTime = "00:04:50"

## 파일 실행 및 설정
app = Application(backend="uia").start(r"C:/Program Files (x86)/GRETECH/GOMPlayer/GOM.EXE")
dig = app.window(title_re=".*곰플레이어")

## 파일 열기
dig.type_keys('{F2}')

## 검증 파일 재생
app.파일_열기.Edit13.type_keys(fileName+"{ENTER}")

## 특정 구간 이동 후 화면 캡쳐
pyautogui.hotkey('g')
dig.Edit.type_keys(videoTime+"{ENTER}")
pyautogui.hotkey('ctrl','e')

time.sleep(5)

## 캡쳐 파일 이름 변경
### 캡쳐된 파일은 일괄적으로 qc_source.png로 변경
### 검증에 쓰일 sample 파일은 동일한 경로에 sample_source.png로 미리 저장 필요
fileList = os.listdir(fileDirectory)
print(fileList)
oldFileName = os.path.join(fileDirectory, fileList[0])
newFilename = os.path.join(fileDirectory, 'qc_source.png')
sampleSourceDirectory = os.path.join(fileDirectory, 'sample_source.png')
os.rename(oldFileName, newFilename)

time.sleep(5)

## 샘플 이미지 set 불러오기
sample_source = cv2.imread(sampleSourceDirectory)
qc_source = cv2.imread(newFilename)

imgs = [sample_source, qc_source]
hists = []

## 이미지 그래프 생성 및 histogram 정규화
for i, img in enumerate(imgs):
    plt.subplot(1,len(imgs),i+1)
    if i==0:
        plt.title('sample_source')
    elif i==1:
        plt.title('qc_source')    
    plt.axis('off')
    plt.imshow(img[:,:,::-1])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hist = cv2.calcHist([hsv], [0,1], None, [180,256], [0,180,0,256])

    cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
    hists.append(hist)

query = hists[0]
methods = {'CORREL': cv2.HISTCMP_CORREL, 'CHISQR': cv2.HISTCMP_CHISQR,
'INTERSECT': cv2.HISTCMP_INTERSECT, 'BHATTACHARYYA': cv2.HISTCMP_BHATTACHARYYA}

print('=============함수별 이미지 유사도 결과============')

## histogram 비교를 통한 이미지 유사도 측정
for j, (name, flag) in enumerate(methods.items()):
    print('%-10s'%name, end='\t')
    for i, (hist, img) in enumerate(zip(hists, imgs)):
        ret = cv2.compareHist(query, hist, flag)
        if flag == cv2.HISTCMP_INTERSECT:
            ret = ret/np.sum(query)
        if flag == cv2.HISTCMP_CORREL or flag == cv2.HISTCMP_INTERSECT:
            retRatio = ret * 100
            if retRatio > 60:
                result = 'PASS'
            else:
                result = 'FAIL'    
        print("img%d:%7.2f"% (i+1, ret), end='\t')
        if i==1:
            print(result,end='\t')        
    print()
plt.show()

## 생성된 캡쳐파일 삭제
os.remove(newFilename)
