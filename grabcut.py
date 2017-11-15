#-*- coding:utf-8 -*-

# GrabCut
# Copyright(C) 2016 Orcuslc
# the executable script.

import sys
import os
import numpy as np
from main import GCClient  # GCClient 만 불러옴 .
import re
import cv2

osname = os.name

nargin = len(sys.argv)   # 옵션의 개수
kn = 1

if nargin < 2:
	raise ImportError('More args needed')   # raise 오류를 일부러 발생시키기 .
elif nargin == 2:
	imgroute = sys.argv[1]
	iteration_count = 1
	component_count = 5
elif nargin == 3:
	imgroute = sys.argv[1]
	iteration_count = sys.argv[2]
	component_count = 5
else:
	imgroute = sys.argv[1]
	iteration_count = sys.argv[2]
	component_count = sys.argv[3]

# if osname == 'nt':
imgname = re.findall(r'\w+\.\w+', imgroute)[0]
imgname = re.findall(r'^\w+', imgname)[0]
# elif osname == 'posix':
	# imgname = re.findall(r'^\S+\.', img[1:])[0][:-1]

if not os.path.isfile(imgroute):
	raise ImportError("Not a valid image")

try:
	img = cv2.imread(imgroute, cv2.IMREAD_COLOR)
except AttributeError:
	raise ImportError("Not a valid image")

output = np.zeros(img.shape, np.uint8)

GC = GCClient(img, component_count)
cv2.namedWindow('output')
cv2.namedWindow('input')
a = cv2.setMouseCallback('input', GC.init_mask)
cv2.moveWindow('input', img.shape[0]+100, img.shape[1]+100)

count = 0
print("Instructions: \n")
print("Draw a rectangle around the object using right mouse button \n")
print('Press N to continue \n')

while True:
	cv2.imshow('output', output)
	cv2.imshow('input', np.asarray(GC.img, dtype=np.uint8))
	k = 0xFF & cv2.waitKey(1)


	if k == 27:
		break
	elif k == ord('s'): # 아스키 코드 변환
		cv2.imwrite('%s_gc.jpg'%(imgname), output)
		print("Result saved as image %s_gc.jpg"%(imgname))
	elif k == ord('n'):
		print(""" For finer touchups, mark foreground and background after pressing keys 0-3
			and again press 'n' \n""")
		if GC.rect_or_mask == 0:
			GC.run()
			GC.rect_or_mask = 1
		elif GC.rect_or_mask == 1:
			GC.iter(1)

	elif k == ord('0'):
		print('Mark background regions with left mouse button \n')
		GC._DRAW_VAL = GC._DRAW_BG
		# output = GC.show(output)

	elif k == ord('1'):
		print('Mark foreground regions with left mouse button \n')
		GC._DRAW_VAL = GC._DRAW_FG
		# output = GC.show(output)

	elif k == ord('2'):
		print('Mark prob. background regions with left mouse button \n')
		GC._DRAW_VAL = GC._DRAW_PR_BG

	elif k == ord('3'):
		print('Mark prob. foreground regions with left mouse button \n')
		GC._DRAW_VAL = GC._DRAW_PR_FG

	elif k == ord('r'):
		GC.__init__(img, component_count)


	FGD = np.where((GC._mask == 1) + (GC._mask == 3), 255, 0).astype('uint8')
	output = cv2.bitwise_and(GC.img2, GC.img2, mask=FGD)  ## 이게 출력하는거다

	# jaejin

	# np.where (arr>0 , 2 , arr) 이면 arr의 원소가 0 보다 크면 2로 출력 작으면 arr원래 원소값 출력
	bgimage = cv2.imread('test/boat.jpg')

	rows , cols, channels = output.shape
	roi = bgimage[0:rows, 0:cols]

	img2gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(img2gray, 10, 255, cv2. THRESH_BINARY)
	mask_inv = cv2.bitwise_not(mask)

	img1_fg = cv2.bitwise_and(output, output, mask=mask)
	img2_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

	#output = cv2.bitwise_and(GC.img2, GC.img2, mask = FGD)  ## 이게 출력하는거다
	#dst = cv2.bitwise_and(GC.img2, GC.img2, mask=FGD)
	dst = cv2.add(img1_fg, img2_bg)
	bgimage[0:rows, 0:cols] = dst

	#output = bgimage
	cv2.imshow('res', bgimage)
	#cv2.waitKey(0)

	if kn == 1:
		print(" 배경삭제 작업 시작 ")
		kn = kn + 1
		if GC.rect_or_mask == 0:
			GC.run()
			GC.rect_or_mask = 1
		elif GC.rect_or_mask == 1:
			GC.iter(1)
		flag = True

	# ---

cv2.destroyAllWindows()