#include "card.h"
#include <iostream>
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

card::card(string kol, string t, string f) {
	color = kol;
	type = t;
	img = imread("patterns\\" + f, CV_LOAD_IMAGE_GRAYSCALE);
	if(!img.data)
		cout << "Nie udalo sie wczytac pliku!\n";
}

Mat card::getImage() {
	return img;
}

string card::name() {
	return type + " " + color;
}