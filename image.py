from skimage import data, filter, morphology
from skimage.feature import (match_descriptors, ORB, plot_matches)
import os
from multiprocessing import Pool
import logging
import matplotlib.pyplot as plt

types = ['as', 'dwojka', 'trojka', 'czworka',
             'piatka', 'szostka', 'siodemka', 'osemka',
             'dziewiatka', 'dziesiatka', 'walet', 'dama', 'krol']
colors = ['pik', 'kier', 'trefl', 'karo']
cards = ['joker']
descriptor_extractor = ORB()

def load_pattenrs(filename):
    z_patterns = []
    print 'Working on: ' + filename
    img = data.imread('patterns/' + filename, as_grey=True)
    tmp = img
    tmp = filter.canny(tmp, sigma=3.0)
    tmp = morphology.dilation(tmp, morphology.disk(2))
    descriptor_extractor.detect_and_extract(tmp)
    obj_key = descriptor_extractor.keypoints
    obj_desc = descriptor_extractor.descriptors
    z_patterns.append([img, obj_desc, obj_key, filename])
    return z_patterns


def load_scenes(filename):
    zipped_scenes = []
    print 'Working on: ' + filename
    img = data.imread('scenes/' + filename, as_grey=True)
    tmp = img
    tmp **= 2.0
    tmp = filter.canny(tmp, sigma=3.0)
    tmp = morphology.dilation(tmp, morphology.disk(2))
    descriptor_extractor.detect_and_extract(tmp)
    obj_key = descriptor_extractor.keypoints
    scen_desc = descriptor_extractor.descriptors
    zipped_scenes.append([img, scen_desc, obj_key, filename])
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
    zipped_matches.append([match.size, name, match])
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
    p_img, patterns, p_key, tmp = zip(*zipped_patterns)
    zipped_scenes.sort(key=lambda x: x[3])
    s_img, scenes, s_key, tmp = zip(*zipped_scenes)
    set_names(len(zipped_patterns) - 1)
    k = 0
    for j in scenes:
        arg_list = []
        for a, b, c, d in zipped_patterns:
            arg_list.append([b, d, j])
        zipped_matches = p.map(f_wrap, arg_list)
        zipped_matches = [ent for sublist in zipped_matches for ent in sublist]
        zipped_matches.sort(key=lambda x: x[1])
        matches, tmp, m_array = zip(*zipped_matches)
        best_match = max(matches)
        proc = 1.0
        id = 0
        for i in range(len(patterns)):
            el = abs((patterns[i].size/j.size) - 1)
            if matches[i] == best_match and el < proc:
                proc = el
                id = i
        fig, ax = plt.subplots()
        plt.gray()
        plot_matches(ax, p_img[id], s_img[k], p_key[id], s_key[k], m_array[id])
        ax.axis('off')
        plt.show()
        print 'Karta to: ', cards[id]
        k += 1

if __name__ == '__main__':
    main()