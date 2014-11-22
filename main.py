from skimage import data, filter, morphology
from skimage.feature import (match_descriptors, ORB)
import os
from multiprocessing import Pool
import logging

types = ['as', 'dwojka', 'trojka', 'czworka',
             'piatka', 'szostka', 'siodemka', 'osemka',
             'dziewiatka', 'dziesiatka', 'walet', 'dama', 'krol']
colors = ['pik', 'kier', 'trefl', 'karo']
cards = ['joker']
descriptor_extractor = ORB()

def load_pattenrs(filename):
    z_patterns = []
    print 'Working on: ' + filename
    tmp = data.imread('patterns/' + filename, as_grey=True)
    tmp = filter.canny(tmp, sigma=3.0)
    tmp = morphology.dilation(tmp, morphology.disk(2))
    descriptor_extractor.detect_and_extract(tmp)
    obj_desc = descriptor_extractor.descriptors
    z_patterns.append([obj_desc, filename])
    return z_patterns


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


def recognize(pattern, name, scene):
    zipped_matches = []
    match = match_descriptors(scene, pattern, cross_check=True)
    zipped_matches.append([match.size, name])
    return zipped_matches

def f_wrap(arg_list):
    try:
        return recognize(*arg_list)
    except Exception:
        logging.exception("f(%r) failed" % (arg_list,))

def main():
    p = Pool(5)
    listing = os.listdir('patterns')
    zipped_patterns = p.map(load_pattenrs, listing)
    zipped_patterns = [ent for sublist in zipped_patterns for ent in sublist]
    listing = os.listdir('scenes')
    zipped_scenes = p.map(load_scenes, listing)
    zipped_scenes = [ent for sublist in zipped_scenes for ent in sublist]
    #zipped_patterns.sort(key=lambda x: x[1])
    #patterns, name = zip(*zipped_patterns)
    zipped_scenes.sort(key=lambda x: x[1])
    scenes, tmp = zip(*zipped_scenes)
    set_names(len(zipped_patterns) - 1)
    for j in scenes:
        arg_list = []
        for a, b in zipped_patterns:
            arg_list.append([a, b, j])
        zipped_matches = p.map(f_wrap, arg_list)
        zipped_matches = [ent for sublist in zipped_matches for ent in sublist]
        zipped_matches.sort(key=lambda x: x[1])
        matches, tmp = zip(*zipped_matches)
        print 'Karta to: ', cards[matches.index(max(matches))]

if __name__ == '__main__':
    main()