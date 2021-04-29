import cv2, numpy as np
import matplotlib.pylab as plt

source = cv2.imread(r'C:/Users/gre508/Desktop/GomPlayer_Script/Kaze_Feature_Matching_project/img/Screenshot_1.png')
img1 = cv2.imread(r'C:/Users/gre508/Desktop/GomPlayer_Script/Kaze_Feature_Matching_project/img/Screenshot_2.png')
img2 = cv2.imread(r'C:/Users/gre508/Desktop/GomPlayer_Script/Kaze_Feature_Matching_project/img/Screenshot_3.png')

#-- query 이름으로 사진 띄워줌
cv2.imshow('query', source)
cv2.waitKey()

imgs = [source, img1, img2]
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

