__author__ = 'student'

from skimage import data, filter, morphology
import matplotlib.pyplot as plt

def main():
    plt.figure(figsize=(15, 14))
    planes = ['samolot01.jpg', 'samolot09.jpg', 'samolot05.jpg', 'samolot00.jpg', 'samolot07.jpg', 'samolot13.jpg']
    i = 0
    for file in planes:
        img = data.imread(file, as_grey=True)
        ax = plt.subplot(3, 2, i)
        ax.axis('off')
        #img = filter.sobel(img)
        img **= 0.4
        img = filter.canny(img, sigma=3.0)
        img = morphology.dilation(img, morphology.disk(2))
        img = filter.gaussian_filter(img, sigma=1.0)
        ax.imshow(img, cmap=plt.cm.gray, aspect='auto')
        i += 1

    plt.savefig('zad1.pdf')

if __name__ == '__main__':
    main()

