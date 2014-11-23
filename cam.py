from skimage import data, filter, morphology
from skimage.feature import (match_descriptors, ORB, plot_matches)
import os
from multiprocessing import Pool
import logging
import cv2
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
    obj_desc = descriptor_extractor.descriptors
    z_patterns.append([obj_desc, filename, img])
    return z_patterns


def take_pic():
    camera = cv2.VideoCapture(0)
    for i in xrange(30):
        temp, tmp = camera.read()
    print("Taking image...")
    retval, img = camera.read()
    cv2.imwrite("tmp.jpg", img)
    img = data.imread('tmp.jpg', as_grey=True)
    tmp = img
    tmp **= 2.0
    tmp = filter.canny(tmp, sigma=3.0)
    tmp = morphology.dilation(tmp, morphology.disk(2))
    descriptor_extractor.detect_and_extract(tmp)
    del(camera)
    return descriptor_extractor.descriptors, img



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
    print "Get ready..."
    #zipped_patterns.sort(key=lambda x: x[1])
    patterns, tmp, img = zip(*zipped_patterns)
    set_names(len(zipped_patterns) - 1)
    scene_desc, scene = take_pic()
    arg_list = []
    for a, b, c in zipped_patterns:
        arg_list.append([a, b, scene_desc])
    zipped_matches = p.map(f_wrap, arg_list)
    zipped_matches = [ent for sublist in zipped_matches for ent in sublist]
    zipped_matches.sort(key=lambda x: x[1])
    matches, tmp, match_array = zip(*zipped_matches)
    best_match = max(matches)
    proc = 1.0
    id = 0
    for i in range(len(patterns)):
        el = abs(1 - (patterns[i].size/scene_desc.size))
        if matches[i] == best_match and el < proc:
            proc = el
            id = i
    print 'Karta to: ', cards[id]
    fig, ax = plt.subplots()
    plt.gray()
    plot_matches(ax, img[id], scene, patterns[id], scene_desc, match_array[id])
    ax.axis('off')
    plt.show()


if __name__ == '__main__':
    main()