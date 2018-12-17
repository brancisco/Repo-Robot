import numpy as np
import cv2
from os.path import join
import matplotlib.pyplot as plt

def rotate(arr, n):
  return arr[n:] + arr[:n]

def stream(op, path):
 
  cap = cv2.VideoCapture(1)
  # cap.set(3, 640)
  # cap.set(4, 420)

  while(cap.isOpened()):

    _, imgo = cap.read()

    # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # _, img = cv2.threshold(img, 100, 255, 1)
    # kernel = np.ones((5,5),np.uint8)
    # img = cv2.dilate(img, kernel, iterations = 2)
    # img = cv2.erode(img, kernel, iterations = 2)
    
    img = cv2.flip(imgo, 1)
    op(img)
    cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == ord('p'):
      cv2.imwrite(path, imgo)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  cap.release()
  cv2.destroyAllWindows()

def take_photo(cam=1):
  cap = cv2.VideoCapture(cam)
  cap.set(3, 640)
  cap.set(4, 420)
  _, img =  cap.read()
  cap.release()
  return img

def euclidean(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def avg_cluser(pts, pts_inds):
  x_tot = 0
  y_tot = 0
  for pt in pts:
    x_tot += pt[0]
    y_tot += pt[1]
  avg_pt = np.array([[x_tot//len(pts), y_tot//len(pts)]])
  min_dist = float('inf')
  min_ind = None
  for i, pt in zip(range(len(pts)), pts):

    dist = euclidean(pt, avg_pt[0])
    if dist < min_dist:
      min_dist = dist
      min_ind = i
  return np.array([[pts[i][0], pts[i][1]]]), pts_inds[i]





def cluster(pts, pts_inds, max_distance):
  pt_labels = {0: 0}
  clusters = [[pts[0][0]]]
  clusters_inds = [[pts_inds[0][0]]]

  for i in range(0, len(pts)):
    found_home = False
    for j in range(i+1, len(pts)):
      p1 = pts[i][0]
      p2 = pts[j][0]
      p1_i = pts_inds[i][0]
      p2_i = pts_inds[j][0]

      if euclidean(p1, p2) <= max_distance:
        if i not in pt_labels:
          pt_labels[i] = len(clusters)
          clusters.append([p1])
          clusters_inds.append([p1_i])

        clusters[pt_labels[i]].append(p2)
        clusters_inds[pt_labels[i]].append(p2_i)
        pt_labels[j] = pt_labels[i]

        found_home = True
    if not found_home and i not in pt_labels and i != 0:
      pt_labels[i] = len(clusters)
      clusters.append([p1])
      clusters_inds.append([p1_i])
  return clusters, clusters_inds

# def compute_beta(a, b):

def do_stuff(imgo, stream=True):

  img = cv2.cvtColor(imgo, cv2.COLOR_RGB2GRAY)

  _, img = cv2.threshold(img, 100, 255, 1)
  kernel = np.ones((5,5),np.uint8)
  img = cv2.dilate(img, kernel, iterations = 2)
  img = cv2.erode(img, kernel, iterations = 2)

  _, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  hand_contour = list(sorted(contours, key=lambda x: len(x)))[-1]
  
  for i in [100]:
    imgc = cv2.drawContours(imgo, [hand_contour], 0, (0, 255, 0), 5)
    imgc = imgo
    cvx_hull1 = cv2.convexHull(hand_contour, False)
    cvx_hull2 = cv2.convexHull(hand_contour, returnPoints=False)
    rough_hull, rough_hull_inds = cluster(cvx_hull1, cvx_hull2, i)
    
    rough_hull, rough_hull_inds = zip(*np.array(list(map(avg_cluser, rough_hull, rough_hull_inds))))
    rough_hull = np.array(rotate([np.array([[x[0][0], x[0][1]]]) for x in rough_hull], 2))
    rough_hull_inds = np.array(rotate([np.array([x]) for x in rough_hull_inds], 2))

    # imgc = cv2.drawContours(imgc, [rough_hull], 0, (255, 0, 0), 5)
    try:
      cvx_defects = list(reversed(cv2.convexityDefects(hand_contour, rough_hull_inds)))
    except Exception as e:
      cvx_defects = None
      print('error', e)

    defect_to_hull = []
    if type(cvx_defects) != type(None):
      first_start, last_end, last_defect, _ = cvx_defects[0][0]
      first_end, first_defect = last_end, last_defect
      p1, p2, p3 = list(map(lambda x: hand_contour[x], [last_defect, first_end, first_defect]))
      p1, p2, p3 = p1[0], p2[0], p3[0]
      cv2.line(imgc,(p1[0],p1[1]),(p3[0],p3[1]),(255,255,0),5)
      cv2.line(imgc,(p2[0],p2[1]),(p3[0],p3[1]),(0,255,255),5)

      # for cvx_defect in cvx_defects:
      #   start, end, defect, _ = cvx_defect[0]
      #   d2h = list(map(lambda x: hand_contour[x], [last_defect, last_end, defect]))
      #   defect_to_hull.append(d2h)
      #   last_defect = defect
      #   last_end = end

      # defect_to_hull.append(
      #   list(map(lambda x: hand_contour[x], [last_defect, end, first_defect]))
      # )
      # for p1, p2, p3 in defect_to_hull[1:2]:
      #   p1, p2, p3 = p1[0], p2[0], p3[0]
      #   cv2.circle(imgc, (p1[0], p1[1]), 7, (255,255,0), -1)
      #   cv2.line(imgc,(p1[0],p1[1]),(p2[0],p2[1]),(0,255,255),5)
      #   cv2.line(imgc,(p2[0],p2[1]),(p3[0],p3[1]),(255,255,0),5)

      # p1, p2, p3 = defect_to_hull[-1]
      # p1, p2, p3 = p1[0], p2[0], p3[0]
      # cv2.circle(imgc, (p1[0], p1[1]), 7, (255,255,0), -1)
      # cv2.line(imgc,(p1[0],p1[1]),(p2[0],p2[1]),(0,255,255),5)
      # cv2.line(imgc,(p2[0],p2[1]),(p3[0],p3[1]),(255,255,0),5)
      # exit()

      # p1 = hand_contour[start][0]
      # p2 = hand_contour[end][0]
      # cv2.line(imgc, (p2[0],p2[1]),(p3[0],p3[1]),(0,255,255),5)
      # print(defect_to_hull)

    i = 0
    for pt in rough_hull:
      p1, p2 = pt[0]
      cv2.circle(imgc, (p1, p2), 7, (255,0,255), -1)
      cv2.putText(imgc, '{}'.format(i), (p1, p2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
      i += 1

    if not stream:
      plt.imshow(imgc, cmap=plt.get_cmap('gray'))
      plt.title('max dist'+ str(i))
      plt.show()
  return imgc

def main():
  # stream(do_stuff, join('imgs', 'hand2.jpg'))
  img = cv2.imread(join('imgs', 'hand.jpg'))
  do_stuff(img, stream=False)

if __name__ == '__main__':
  main()