from skimage import data, filter, morphology
from skimage.feature import (match_descriptors, corner_harris,
                             corner_peaks, ORB, plot_matches)
import os
from multiprocessing import Pool


def load_pattenrs(patterns, descriptor_extractor):
    listing = os.listdir('patterns')
    for filename in listing:
        print 'Working on: ' + filename
        tmp = data.imread('patterns/' + filename, as_grey=True)
        tmp **= 2.0
        tmp = filter.canny(tmp, sigma=3.0)
        tmp = morphology.dilation(tmp, morphology.disk(2))
        descriptor_extractor.detect_and_extract(tmp)
        obj_desc = descriptor_extractor.descriptors
        patterns.append(obj_desc)


def load_scenes(scenes, descriptor_extractor):
    listing = os.listdir('scenes')
    for filename in listing:
        print 'Working on: ' + filename
        tmp = data.imread('scenes/' + filename, as_grey=True)
        tmp **= 2.0
        tmp = filter.canny(tmp, sigma=3.0)
        tmp = morphology.dilation(tmp, morphology.disk(2))
        descriptor_extractor.detect_and_extract(tmp)
        scen_desc = descriptor_extractor.descriptors
        scenes.append(scen_desc)


def set_names(types, colors, card, size):
    i = -1
    while i < size:
        if i > -1:
            card.append(types[i % 13] + ' ' + colors[int(i / 13)])
        i += 1


def recognize(patterns, scenes, cards):
    for j in scenes:
        best_match = 0
        id = 0
        i = 0
        while i < len(patterns):
            matches = match_descriptors(j, patterns[i], cross_check=True)
            if matches.size > best_match:
                id = i
                best_match = matches.size
            i += 1
        print 'Karta to: ', cards[id]


def main():
    types = ['as', 'dwojka', 'trojka', 'czworka',
             'piatka', 'szostka', 'siodemka', 'osemka',
             'dziewiatka', 'dziesiatka', 'walet', 'dama', 'krol']
    colors = ['pik', 'kier', 'trefl', 'karo']
    cards = ['joker']
    patterns = []
    scenes = []
    descriptor_extractor = ORB()
    #p = Pool(5)

    #p.map(load_pattenrs, patterns, descriptor_extractor)
    #p.map(load_scenes, scenes, descriptor_extractor)
    load_pattenrs(patterns, descriptor_extractor)
    load_scenes(scenes, descriptor_extractor)
    set_names(types, colors, cards, len(patterns) - 1)

    recognize(patterns, scenes, cards)

if __name__ == '__main__':
    main()