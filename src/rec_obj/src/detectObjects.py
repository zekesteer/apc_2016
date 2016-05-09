import numpy as np
import cv2
from matplotlib import pyplot as plt
import keypoints_management
import glob
import scipy as sp
import math



def matchImageWithDatabase(imgDest, databasePath, imagesPath, extensionImages, objectNames):

    MAX_ERROR_MATCHING = 10

    sift = cv2.SIFT()


    kpDest_sift, desDest_sift = sift.detectAndCompute(imgDest, None)

    img_sift = cv2.drawKeypoints(imgDest, kpDest_sift)

    matches_sift_global_name = []

    error_sift_global = []

    M_sift_global = []

    mask_sift_global = []

    matches_sift_global_goodPoints = []

    kp_matched_image_sift_global = []

    name_matched_image_sift_global = []


    tifCounter = len(glob.glob1(databasePath, "*.key_sift"))
    counter = 1

    if len(kpDest_sift) > 0 :
        for objSource in objectNames:

            minError_sift = float("inf")


            for file in glob.glob1(databasePath, objSource + "*.key_sift"):

#                print "Matching image with image in database number", counter, "out of", tifCounter

                kpSrc_sift, desSrc_sift = keypoints_management.loadKeypointsDatabase(databasePath + file)

                M_sift, mask_sift, error_sift, matches_goodPoints_sift = matchImages(imagesPath + file[:-9] + extensionImages,\
                    kpDest_sift, desDest_sift, kpSrc_sift, desSrc_sift)


                if(error_sift is not -1 and error_sift < minError_sift):
                    minError_sift = error_sift
                    maxM_sift = M_sift
                    maxMask_sift = mask_sift
                    maxMatchesGoodPoints_sift = matches_goodPoints_sift
                    maxKp_matched_image_sift = kpSrc_sift
                    maxName_matched_image_sift = file[:-9]

                counter = counter + 1




            if minError_sift < MAX_ERROR_MATCHING:
                matches_sift_global_name.append(objSource)
                error_sift_global.append(minError_sift)
                M_sift_global.append(maxM_sift)
                mask_sift_global.append(maxMask_sift)
                matches_sift_global_goodPoints.append(maxMatchesGoodPoints_sift)
                kp_matched_image_sift_global.append(maxKp_matched_image_sift)
                name_matched_image_sift_global.append(maxName_matched_image_sift)



    return name_matched_image_sift_global, kp_matched_image_sift_global, kpDest_sift, matches_sift_global_goodPoints, matches_sift_global_name, error_sift_global, M_sift_global, mask_sift_global



