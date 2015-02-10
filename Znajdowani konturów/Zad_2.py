__author__ = 'student'

from skimage import data, filter, morphology
import matplotlib.pyplot as plt
from skimage import measure
from scipy import ndimage

def main():
    plt.figure(figsize=(25, 24))
    planes = ['samolot00.jpg', 'samolot01.jpg', 'samolot03.jpg', 'samolot04.jpg', 'samolot05.jpg','samolot07.jpg',
              'samolot08.jpg', 'samolot09.jpg', 'samolot10.jpg', 'samolot11.jpg', 'samolot12.jpg', 'samolot13.jpg',
              'samolot14.jpg', 'samolot15.jpg', 'samolot16.jpg', 'samolot17.jpg', 'samolot18.jpg', 'samolot20.jpg']
    i = 1
    for file in planes:
        img = data.imread(file, as_grey=True)
        img2 = data.imread(file)
        ax = plt.subplot(6, 3, i)
        ax.axis('off')
        img **= 0.4
        img = filter.canny(img, sigma=3.0)
        img = morphology.dilation(img, morphology.disk(4))
        img = ndimage.binary_fill_holes(img)
        img = morphology.remove_small_objects(img, 1000)
        contours = measure.find_contours(img, 0.8)
        ax.imshow(img2, aspect='auto')
        for n, contour in enumerate(contours):
            ax.plot(contour[:, 1], contour[:, 0], linewidth=1.5)
            center = (sum(contour[:, 1])/len(contour[:, 1]), sum(contour[:, 0])/len(contour[:, 0]))
            ax.scatter(center[0], center[1], color='white')
        i += 1

    plt.savefig('zad2.pdf')

if __name__ == '__main__':
    main()

