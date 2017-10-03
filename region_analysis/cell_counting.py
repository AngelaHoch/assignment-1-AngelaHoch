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
        k = 1
        region = -1

        print("Setting regions")

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
                    
                    """for coords in window:
                        if image[coords[0]][coords[1]] == 255:
                            if region == -1 and coords in blobs:
                                region = blobs[coords]
                            elif region != -1:
                                blobs[coords] = region
                            else:
                                blobs[coords] = k
                                region = k
                                k = k + 1
                    """
                    windowRegion = [0] * 9
                    for i in range(9):
                        coords = window[i]
                        if image[coords[0]][coords[1]] == 255:
                            if coords in blobs:
                                windowRegion[i] = blobs[coords]
                                region = blobs[coords]
                            else:
                                windowRegion[i] = -1

                    if region == -1:
                        region = k
                        k += 1
                        for i in range(9):
                            if windowRegion[i] == 0:
                                continue
                            coords = window[i]
                            blobs[coords] = region

                    else:
                        for i in range(9):
                            if windowRegion[i] == 0:
                                continue;
                            coords = window[i]
                            if region != windowRegion[i]:
                                if windowRegion[i] != -1:
                                #find all instances in the dict that have windowRegion[i] and replace them with region
                                    for p, r in blobs.items():
                                        if blobs[p] == windowRegion[i]:
                                            blobs[p] = region
                                else:
                                    blobs[coords] = region


                    region = -1

        print("Reversing Dictionary")

        for p, r in blobs.items():
            if r in regions:
                regions[r] = regions[r] + [p]
            else:
                regions[r] = [p]
            
        return regions

    def compute_statistics(self, region):
        """Compute cell statistics area and location
        takes as input
        region: a list of pixels in a region
        returns: area"""

        stats = dict()

        print("The center of everything")
        
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
            center = (centerx, centery)
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

        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        font = cv2.FONT_HERSHEY_SIMPLEX

        for r in stats.keys():
            center, area = stats[r]
            cv2.circle(image,center, 3, (200,0,128), -1)
            cv2.putText(image,str(area),center, font, 0.5,(255,0,255), 1)

        return image