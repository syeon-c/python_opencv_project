## 이미지 유사도 측정을 이용한 곰플레이어 기본검증

#### 1. 개요 및 시나리오 설명

​	a. 개요

		- 곰플레이어 기본 검증 시, 확장자 별로 올바르게 재생되는지 확인하기 위해 이미지 유사도를 이용한 자동화 스크립트를 작성했습니다.
		- 현재 스크립트는 미리 준비해 둔 영상의 임의 샘플 캡쳐본과 비교해 이미지 유사도 특정 수치를 넘게 되면 Pass 되도록 구현이 되었습니다.
		- 1개의 파일에 대해서만 스크립트가 실행 되며, 추후 반복문을 이용해 여러 확장자 별 파일을 일괄적으로 테스트 할 수 있도록 보완 할 계획입니다.



- Language: Python
- Library: opencv / pywinauto / pyautogui / numpy / matplotlib



​	b. 스크립트 시나리오

	- 곰플레이어 실행
	- 스크립트에서 지정한 파일이 재생되고, 특정 구간으로 이동 (구간 설정 가능)
	- 이동된 구간의 화면 자동 캡쳐
	- 캡쳐된 화면과 준비해 둔 샘플 캡쳐본의 이미지 유사도 측정



#### 2. 파이썬 라이브러리 설치(터미널/cmd 창에서 진행)

- opencv(Open Source Computer Vision) : 실시간 컴퓨터 비전을 목적으로 한 프로그래밍 라이브러리 

  => **pip install opencv-python**

- pywinauto : Window OS 프로그램을 키보드 마우스 입력 없이 자동으로 제어할 수 있는 python 라이브러리 

  => **pip install pywinauto**

- pyautogui : 키보드와 마우스를 자동으로 제어할 수 있는 python 라이브러리 

  => **pip install pyautogui**

- numpy : 행렬이나 배열을 쉽게 처리할 수 있도록 지원하는 python 라이브러리

  => **pip install numpy** 

- matplotlib : 그래프를 시각적으로 표시할 수 있도록 해주는 python 라이브러리

  => **pip install matplotlib**



#### 3. 주요 변수 및 함수 설명

- 변수

  - fileDirectory : 곰플레이어에서 자동 화면캡쳐 파일이 저장되는 directory 경로
  - sampleDirectory : sample 캡쳐본이 있는 경로
  - fileName : 검증 할 영상 파일의 경로
  - videoTime : 검증 할 영상에서 캡쳐할 구간으로 이동할 시간

- opencv histogram 비교 함수

  - cv2.HISTCMP_CORREL : 상관관계 (1 : 완전 일치, -1 : 완전 불일치, 0 : 무관계) 

    => 0~1 사이에서 1에 가까운 수치일 수록 두 이미지는 유사함

  - cv2.HISTCMP_CHISQR : 카이제곱 (0 : 완전 일치, 무한대 : 완전 불일치)

    => 0에 가까운 수치일 수록 두 이미지는 유사함

  - cv2.HISTCMP_INTERSECT : 교차 (1 : 완전 일치, 0 : 완전 불일치)

    => 1에 가까운 수치일 수록 두 이미지는 유사함

  - cv2.HISTCMP_BHATTACHARYYA : Bhattacharyya 거리 ( 0 : 완전 일치, 1 : 완전 불일치)

    => 0에 가까운 수치일 수록 두 이미지는 유사함



#### 4. 사전 준비

- 코드 수정

  ![코드수정](C:\Users\gre508\Desktop\코드수정.png)

  - fileDirectory의 경로를 곰플레이어에서 화면 캡쳐 파일이 저장되는 경로로 변경
  - sampleDirectory의 경로를 샘플 캡쳐본이 존재하는 경로로 변경 (filedirectory의 경로와 다르게 지정)
  - fileName을 재생하고자 하는 파일의 경로로 변경
  - videoTime을 이동하고자 하는 구간으로 시간 변경 (hh:mm:ss)
  - 모든 경로의 역슬래시는 슬래시로 변경

- sampleDirectory 경로 내에 'sample_source.png' 이름으로 샘플 캡쳐본 배치

- 곰플레이어 내 단축키 확인 ( 곰플레이어 - 프로그램 정보 - 단축키 목록에서 확인 )

  - G : 이동할 위치 직접 입력
  - ctrl + e : 화면을 파일로 저장



#### 5. 발생 가능 이슈 및 개선사항

- 발생 가능 이슈
  - histogram의 구성을 비교해 이미지의 유사도를 측정하기 때문에 구성이 비슷하면 이미지가 유사하지 않아도 pass 처리 될 수 있음 (반대도 가능) - 알고리즘 변경해야 함
  - fileName 변수에 경로를 넣지 않고 파일 자체의 이름을 넣고 있어서, '파일 열기' 했을 때 파일을 찾지 못할 수 있음 - '파일 열기' 로직을 cmd에서 실행시키는 방향으로 수정 가능 **(수정 완료)**
  - 준비된 sample_source의 이미지와 자동으로 생성되는 qc_source의 이미지가 미세하게 다를 수 있음 - 동일한 시간 안에서도 영상의 화면이 미세하게 바뀌기 때문



#### 6. 시연 영상

![img](C:\Users\gre508\Desktop\시연영상.gif)

