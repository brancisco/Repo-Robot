import numpy as np
import cv2
from os.path import join
import matplotlib.pyplot as plt
from FingerCounter import *

def count_fingers_display_steps(img, oimg, writeloc):
  max_cluster_dist = 20
  finger_count  = 0
  defect_to_hull = []
  beta = []
  _, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  if len(contours) < 1:
    # if no contours, return early
    return finger_count, defect_to_hull, beta

  # hand contour should be the bigest contour
  hand_contour = list(sorted(contours, key=lambda x: len(x)))[-1]

  img_contours = cv2.drawContours(oimg, [hand_contour], -1, (0,255,0), 3)
  cv2.imwrite(join(writeloc, 'step3.jpg'), img_contours)
  plt.imshow(img_contours)
  plt.show()

  cvx_hull = cv2.convexHull(hand_contour, False)
  cvx_hull_inds = cv2.convexHull(hand_contour, returnPoints=False)

  img_hull = cv2.drawContours(oimg, [cvx_hull], -1, (255,0,255), 3)
  cv2.imwrite(join(writeloc, 'step4.jpg'), img_hull)
  plt.imshow(img_hull)
  plt.show()

  # calculate the rough hull
  rough_hull, rough_hull_inds = cluster(cvx_hull, cvx_hull_inds, max_cluster_dist)
  rough_hull, rough_hull_inds = zip(*np.array(list(map(avg_cluser, rough_hull, rough_hull_inds))))

  # rotate both arrays to make sure they line up for calculating the defect_to_hull
  rough_hull = np.array(rotate([np.array([[x[0][0], x[0][1]]]) for x in rough_hull], 2))
  rough_hull_inds = np.array(rotate([np.array([x]) for x in rough_hull_inds], 2))

  for p in rough_hull:
    p = p[0]
    img_hull = cv2.circle(img_hull,(p[0], p[1]), 10, (0,255,255), -1)
  cv2.imwrite(join(writeloc, 'step5.jpg'), img_hull)
  plt.imshow(img_hull)
  plt.show()

  # check if there are any defects
  try:
    cvx_defects = cv2.convexityDefects(hand_contour, rough_hull_inds)
  except Exception as e:
    cvx_defects = None
    print('error', e)

  defect_to_hull = []
  if type(cvx_defects) != type(None):
    # calculate the defect_to_hull array (this is array of three touples (defect1,hull,defect2))
    for i in range(len(cvx_defects)-1):
      start, end, defect, _ = cvx_defects[i][0]
      _, _, next_def, _ = cvx_defects[i+1][0]

      d2h = list(map(lambda x: hand_contour[x][0], [defect, end, next_def]))
      defect_to_hull.append(d2h)

    for p1, p2, p3 in defect_to_hull:
      img_hull = cv2.circle(img_hull,(p1[0], p1[1]), 10, (255,0,255), -1)
    img_hull = cv2.circle(img_hull,(p3[0], p3[1]), 10, (255,0,255), -1)
    cv2.imwrite(join(writeloc, 'step6.jpg'), img_hull)
    plt.imshow(img_hull)
    plt.show()

    for i in range(len(defect_to_hull)):
      p1, p2, p3 = defect_to_hull[i]
      cv2.line(img_hull,(p1[0],p1[1]),(p2[0],p2[1]),(0,255,255),5)
      cv2.line(img_hull,(p2[0],p2[1]),(p3[0],p3[1]),(255,255,0),5)
    cv2.imwrite(join(writeloc, 'step7.jpg'), img_hull)
    plt.imshow(img_hull)
    plt.show()

    beta = get_betas(defect_to_hull)

    for i in range(len(defect_to_hull)):
      p1, p2, p3 = defect_to_hull[i]
      cv2.putText(img_hull, '{} deg.'.format(beta[i]), (p2[0], p2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imwrite(join(writeloc, 'step8.jpg'), img_hull)
    plt.imshow(img_hull)
    plt.show()
    # calculate angles of the insides of our defect_to_hull
    
    finger_count = sum(list(map(lambda x: int(x > 8 and x < 50), beta)))
    cv2.putText(img_hull, 'FINGER COUNT: {}'.format(finger_count), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.imwrite(join(writeloc, 'step9.jpg'), img_hull)
    plt.imshow(img_hull)
    plt.show()

  return finger_count, defect_to_hull, beta

def main():
  writeloc = 'figures'
  oimg = cv2.imread(join(writeloc, 'img', 'hand.jpg'))
  cv2.imwrite(join(writeloc, 'step1.jpg'), oimg)
  plt.imshow(oimg)
  plt.show()
  img = pre_process_img(oimg)
  cv2.imwrite(join(writeloc, 'step2.jpg'), img)
  plt.imshow(img, cmap='gray')
  plt.show()
  count_fingers_display_steps(img, oimg, writeloc)


if __name__ == '__main__':
  main()