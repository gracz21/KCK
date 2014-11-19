#include "card.h"
#include "opencv2/highgui/highgui.hpp"

card::card(string kol, string t, string f) {
	color = kol;
	type = t;
	img = imread("patterns\\" + f, CV_LOAD_IMAGE_GRAYSCALE);
}