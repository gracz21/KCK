#include <iostream>
#include <vector>
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/calib3d/calib3d.hpp"
#include "opencv2/nonfree/nonfree.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "card.h"
#include "consts.h"

const int numOfCards = 10;
const int numOfScenes = 9;

void readPatterns(vector<card*> &patterns) {
	for(int i = 0; i < numOfCards; i++) {
		ostringstream ss;
		ss << i;
		card *tmp = new card(colors[i], types[i], ss.str()+".jpg");
		patterns.push_back(tmp);
	}
}

void readScens(vector<Mat> &scenes) {
	for(int i = 0; i < numOfScenes; i++) {
		ostringstream ss;
		ss << i;
		Mat tmp = imread("scenes//" + ss.str() + ".jpg", CV_LOAD_IMAGE_GRAYSCALE);
		scenes.push_back(tmp);
	}
}

string recognize(Mat scene, vector<card*> patterns) {
	int minHessian = 400;
	SurfFeatureDetector detector(minHessian);
	std::vector<KeyPoint> keypoints_object, keypoints_scene;

	int j;
	int id = 0, mostCorr = 0;
	for(j = 0; j < 3; j++) {
		Mat object = patterns.at(j)->getImage();	
		detector.detect(object, keypoints_object);
		detector.detect(scene, keypoints_scene);

		SurfDescriptorExtractor extractor;
		Mat descriptors_object, descriptors_scene;
		extractor.compute(object, keypoints_object, descriptors_object);
		extractor.compute(scene, keypoints_scene, descriptors_scene);
		
		FlannBasedMatcher matcher;
		vector<DMatch> matches;
		matcher.match(descriptors_object, descriptors_scene, matches);
		double max_dist = 0; double min_dist = 100;

		for(int i = 0; i < descriptors_object.rows; i++){
			double dist = matches[i].distance;
			if(dist < min_dist) min_dist = dist;
			if(dist > max_dist) max_dist = dist;
		}
		//printf("-- Max dist : %f \n", max_dist );
		//printf("-- Min dist : %f \n", min_dist );

		std::vector< DMatch > good_matches;

		for(int i = 0; i < descriptors_object.rows; i++ )
			if(matches[i].distance < 3*min_dist) good_matches.push_back(matches[i]);

		if(mostCorr < good_matches.size()) {
			id = j;
			mostCorr = good_matches.size();
		}
		cout << "Iteracja: " << j << ", correct: " << good_matches.size() <<endl;
		Mat img_matches;
		drawMatches(object, keypoints_object, scene, keypoints_scene,
					good_matches, img_matches, Scalar::all(-1), Scalar::all(-1),
					vector<char>(), DrawMatchesFlags::NOT_DRAW_SINGLE_POINTS);

		std::vector<Point2f> obj;
		std::vector<Point2f> scene;

		for(int i = 0; i < good_matches.size(); i++) {
			obj.push_back(keypoints_object[good_matches[i].queryIdx].pt);
			scene.push_back(keypoints_scene[good_matches[i].trainIdx].pt);
		}
		Mat H = findHomography(obj, scene, CV_RANSAC);

		std::vector<Point2f> obj_corners(4);
		obj_corners[0] = cvPoint(0,0); obj_corners[1] = cvPoint(object.cols, 0);
		obj_corners[2] = cvPoint(object.cols, object.rows);
		obj_corners[3] = cvPoint(0, object.rows);
		std::vector<Point2f> scene_corners(4);

		perspectiveTransform(obj_corners, scene_corners, H);

		line(img_matches, scene_corners[0] + Point2f(object.cols, 0), scene_corners[1] + Point2f(object.cols, 0), Scalar(0, 255, 0), 4);
		line(img_matches, scene_corners[1] + Point2f(object.cols, 0), scene_corners[2] + Point2f(object.cols, 0), Scalar( 0, 255, 0), 4);
		line(img_matches, scene_corners[2] + Point2f(object.cols, 0), scene_corners[3] + Point2f(object.cols, 0), Scalar( 0, 255, 0), 4);
		line(img_matches, scene_corners[3] + Point2f(object.cols, 0), scene_corners[0] + Point2f(object.cols, 0), Scalar( 0, 255, 0), 4);

		imshow( "Good Matches & Object detection", img_matches );
		waitKey(0);
		keypoints_object.clear();
		keypoints_scene.clear();
	}
	return patterns.at(id)->name();
}

int main() {
	vector<card*> patterns;
	vector<Mat> scenes;
	readPatterns(patterns);
	readScens(scenes);
	int i;
	for(i = 0; i < 1; i++)
		cout << "Scena " << i << " : " << recognize(scenes.at(i), patterns) << endl;
	for(i = 0; i < numOfCards; i++)
		delete patterns.at(i);
}