def matchImages(imgSrcPath, kpDest, desDest, kpSrc, desSrc, isORB = False):

    error = -1

    if len(kpDest) == 0 or len(kpSrc) == 0 :
        M = None
        mask = None
        good = []

        return M, mask, error, good

    MIN_MATCH_COUNT = 10

    good = []

    if not isORB:

        # FLANN_INDEX_KDTREE = 0
        # index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        # search_params = dict(checks=50)

        # bf = cv2.FlannBasedMatcher(index_params, search_params)
        # matches = bf.knnMatch(desSrc,desDest, k=2)


        # try:
        #     for m, n in matches:
        #         if m.distance < 0.7*n.distance:
        #             good.append(m)

        #     # drawMatch2("test", imgDstPath, kpDest, imgSrcPath, kpSrc, np.asarray(good), None)



        bf = cv2.BFMatcher(crossCheck=True)
        matches = bf.match(desSrc,desDest)

        dist = [m.distance for m in matches]
        thres_dist = (sum(dist) / len(dist)) * 0.7

        for m in matches:
            if m.distance < thres_dist:
                good.append(m)



        # except ValueError:

        #     M = None
        #     mask = None

        #     return M, mask, error, good

    else:
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(desSrc,desDest)

        dist = [m.distance for m in matches]
        thres_dist = (sum(dist) / len(dist)) * 0.7

        for m in matches:
            if m.distance < thres_dist:
                good.append(m)
    
    

    if len(good) >= MIN_MATCH_COUNT:
        src_pts = np.float32([ kpSrc[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kpDest[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 1.0)
        inliers = np.array(mask.ravel().tolist(), dtype=np.bool)

        nMatches = np.sum(inliers)

        if nMatches >= MIN_MATCH_COUNT:

        	error = computeReprojectionError(src_pts, dst_pts, M, inliers)

        else:
        	M = None
        	mask = None
        	good = []
        	error = -1


    else:
        M = None
        mask = None

    return M, mask, error, good


def computeReprojectionError(ptsSrc, ptsDest, M, inliersMask):

    error = 0

    projected = cv2.perspectiveTransform(ptsSrc,M)
    # print projected

    # print projected[0]
    # print projected[0,0]

    countGoodMatch = 0
    for idx, inlier in enumerate(inliersMask):
        if inlier:
            countGoodMatch = countGoodMatch + 1
            error = error + math.sqrt(math.pow(projected[idx,0,0] - ptsDest[idx,0,0], 2) + math.pow(projected[idx,0,1] - ptsDest[idx,0,1], 2))

    return error/countGoodMatch



def drawMatch(nameWindow, imgDestPath, kpDest, imgSrcPath, kpSrc, M, mask, pointMatches):



    img1 = cv2.imread(imgSrcPath)
    img2 = cv2.imread(imgDestPath)

    matchesMask = mask.ravel().tolist()

    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    pts = np.float32([ [0,0],[0,h1-1],[w1-1,h1-1],[w1-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.CV_AA)


    view = sp.zeros((max(h1, h2), w1 + w2, 3), sp.uint8)
    view[:h1, :w1, :] = img1  
    view[:h2, w1:, :] = img2
    view[:, :, 1] = view[:, :, 0]  
    view[:, :, 2] = view[:, :, 0]

    for idx, m in enumerate(pointMatches):

        if mask[idx]:

            # draw the keypoints
            # print m.queryIdx, m.trainIdx, m.distance
            color = tuple([sp.random.randint(0, 255) for _ in xrange(3)])

            cv2.line(view, (int(kpSrc[m.queryIdx].pt[0]), int(kpSrc[m.queryIdx].pt[1])) , \
                (int(kpDest[m.trainIdx].pt[0] + w1), int(kpDest[m.trainIdx].pt[1])), color)

    cv2.namedWindow(nameWindow, cv2.WINDOW_NORMAL)
    cv2.imshow(nameWindow, view)



def drawMatch2(nameWindow, imgDestPath, kpDest, imgSrcPath, kpSrc, pointMatches, colors):

    cv2.destroyAllWindows()

    # print "1"

    img1 = cv2.imread(imgSrcPath)
    img2 = cv2.imread(imgDestPath)

    # cv2.imshow("1", img1)
    # cv2.imshow("2", img2)

    # print "2"

    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    # print "3"

    view = sp.zeros((max(h1, h2), w1 + w2, 3), sp.uint8)

    # print "3.1"

    view[:h1, :w1, :] = img1  

    # print "3.2"

    view[:h2, w1:, :] = img2

    # print "4"

    view[:, :, 1] = view[:, :, 0]  
    view[:, :, 2] = view[:, :, 0]

    # print "BEFORE LOOP"

    for idx, m in enumerate(pointMatches):

        if len(pointMatches) == 2:

            for n in m:

                # draw the keypoints
                if colors is None:
                    color = tuple([sp.random.randint(0, 255) for _ in xrange(3)])
                else:
                    color = colors[idx]

                cv2.line(view, (int(kpSrc[n.queryIdx].pt[0]), int(kpSrc[n.queryIdx].pt[1])) , \
                    (int(kpDest[n.trainIdx].pt[0] + w1), int(kpDest[n.trainIdx].pt[1])), color)

        else:

            # draw the keypoints
            if colors is None:
                color = tuple([sp.random.randint(0, 255) for _ in xrange(3)])
            else:
                color = colors[idx]

            cv2.line(view, (int(kpSrc[m.queryIdx].pt[0]), int(kpSrc[m.queryIdx].pt[1])) , \
                (int(kpDest[m.trainIdx].pt[0] + w1), int(kpDest[m.trainIdx].pt[1])), color)

    # print "AFTER LOOP"
    cv2.namedWindow(nameWindow, cv2.WINDOW_NORMAL)
    cv2.imshow(nameWindow, view)
    cv2.waitKey()



def main(imDest):

    objectsToRecognisePath = "./"
    database = objectsToRecognisePath + "keypoints/"
    imagesPath = objectsToRecognisePath + "poses/"
    extensionTrainingImages = ".png"


    print "MATCHING OBJECT:", file
    print

    name_matched_image_sift_global, kp_matched_image_sift_global, kpDest_sift, matches_sift_global_goodPoints, matches_sift_global_name, error_sift_global, M_sift_global, mask_sift_global = matchImageWithDatabase(imDest, database, imagesPath, extensionTrainingImages)

    print


    print "Matches by SIFT:"
    for idx, e in enumerate(matches_sift_global_name):
        print "\t", e,  "\t", error_sift_global[idx], "reprojection error"

    print



    for idx, e in enumerate(matches_sift_global_name):
        drawMatch(file + " best matched with " + imagesPath + name_matched_image_sift_global[idx] + " by SIFT", \
            objectsToRecognisePath + file, kpDest_sift, \
            imagesPath + name_matched_image_sift_global[idx] + extensionTrainingImages, \
            kp_matched_image_sift_global[idx], M_sift_global[idx], mask_sift_global[idx], matches_sift_global_goodPoints[idx])

        cv2.waitKey()
