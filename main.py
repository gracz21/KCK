from skimage import data, filter, morphology
from skimage.feature import (match_descriptors, ORB)
import os
from multiprocessing import Pool
from itertools import repeat
import functools

types = ['as', 'dwojka', 'trojka', 'czworka',
             'piatka', 'szostka', 'siodemka', 'osemka',
             'dziewiatka', 'dziesiatka', 'walet', 'dama', 'krol']
colors = ['pik', 'kier', 'trefl', 'karo']
cards = ['joker']
descriptor_extractor = ORB()

def load_patterns(filename):
    zipped_patterns = []
    print 'Working on: ' + filename
    tmp = data.imread('patterns/' + filename, as_grey=True)
    #tmp **= 2.0
    tmp = filter.canny(tmp, sigma=3.0)
    tmp = morphology.dilation(tmp, morphology.disk(2))
    descriptor_extractor.detect_and_extract(tmp)
    obj_desc = descriptor_extractor.descriptors
    zipped_patterns.append([obj_desc, filename])
    return zipped_patterns


def load_scenes(filename):
    zipped_scenes = []
    print 'Working on: ' + filename
    tmp = data.imread('scenes/' + filename, as_grey=True)
    tmp **= 2.0
    tmp = filter.canny(tmp, sigma=3.0)
    tmp = morphology.dilation(tmp, morphology.disk(2))
    descriptor_extractor.detect_and_extract(tmp)
    scen_desc = descriptor_extractor.descriptors
    zipped_scenes.append([scen_desc, filename])
    return zipped_scenes


def set_names(size):
    i = -1
    while i < size:
        if i > -1:
            cards.append(types[i % 13] + ' ' + colors[int(i / 13)])
        i += 1


def recognize(patterns, scenes):
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
    p = Pool(5)
    listing = os.listdir('patterns')
    zipped_patterns = p.map(load_patterns, listing)
    zipped_patterns = [ent for sublist in zipped_patterns for ent in sublist]
    listing = os.listdir('scenes')
    zipped_scenes = p.map(load_scenes, listing)
    zipped_scenes = [ent for sublist in zipped_scenes for ent in sublist]
    zipped_patterns.sort(key=lambda x: x[1])
    patterns, tmp = zip(*zipped_patterns)
    zipped_scenes.sort(key=lambda x: x[1])
    scenes, tmp = zip(*zipped_scenes)
    set_names(len(zipped_patterns) - 1)

    recognize(patterns, scenes)

if __name__ == '__main__':
    main()
