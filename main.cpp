#include <iostream>
#include <vector>
#include "opencv2/highgui/highgui.hpp"
#include "card.h"
#include "consts.h"

const int numOfScens = 1;

void readPatterns(vector<card*> &patterns) {
	for(int i = 0; i < 52; i++) {
		ostringstream ss;
		ss << i;
		card *tmp = new card(colors[int(i/13)], types[i%13], ss.str());
		patterns.push_back(tmp);
	}
}

void readScens(vector<Mat> &scenes) {
	for(int i = 0; i < numOfScens; i++) {
		ostringstream ss;
		ss << i;
		Mat tmp = imread("scenes//" + ss.str(), CV_LOAD_IMAGE_GRAYSCALE);
		scenes.push_back(tmp);
	}
}

int main() {
	vector<card*> patterns;
	vector<Mat> scenes;
	readPatterns(patterns);
	readScens(scenes);
	for(int i = 0; i < 52; i++)
		delete patterns.at(i);
}