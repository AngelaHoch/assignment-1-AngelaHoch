import numpy as np

class binary_image:

    def compute_histogram(self, image):
        """Computes the histogram of the input image
        takes as input:
        image: a grey scale image
        returns a histogram"""

        hist = [0]*256
        for j in range(image.shape[0]):
            for i in range(image.shape[1]):
                intensity = image[j][i]
                hist[intensity] += 1

        return hist

    def find_optimal_threshold(self, hist):
        """analyses a histogram it to find the optimal threshold value assuming a bimodal histogram
        takes as input
        hist: a bimodal histogram
        returns: an optimal threshold value"""

        threshold = 128
        m1 = 0
        c1 = 0
        m2 = 0
        c2 = 0
        deltam1 = 1
        deltam2 = 1

        while (deltam1 != 0 and deltam2 != 0):
            deltam1 = m1
            deltam2 = m2
            m1 = 0
            m2 = 0
            c1 = 0
            c2 = 0

            for i in range(256):
                if i < threshold:
                    m1 = m1 + (i * hist[i])
                    c1 = c1 + hist[i]
                else:
                    m2 = m2 + (i * hist[i])
                    c2 = c2 + hist[i]

            m1 = m1/c1
            m2 = m2/c2

            if m1 > m2:
                temp = m1
                m1 = m2
                m2 = temp

            threshold = (m1 + m2)/2

            deltam1 = (deltam1 - m1)
            deltam2 = (deltam2 - m2)

        return int(threshold)

    def binarize(self, image):
        """Comptues the binary image of the the input image based on histogram analysis and thresholding
        take as input
        image: an grey scale image
        returns: a binary image"""

        bin_img = image.copy()
        hist = self.compute_histogram(image)
        threshold = self.find_optimal_threshold(hist)

        for j in range(bin_img.shape[0]):
            for i in range(bin_img.shape[1]):
                intensity = bin_img[j][i]
                if intensity < threshold:
                    bin_img[j][i] = 0
                else:
                    bin_img[j][i] = 255

        return bin_img


