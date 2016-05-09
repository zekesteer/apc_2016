import cv2
import os
import numpy as np
import cPickle as pickle
import glob


def loadKeypointsDatabase(filename):

    keypoints_database = pickle.load( open(filename, "rb" ))
    kp1, desc1 = unpickle_keypoints(keypoints_database)
    return kp1, desc1


def saveKeypointsDatabase(points, filename):
    pickle.dump(points, open(filename, "wb"))


def pickle_keypoints(keypoints, descriptors):
    i = 0
    temp_array = []
    for point in keypoints:
        temp = (point.pt, point.size, point.angle, point.response, point.octave,
        point.class_id, descriptors[i])     
        i = i + 1
        temp_array.append(temp)
    return temp_array

def unpickle_keypoints(array):
    keypoints = []
    descriptors = []

    for point in array:
        temp_feature = cv2.KeyPoint(
            x=point[0][0],
            y=point[0][1],
            _size=point[1], 
            _angle=point[2], 
            _response=point[3], 
            _octave=point[4], 
            _class_id=point[5])
        temp_descriptor = point[6]
        keypoints.append(temp_feature)
        descriptors.append(temp_descriptor)
    return keypoints, np.array(descriptors)


def process_image(imageName, maskName, resultName):

    img = cv2.imread(imageName, cv2.CV_LOAD_IMAGE_GRAYSCALE)

    if maskName is not None:
        mask = cv2.imread(maskName, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        img[np.where((mask > 128))] = 0

    if not os.path.isfile(resultName + ".key_surf"):

        # SURF
        surf = cv2.SURF()
        k_surf, des_surf = surf.detectAndCompute(img, None)

#        img_surf = cv2.drawKeypoints(img, k_surf)
#        cv2.imwrite(resultName + "_keypoints_SURF.jpeg", img_surf)

        points_surf = pickle_keypoints(k_surf, des_surf)
        saveKeypointsDatabase(points_surf, resultName + ".key_surf")


    if not os.path.isfile(resultName + ".key_sift"):
    
        # SIFT
        sift = cv2.SIFT()
        k_sift, des_sift = sift.detectAndCompute(img, None)

#        img_sift = cv2.drawKeypoints(img, k_sift)
#        cv2.imwrite(resultName + "_keypoints_SIFT.jpeg", img_sift)

        points_sift = pickle_keypoints(k_sift, des_sift)
        saveKeypointsDatabase(points_sift, resultName + ".key_sift")


    if not os.path.isfile(resultName + ".key_orb"):

        # ORB
        orb = cv2.ORB()
        k_orb, des_orb = orb.detectAndCompute(img, None)

#        img_orb = cv2.drawKeypoints(img, k_orb)
#        cv2.imwrite(resultName + "_keypoints_ORB.jpeg", img_orb)

        points_orb = pickle_keypoints(k_orb, des_orb)
        saveKeypointsDatabase(points_orb, resultName + ".key_orb")



def main():

    objectsToRecognisePath = "./"
    poses = objectsToRecognisePath + "poses/"
    database = objectsToRecognisePath + "keypoints/"
    extensionImages = ".png"

    tifCounter = len(glob.glob1(poses, "*" + extensionImages))
    counter = 1

    for file in os.listdir(poses):
        if file.endswith(extensionImages):

            print "Processing image number", counter, "out of", tifCounter

            filename = file[:-4]
            process_image(
                poses + file, 
                None, 
                database + filename)

            counter = counter + 1
    

if __name__ == "__main__":
    main()
