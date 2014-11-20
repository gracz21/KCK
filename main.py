from skimage import data, filter, morphology
from skimage.feature import (match_descriptors, corner_harris,
                             corner_peaks, ORB, plot_matches)

def load_pattenrs(patterns, descriptor_extractor):
    i = 1
    while i < 11:
        tmp = data.imread('pattern (' + str(i) + ').jpg', as_grey=True)
        tmp **= 2.0
        tmp = filter.canny(tmp, sigma=3.0)
        tmp = morphology.dilation(tmp, morphology.disk(2))
        descriptor_extractor.detect_and_extract(tmp)
        obj_desc = descriptor_extractor.descriptors
        patterns.append(obj_desc)
        i += 1

def load_scenes(scenes, descriptor_extractor):
    i = 1
    while i < 10:
        tmp = data.imread('scene (' + str(i) + ').jpg', as_grey=True)
        tmp **= 2.0
        tmp = filter.canny(tmp, sigma=3.0)
        tmp = morphology.dilation(tmp, morphology.disk(2))
        descriptor_extractor.detect_and_extract(tmp)
        scen_desc = descriptor_extractor.descriptors
        scenes.append(scen_desc)
        i += 1


def recognize(patterns, scenes, cards):
    for j in scenes:
        best_match = 0
        id = 0
        i = 0
        while i < 10:
            matches = match_descriptors(j, patterns[i], cross_check=True)
            if matches.size > best_match:
                id = i
                best_match = matches.size
            i += 1
        print 'Karta to: ', cards[id]


def main():
    cards = ['dama karo', 'szostka kier', 'trojka karo', 'siodemka pik', 'piatka kier',
             'krol trefl', 'czarny joker', 'czerwony joker', 'dwojka trefl', 'as pik']
    patterns = []
    scenes = []
    descriptor_extractor = ORB()

    load_pattenrs(patterns, descriptor_extractor)
    load_scenes(scenes, descriptor_extractor)

    recognize(patterns, scenes, cards)

if __name__ == '__main__':
    main()