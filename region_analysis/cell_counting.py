import numpy
import cv2
class cell_counting:

    def blob_coloring(self, image):
        """Uses the blob coloring algorithm based on 8 pixel window assign region names
        takes a input:
        image: binary image
        return: a list of regions"""

        #using white (255) as blob color

        regions = dict()
        blobs = dict()
        k = 0
        region = -1

        for j in range(image.shape[0]):
            for i in range(image.shape[1]):
                if image[j][i] == 255:
                    point = (j, i);
                    if point in blobs:
                        continue
                    left = i - 1
                    right = i + 1
                    up = j + 1
                    down = j - 1
                    if(left < 0):
                        left = 0
                    if(right >= image.shape[1]):
                        right = image.shape[1] - 1
                    if(up >= image.shape[0]):
                        up = image.shape[0] - 1
                    if(down < 0):
                        down = 0

                    window = [(up, left),(up, i),(up, right),(j, left),point,(j, right),(down, left),(down, i),(down, right)]

                    #current = (0, 0);
                    
                    for coords in window:
                        if image[coords[0]][coords[1]] == 255:
                            if region == -1 and coords in blobs:
                                region = blobs[coords]
                            elif region != -1:
                                blobs[coords] = region
                            else:
                                blobs[coords] = k
                                region = k
                                k = k + 1

                    region = -1

        for point, r in blobs.items():
            if r in regions:
                regions[r] = regions[r] + [point]
            else:
                regions[r] = [point]
            
        return regions

    def compute_statistics(self, region):
        """Compute cell statistics area and location
        takes as input
        region: a list of pixels in a region
        returns: area"""

        stats = dict()
        
        for r in region.keys():
            maxx = 0
            maxy = 0
            minx = 0
            miny = 0
            area = 0
            for point in region[r]:
                if point[0] > maxy or maxy == 0:
                    maxy = point[0]
                if point[0] < miny or miny == 0:
                    miny = point[0]
                if point[1] > maxx or maxx == 0:
                    maxx = point[1]
                if point[1] < minx or minx == 0:
                    minx = point[1]
                area = area + 1
            centerx = int((maxx + minx)/2)
            centery = int((maxy + miny)/2)
            center = (centery, centerx)
            if area >= 15:
                stats[r] = (center, area)

        for r in stats.keys():
            print("Region:  ", r, "\tArea:  ", stats[r][1], "\tCentroid:  ", stats[r][0])

        # Please print your region statistics to stdout
        # <region number>: <location or center>, <area>
        # print(stats)

        return stats

    def mark_regions_image(self, image, stats):
        """Creates a new image with computed stats
        takes as input
        image: a list of pixels in a region
        stats: stats regarding location and area
        returns: image marked with center and area"""

        font = cv2.FONT_HERSHEY_SIMPLEX

        for r in stats.keys():
            center, area = stats[r]
            cv2.putText(image,str(area),center, font, 1,(0,0,128))

        return image