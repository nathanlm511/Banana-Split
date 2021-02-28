import cv2, numpy as np
import sys
import time
import math
import copy

start = time.time()

def get_new(old):
    new = np.ones(old.shape, np.uint8)
    cv2.bitwise_not(new,new)
    return new

def get_dist(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# print(f"get_dist((15,20),(42,87)): {get_dist((15,20),(42,87))}")

def get_ang(line1, line2):
    x1,y1 = (line1[0][0] - line1[1][0], line1[0][1] - line1[1][1])
    x2,y2 = (line2[1][0] - line2[0][0], line2[1][1] - line2[0][1])
    abs1 = math.sqrt(x1**2 + y1**2)
    abs2 = math.sqrt(x2**2 + y2**2)
    ang = math.acos((x1*x2 + y1*y2)/(abs1*abs2)) * 180/np.pi
    if ang == math.nan:
        ang = 90
    return ang

# cap = cv2.VideoCapture(1)

# ret = True

# while (ret):
# ret, orig = cap.read()


# these constants are carefully picked
# originals
# MORPH = 9
# CANNY = 84
# HOUGH = 25
# testing
MORPH = 9 # Started at 9
CANNY = 100 # Started at 84
HOUGH = 40 # Started at 25

def get_corner_points(orig_img):
    orig = orig_img.copy()
    img = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    cv2.GaussianBlur(img, (3,3), 0, img)


    # this is to recognize white on white
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(MORPH,MORPH))
    dilated = cv2.dilate(img, kernel)

    edges = cv2.Canny(dilated, 0, CANNY, apertureSize=3)

    lines = cv2.HoughLinesP(edges, 100,  3.14/180, HOUGH)
    # lines = cv2.HoughLinesP(edges, 100,  6.14/180, HOUGH)

    failed_to_find_lines = False
    try:
        for line in lines:
            line = line[0]
            # print(f"line: {line}")
            cv2.line(edges, (line[0], line[1]), (line[2], line[3]),
                            (255,0,0), 2, 8)
    except:
        print("Hough detector found no lines.")
        failed_to_find_lines = True

    if not failed_to_find_lines:
        # finding contours
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_TC89_KCOS)
        contours = filter(lambda cont: cv2.arcLength(cont, False) > 1000, contours)
        contours = filter(lambda cont: cv2.contourArea(cont) > 10000, contours)
        
        contours_copy = copy.deepcopy(contours)

        # Take only contour with centroid closest to center if more than one contour
        cnt_moments = []
        cnt_areas = []
        for cont in contours_copy:
            cnt_moments.append(cv2.moments(cont))
            cnt_areas.append(cv2.contourArea(cont))
            
        
        # Find centroids
        cnt_centroids = []
        if len(cnt_moments) > 1:
            for moment in cnt_moments:
                cx = int(moment['m10']/moment['m00'])
                cy = int(moment['m01']/moment['m00'])
                cnt_centroids.append((cx, cy))
        # print(f"image w,h,c: {(orig.shape[0], orig.shape[1], orig.shape[2])}")
        # Calculate center of image
        img_center = (orig.shape[1]/2, orig.shape[0]/2)
        
        
        # print(img_center)
        # print(f"cnt_centroids: {cnt_centroids}")

        # Take centroid with best score based on distance from center and area
        scores = np.array([])
        for i, point in enumerate(cnt_centroids):
            moment = cnt_moments[i]
            dist_to_center = get_dist(point, img_center)
            score = (1000 - dist_to_center) * 700 # Scale based on observed moment sizes and distances
            score += cnt_areas[i]
            scores = np.append(scores, score)
            # print(f"cnt_areas[{i}]: {cnt_areas[i]}")
            # print(f"dist to center[{i}]: {dist_to_center}")
        # print(f"scores: {scores}")
        
        # print(f"np.argmax(scores): {np.argmax(scores)}")
        
        # print(f"contours: {contours}")
        
        
        # simplify contours down to polygons
        outlines = []
        count = 0
        for i,cont in enumerate(contours):
            count += 1
            # if i == np.argmax(scores): # Best contour
            outline = cv2.approxPolyDP(cont, 30, True).copy().reshape(-1, 2)
            outlines.append(outline)
        if len(cnt_moments) > 1:
            outline = outlines[np.argmax(scores)] # Outline of best contour
        # print(count)
        # print(f"outline: {outline}")
        print(f"outline size before pruning: {len(outline)}")
        # print(f"Starting proximity based removal")
        
        
        
        #
        #   REMOVE POINTS BASED ON PROXIMITY
        #
            
        # Now prune based on proximity of each point to other points
        
        # Need to find a threshold value to compare to. This will change between images
        # For now set to constant
        # Score threshold should also be determined dynamically
        prox_threshold = 170
        
        for point in outline:
            cv2.circle(orig, tuple(point), prox_threshold, (255, 255, 0), 2)
            
        # # Then remove points if they are too close to another point
        prox_mask = np.ones(len(outline))
        outline_cpy = outline
        # points_to_remove = True
        # cur_point_index = 0
        # index = 0
        # while (points_to_remove):
        #     print(f"curpointindex: {cur_point_index}")
        #     # print(f"outline: {outline}")
        #     remove_this_point = False
        #     cur_point = outline[cur_point_index]
        #     print(f"cur_point: {cur_point}")
        #     all_greater_than_thresh = True
        #     # Check distance betweeen all other points
        #     for point in outline[cur_point_index + 1:]:
        #         print(f"point: {point}, dist: {get_dist(cur_point, point)}")
        #         if get_dist(cur_point, point) < prox_threshold:
        #             remove_this_point = True
        #             all_greater_than_thresh = False
        #             break
        #     print(f"remove this pint: {remove_this_point}")
        #     if remove_this_point:
        #         print(f"DELETING AT {cur_point_index}")
        #         outline = np.delete(outline, cur_point_index, axis=0)
        #         prox_mask[index] = 0
        #     else:
        #         print(f"incrementing cur_point_index")
        #         cur_point_index += 1

        #     if cur_point_index == len(outline): # We have searched the entire list
        #         break

        #     index += 1

        # Another way to remove points based on proximity: check all points for all other points and
        # remove any that are close to at least a few others
        proximities_all_points = []
        for i, point in enumerate(outline):
            proximities_this_point = []
            for other_point in outline:
                if other_point is not point:
                    dist = get_dist(point, other_point)
                    if dist < prox_threshold:
                        proximities_this_point.append(dist)
            proximities_all_points.append(proximities_this_point)
            
        # print(f"Drawing point numbers")
        
        for i, point in enumerate(outline):
            cv2.putText(orig, str(i), tuple(point), color=(2, 2, 2), thickness=4,fontScale=1.5, fontFace=cv2.FONT_ITALIC)
        
        # See if proximities warrant removal
        # Removal status is given based on a combination of number of nearby points and how close those points are
        # Score threshold should also be determined dynamically
        for i, proximities_for_point in enumerate(proximities_all_points):
            len_score = (len(proximities_for_point)-1)**3 * 5
            sum_score = sum(proximities_for_point)
            score = len_score + sum_score
            if score > 200:
                prox_mask[i] = 0
            # print(f"i, len, sum prox: {i}: {len(proximities_for_point), sum(proximities_for_point)}")
            # print(f"i, len, sum, total score: {i}: {len_score}, {sum_score}, {score}")
        
        
        points_deleted_by_prox = outline[prox_mask == 0]
        outline = outline[prox_mask == 1]

        
        # Highlight points removed by proximity pruning in yellow
        for i, deleted in enumerate(points_deleted_by_prox):
            cv2.circle(orig, tuple(deleted), 7, (0, 255, 255), 10)
            cv2.putText(orig, "proximity", tuple(deleted), color=(200, 200, 200), thickness=2,fontScale=1, fontFace=cv2.FONT_ITALIC)
            
        print(f"outline size after prox pruning: {len(outline)}")
        
        # print(f"Drawing remaining points")
        # print(outline)
        for point in outline: # Highlight points remaining after proximity pruning in blue
            cv2.circle(orig, tuple(point), 7, (255, 0, 0), 10)
            cv2.putText(orig, "after prox", tuple(point), color=(200, 200, 200), thickness=2,fontScale=1, fontFace=cv2.FONT_ITALIC)

        # print(f"Starting angle based removal")
        
        
        # print(f"Drawing border lines")
        orig_height = orig.shape[0]
        orig_width = orig.shape[1]
        x_thresh, y_thresh = 10,10
        top_left = (x_thresh,y_thresh)
        bottom_left = (x_thresh,orig_height-y_thresh)
        top_right = (orig_width-x_thresh,y_thresh)
        bottom_right = (orig_width-x_thresh,orig_height-y_thresh)
        cv2.line(orig, top_left, bottom_left, (0, 0, 255), thickness=3)
        cv2.line(orig, bottom_left, bottom_right, (0, 0, 255), thickness=3)
        cv2.line(orig, bottom_right, top_right, (0, 0, 255), thickness=3)
        cv2.line(orig, top_right, top_left, (0, 0, 255), thickness=3)
        
        #
        #   REMOVE POINTS CLOSE TO EDGE
        #
        edge_mask = np.ones(len(outline))
        for i, point in enumerate(outline):
            if point[0] < x_thresh or point[1] < y_thresh or point[0] > orig_width-x_thresh or point[1] > orig_height-y_thresh:
                # Out of bounds
                edge_mask[i] = 0
        
        removed_by_edge_mask = outline[edge_mask == 0]
        outline = outline[edge_mask == 1]
        
        print(f"outline size after border pruning: {len(outline)}")
        
        #
        #   REMOVE POINTS BASED ON ANGLE
        #
        
        # Make lines between adjacent sets of points
        lines = []
        prev_point = (-1,-1)
        first_point = (-1,-1)
        first_point_bool = True
        for i,point in enumerate(outline):
            point = tuple(point)
            if first_point_bool:
                first_point_bool = False
                first_point = point
            else:
                lines.append([prev_point, point])
            prev_point = point
                
        lines.append([prev_point, first_point]) # Last line is first point and last point
        # for line in lines:
        #     print(line)
            
        # outline: all points [x, y]
        # lines: list of two points [(x1, y1), (x2, y2)]
            
        # Calculate angle between every set of two connected lines
        angles = []
        prev_line = [(-1,-1), (-1,-1)]
        first_line = [(-1,-1), (-1,-1)]
        first_line_bool = True
        for line in lines:
            if first_line_bool:
                first_line_bool = False
                first_line = line
            else:
                # print(f"calculating angle between: {prev_line, line}")
                angles.append(get_ang(prev_line, line))
            prev_line = line
        # print(f"calculating angle between: {prev_line, first_line}")
        angles.append(get_ang(prev_line, first_line))
        
        # # Draw angles
        # print(f"angles: {angles}")
        # for i, ang in enumerate(angles):
        #     if i < len(angles)-1:
        #         cv2.circle(orig, tuple(outline[i+1]), 5, (255, 0, 0), 10)
        #         cv2.putText(orig, str(int(angles[i])), tuple(outline[i+1]), color=(200, 200, 200), thickness=2,fontScale=.9, fontFace=cv2.FONT_ITALIC)
        #     else:
        #         cv2.circle(orig, tuple(outline[0]), 5, (255, 0, 0), 10)
        #         cv2.putText(orig, str(int(angles[len(angles)-1])), tuple(outline[0]), color=(200, 200, 200), thickness=2,fontScale=.9, fontFace=cv2.FONT_ITALIC)

        # Create mask for pruning points in outline
        angle_mask = np.ones(len(outline))
        for i, point in enumerate(outline):
            # print(f"point in outline: {point}")
            if i > 0:
                ang = angles[i-1]
            else:
                ang = angles[0]
            if ang < 80 or ang > 140: # Threshold
                angle_mask[i] = 0
                
        # print(angle_mask)
        deleted_points = outline[angle_mask == 0]
        outline = outline[angle_mask == 1]
        
        print(f"outline size after angle pruning: {len(outline)}")
        
        for i, deleted in enumerate(deleted_points):
            cv2.circle(orig, tuple(deleted), 7, (0, 0, 255), 10)
            cv2.putText(orig, "angle", tuple(deleted), color=(200, 200, 200), thickness=2,fontScale=1, fontFace=cv2.FONT_ITALIC)
        
        # print(f"outlineup here {outline}")
        if len(outline) != 4:
            # Any remaining points too close to each other are combined
            combine_mask = np.zeros(len(outline))
            neighbors_all = []
            for i, point in enumerate(outline):
                neighbors_this = []
                for j, other_point in enumerate(outline):
                    if other_point is not point:
                        dist = get_dist(point, other_point)
                        if dist < prox_threshold:
                            combine_mask[i] = 1
                            neighbors_this.append(j)
                neighbors_all.append(neighbors_this)
                
                    
            # # Make sure all neighbors_this contain separate indices
            # indices = []
            # for neighbors_this in neighbors_all:
            #     neighbors_this_size = neighbors_this.size
            #     mask3 = np.ones(neighbors_this_size).astype(int)
            #     for i, index in enumerate([neighbors_this]):
            #         if index not in indices:
            #             indices.append(index)
            #         else:
            #             mask3[i] = 0
            #     neighbors_this = np.asarray(neighbors_this)
            #     print(f"mask3.size: {mask3.size}")
            #     print(f"neighbors_this.size: {neighbors_this.size}")
            #     print(f"neighbors_this: {neighbors_this}")
            #     print(f"type(mask3): {type(mask3)}")
            #     print(f"type(neighbors_this): {type(neighbors_this)}")
            #     if neighbors_this.size != 1:
            #         neighbors_this = neighbors_this[mask3 == 1]
            
            # neighbors_all_size = neighbors_all.size
            # mask4 = np.ones(neighbors_all_size).astype(int)
            # for i, neighbors_this in enumerate(neighbors_all):
            #     if neighbors_this.shape == 1:
            #         mask4[i] = 0
            # mask4 = [int(x) for x in mask4]
            # neighbors_all = neighbors_all[mask4]
            
            indices = []
            mask4 = []
            for i, list in enumerate(neighbors_all):
                if len(list) < 2 or list in indices:
                    mask4.append(0)
                else:
                    indices.append(list)
                    mask4.append(1)
            neighbors_all = [neighbors for tf, neighbors in zip(mask4, neighbors_all) if tf == 1]    

            # for neighbors in neighbors_all:
            #     print("new")
            #     for ind in neighbors:
            #         print(ind)

            avg_locs = []
            associated_points = []
            for neighbors_this in neighbors_all:
                if len(neighbors_this) > 1:
                    # print(f"new set")
                    x_locations = []
                    y_locations = []
                    count = 0
                    pts = []
                    for index in neighbors_this:
                        pts.append(index)
                        # print(f"index: {index}")
                        count += 1
                        x_locations.append(outline[int(index),0])
                        y_locations.append(outline[int(index),1])
                    # print(f"sum x sumy : {sum(x_locations)}, {sum(y_locations)}")
                    avg_locs.append([int(sum(x_locations)/count), int(sum(y_locations)/count)])
                    associated_points.append(pts)
            # print(f"avg locations: {avg_locs}")
            # print(f"associated pts: {associated_points}")
            
            near_mask = np.ones(len(outline))
            for pts in associated_points:
                for index in pts:
                    near_mask[index] = 0
            
            # Create new points
            new_pts = []
            for i, location in enumerate(avg_locs):
                new_pts.append(location)
            
            # Mask outline
            # outline = [point for tf, point in zip(near_mask, outline) if tf == 1]   
            outline = outline[near_mask == 1]
            
            # print(f"outline: {outline}")
            # Add new points to outline
            for new_pt in new_pts:
                # print(f"newpt: {[new_pt]}")
                outline = np.append(outline, [new_pt], axis=0)
                
            # print(f"outline: {outline}")
        
        # Make this outline the only outline in outlines
        outlines = []
        outlines.append(outline)
        
        # Draw contours onto new image
        new = get_new(img) # show only contours on new
        cv2.drawContours(orig, outlines,-1,(0,255,0),2)
        dist_thresh = 100
        for point in outline:
            # cv2.circle(orig, (point[0], point[1]), dist_thresh, (255,0,0), 2)
            # print(f"point: {point}")
            pass
            # while len(outline) > 4: # Prune points until we get best rectangle
            #     pass
        cv2.drawContours(new, outlines,-1,(0,255,0),1)
        # cv2.GaussianBlur(new, (9,9), 0, new)
        new = cv2.Canny(new, 0, CANNY, apertureSize=3)
        
        return outline


    print(f"time taken to find corners: {time.time() - start}")
    # cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    orig = cv2.resize(orig, (600,840))
    # dilated = cv2.resize(dilated, (600,840))
    # edges = cv2.resize(edges, (600,840))
    # new = cv2.resize(new, (600,840))
    # cv2.imshow('original', orig)
    # cv2.waitKey(0)
    # cv2.imshow('dilated (after morph)', dilated)
    # cv2.waitKey(0)
    # cv2.imshow('edges (after drawing lines)', edges)
    # cv2.waitKey(0)
    # cv2.imshow('new (after drawing contours)', new)
    # cv2.waitKey(0)
    # if cv2.waitKey(33) == ord('x'):
            # break
    return None
            
# img = cv2.imread('unmodified-images/receipt3_unmod4.jpg')

# points = get_corner_points(img)

# print(f"num points: {len(points)}")

# for point in points:
#     cv2.circle(img, tuple(point), 30, (255, 255, 255), 3)

# img = cv2.resize(img, (600,840))

# cv2.imshow('points found', img)

# cv2.waitKey(0)

# cv2.destroyAllWindows()


if __name__ == "__main__":
    pass