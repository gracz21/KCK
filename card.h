#ifndef CARD_H
#define CARD_H

#include <string>
#include "opencv2/core/core.hpp"

using namespace std;
using namespace cv;

class card {
public:
	card(string col, string t, string f);
//private:
	string color;
	string type;
	Mat img;
};

#endif