import numpy as np
import cv2
from os.path import join
import matplotlib.pyplot as plt

def stream_to_program_mac(run_program, ith_cam=0):
 
  cap = cv2.VideoCapture(ith_cam)
  # cap.set(3, 640)
  # cap.set(4, 420)

  while(cap.isOpened()):
    _, img = cap.read()
    run_program(img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  cap.release()
  cv2.destroyAllWindows()

def rotate(arr, n):
  """
  Rotation of an array by n positions
  @param arr: array to be rotated
  @param n: int (-len(arr) > n < len(arr)) number of positions to rotate arr
  """
  return arr[n:] + arr[:n]

def euclidean(p1, p2):
  """
  Calculate the euclidean distance between two points
  @param p1: touple of x, y
  @param p2: touple of x, y
  """
  return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def avg_cluser(pts, pts_inds):
  """
  Calculates the center most point of a cluster
  @param pts: array of pts in a cluster
  @param pts_inds: array of point indicies which correspond to some contour set
  @return a touple containing an array of 
  """
  x_tot = 0
  y_tot = 0
  # sum up the x and y distances
  for pt in pts:
    x_tot += pt[0]
    y_tot += pt[1]
  # get the mean position of
  avg_pt = np.array([[x_tot//len(pts), y_tot//len(pts)]])
  # init vars for calculating closest point to mean
  min_dist = float('inf')
  min_ind = None
  # calculate closest point to center of mass
  for i, pt in zip(range(len(pts)), pts):
    dist = euclidean(pt, avg_pt[0])
    if dist < min_dist:
      min_dist = dist
      min_ind = i
  return np.array([[pts[min_ind][0], pts[min_ind][1]]]), pts_inds[min_ind]

def cluster(pts, pts_inds, max_distance):
  """
  Clusters points within some max_distance
  @param pts: 
  @param pts_inds:
  @param max_distance: 
  @return touple containing 1) clusters of points,
      and 2) clusters containing mappings of (1)
  """

  # initialization
  pt_labels = {0: 0}
  clusters = [[pts[0][0]]]
  clusters_inds = [[pts_inds[0][0]]]

  # for every point, compare to every other point
  for i in range(0, len(pts)):
    found_home = False
    for j in range(i+1, len(pts)):
      p1 = pts[i][0]
      p2 = pts[j][0]
      p1_i = pts_inds[i][0]
      p2_i = pts_inds[j][0]
      # check if within max dist
      if euclidean(p1, p2) <= max_distance:
        # if not in some cluster, create a new cluster
        if i not in pt_labels:
          pt_labels[i] = len(clusters)
          clusters.append([p1])
          clusters_inds.append([p1_i])

        # add p2 to same cluster as p1
        clusters[pt_labels[i]].append(p2)
        clusters_inds[pt_labels[i]].append(p2_i)
        pt_labels[j] = pt_labels[i]

        found_home = True
    # if no other point near this point, create new cluster
    if not found_home and i not in pt_labels and i != 0:
      pt_labels[i] = len(clusters)
      clusters.append([p1])
      clusters_inds.append([p1_i])

  return clusters, clusters_inds

def get_betas(defect_to_hulls):
  """
  calculate angle between two defects and a hull point
  @param defect_to_hulls array: formatted as an array of three touples of
      (defect1, hull point, defect2)
  @return array of angles (betas) corresponding to the defect_to_hulls
  """
  beta = []
  for p1, p2, p3 in defect_to_hulls:
    a = euclidean(p1, p2)
    b = euclidean(p2, p3)
    c = euclidean(p3, p1)

    beta.append(int(np.arccos((a**2 + b**2 - c**2)/(2*a*b))*(180/np.pi)))

  return beta

def count_fingers(img):
  max_cluster_dist = 100
  finger_count  = 0
  defect_to_hull = []
  beta = []
  _, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  if len(contours) < 1:
    # if no contours, return early
    return finger_count, defect_to_hull, beta

  # hand contour should be the bigest contour
  hand_contour = list(sorted(contours, key=lambda x: len(x)))[-1]
  
  cvx_hull = cv2.convexHull(hand_contour, False)
  cvx_hull_inds = cv2.convexHull(hand_contour, returnPoints=False)

  # calculate the rough hull
  rough_hull, rough_hull_inds = cluster(cvx_hull, cvx_hull_inds, max_cluster_dist)
  rough_hull, rough_hull_inds = zip(*np.array(list(map(avg_cluser, rough_hull, rough_hull_inds))))

  # rotate both arrays to make sure they line up for calculating the defect_to_hull
  rough_hull = np.array(rotate([np.array([[x[0][0], x[0][1]]]) for x in rough_hull], 2))
  rough_hull_inds = np.array(rotate([np.array([x]) for x in rough_hull_inds], 2))

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
    
    # calculate angles of the insides of our defect_to_hull
    beta = get_betas(defect_to_hull)

    finger_count = sum(list(map(lambda x: int(x > 8 and x < 50), beta)))

  return finger_count, defect_to_hull, beta

def display(img, d2h, beta):
  finger_count = 0
  if len(d2h) > 0 and len(beta) > 0:
    for i in range(len(d2h)):
      p1, p2, p3 = d2h[i]
      cv2.circle(img, (p1[0], p1[1]), 15, (255,255,0), -1)
      cv2.circle(img, (p2[0], p2[1]), 15, (255,0,255), -1)
      cv2.putText(img, '{} deg.'.format(beta[i]), (p2[0], p2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
      cv2.line(img,(p1[0],p1[1]),(p2[0],p2[1]),(0,255,255),5)
      cv2.line(img,(p2[0],p2[1]),(p3[0],p3[1]),(255,255,0),5)

    finger_count = sum(list(map(lambda x: int(x > 8 and x < 50), beta)))
  cv2.putText(img, 'FINGER COUNT: {}'.format(finger_count), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2, cv2.LINE_AA)

  return img

def pre_process_img(img):
  """
  Do any preprocessing for a given image
  @param img: img formatted as numpy array to be processed
  """
  img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
  _, img = cv2.threshold(img, 100, 255, 1)
  kernel = np.ones((5,5),np.uint8)
  img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=2)
  return img

def fingers_on_command_line(img):
  imgo = img
  img = pre_process_img(imgo)
  f_count, d2h, beta = count_fingers(img)
  display(imgo, d2h, beta)
  cv2.imshow('img', imgo)
  
  print('Number of Fingers', f_count)

def main():
  stream_to_program_mac(fingers_on_command_line, ith_cam=1)

if __name__ == '__main__':
  main()