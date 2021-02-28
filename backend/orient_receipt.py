import cv2
import numpy as np
import math

def get_dist(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def orient_receipt(orig_points, img, orig_img_shape):
    desired_height, desired_width = img.shape[0], img.shape[1]
    orig_height, orig_width = orig_img_shape[0], orig_img_shape[1]
    
    # Get lengths between sides
    lengths = []
    prev_pt = (-1, -1)
    first_pt = (-1, -1)
    first_point = True
    for point in orig_points:
        if first_point:
            first_point = False
            first_pt = point
        else:
            lengths.append(get_dist(point, prev_pt))
        prev_pt = point
    lengths.append(get_dist(first_pt, prev_pt))
    
    # print(f"lengths: {lengths}")
    # Make two pairs of lengths (horizontal and vertical lengths of receipt)
    length_pairs = []
    dists = []
    first_len = lengths[0]
    for other_len in lengths[1:]:
        dists.append(abs(first_len - other_len))
    closest_len_index = dists.index(min(dists))+1
    pair1 = (first_len, lengths[closest_len_index])
    del lengths[0]
    del lengths[closest_len_index-1]
    pair2 = (lengths[0], lengths[1])
    
    shorter_pair = ()
    longer_pair = ()
    if pair1[0] < pair2[0]:
        shorter_pair = pair1
        longer_pair = pair2
    else:
        shorter_pair = pair2
        longer_pair = pair1
    
    receipt_ratio = shorter_pair[0] / longer_pair[0] # width/height
        
    # des_top_left = cv2.KeyPoint(0,0,1)
    # des_top_right = cv2.KeyPoint(desired_width,0,1)
    # des_bottom_left = cv2.KeyPoint(0,desired_height,1)
    # des_bottom_right = cv2.KeyPoint(desired_width,desired_height,1)

    des_top_left = [0,0]
    des_top_right = [desired_width,0]
    des_bottom_left = [0,desired_height]
    des_bottom_right = [desired_width,desired_height]
    des_points = np.float32([des_top_left, des_top_right, des_bottom_left, des_bottom_right])
    
    orig_top_left = (0,0)
    orig_top_right = (orig_width,0)
    orig_bottom_left = (0,orig_height)
    orig_bottom_right = (orig_width,orig_height)
    
    
    # Find points closest to corners and match with desired points
    closest_to_top_left = ()
    dists = []
    for point in orig_points:
        dists.append(get_dist(orig_top_left, point))
    closest_to_top_left = orig_points[dists.index(min(dists))]
    # print(closest_to_top_left)
    
    closest_to_top_right = ()
    dists = []
    for point in orig_points:
        dists.append(get_dist(orig_top_right, point))
    closest_to_top_right = orig_points[dists.index(min(dists))]
    # print(closest_to_top_right)
    
    closest_to_bottom_left = ()
    dists = []
    for point in orig_points:
        dists.append(get_dist(orig_bottom_left, point))
    closest_to_bottom_left = orig_points[dists.index(min(dists))]
    
    closest_to_bottom_right = ()
    dists = []
    for point in orig_points:
        dists.append(get_dist(orig_bottom_right, point))
    closest_to_bottom_right = orig_points[dists.index(min(dists))]
    
    start_points = [closest_to_top_left, closest_to_top_right, closest_to_bottom_left, closest_to_bottom_right]

    # Convert to format usable by findHomography
    # des_points = np.array(des_points)
    # des_points = np.float32(des_points[:, np.newaxis, :])
    
    start_points = np.array(start_points)
    start_points = np.float32(start_points)
    
    # print(f"start_points: {start_points}")
    # print(f"des_points: {des_points}")
    
    # print(f"longer pair: {longer_pair}, shorter pair: {shorter_pair}")
    
    # Find homography
    # h, mask = cv2.findHomography(orig_points, des_points)
    h = cv2.getPerspectiveTransform(start_points, des_points)

    # Use homography
    img_warped = cv2.warpPerspective(img, h, (desired_width, desired_height))
    return img_warped, receipt_ratio
