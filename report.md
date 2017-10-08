Angela Hoch
1184422

nearest_neighbor:

The nearest neighbor implementation I used is simple. First, the new image size is calculated, and a black image is created to be a placeholder for the new image, using numpy's zeros function. The basic algorithm for nearest neighbor is based off of how close the nearest cell in the original image is to the current cell we are looking at in the new image, and copying the intensity of the old cell into the new. So in my code, a nested for loop is used to look at every pixel of the new image. Using the index number of the pixel it is looking at, the y and x values are calculated based on the index divided by the scale of the new image. the x and y values are rounded to the nearest whole number, and then turned into int values so that they can be used as coordinates of the old image.

The first thing I learned from doing this assignment is that images read by the cv2 library are stored in matrices that are represented as (y, x) instead of (x, y). This has probably been mentioned before, and it took me a while to figure out that this was a problem. I employed a function that worked while assuming that the matrix of the image is (x, y) based, however once I started scaling things out of proportion (ie, instead of fx = fy), I noticed that something was off about the output image.

bilinear_interpolation:

This method of resizing an image was a bit more complicated. It started the same as before; calculate the new size, create a placeholder image. Afterwards, calculate the y and x values of the old image that correspond to the new image. If these values are not whole numbers, then new intensity values need to be calculated for the new image. To do this, it needed to find the surrounding values of the y and x coordinates, where the new point xy is in the middle of p1, p2, p3, and p4, as shown below:

    p1 -xy1- p2
    |        |
    |   xy   |
    |        |
    p3 -xy2- p4

To calculate the new intensity, the proportions of each point's intensity surrounding xy are added together. The functions for doing this can be found in interpolation.py. 

	bilinear_interpolation:
	This function calculates the bilinear interpolation between 4 given points. It first decides if the x-axis points need to undergo linear interpolation, and send them to linear_interpolation if they do. Then it determines if the same needs to happen on the y-axis. 
	linear_interpolation:
	Using the coordinate of the new x point, the function returns the intensity of the x-axis interpolation. This is calculated using the following formula:
	
	f_Total = f_1 * ((x - p1(x))/(p2(x)-p1(x))) + f_2 * ((p2(x) - x)/(p2(x)-p1(x)))
	
	where f_1 is the intensity of the right side point and f_2 is the intensity of the left side point.
	
	This formula is also used later in the earlier function to determine the interpolation on the y-axis.
	
compute_histogram:

This function employs a simple tactic; it uses a nested for loop to look at every pixel of the given image, and uses the pixel's intensity as an index to the list that keeps count of the pixels.

find_optimal_threshold:

Since the threshold is going to be between 0 and 255, it is initialized at 128. Then, the expected value is calculated on each side of the threshold, along with the total number of pixels, using the list that was created to create the histogram. Using the expected values, the threshold is recalculated. This process continues until the expected values do not change.

binarize:

Using the threshold previously calculated, this function uses a nested for loop to reassign the intensities of the image. Anything less than the threshold is given an intensity of 0, anything else is given a threshold of 255 (If this image were stored in binary, this would be a equivilant of changing everything to 0s and 1s).

blob_coloring:

This function uses 3 dictionaries to find, mark, and clean up the blob coloring. The first dictionary in use is called blobs. This dictionary keeps track of each tuple of points and their region number. This allows the program to check if the point being checked has a region assigned to it already by looking it up by its key. Otherwise, if we had the region numbers as the keys, it would take a bit more time to find if a point exists in any given region, and if it exists in the wrong region, this would create some issues. It also puts off creating a list for each key to point to. The first set of nested loops creates the values of dictionary blobs. This formula is using white for its blob color, so any black cells that are being investigated are ignored. Once a white cell is found, the 8 cells around it are found and all cells are assigned a region number. If one of these cells already hase a region number, then all the cells are given that region. Else, if more than one cell has a region number, the assigned number is the last region found in the group of cells, and all cells with an incorrect region number are renumbered to have the same one. This is all cells in the image that have the wrong number, not just the ones within the window. After the blobs have been numbered, the regionstemp dictionary is used to organize blobs by region, using the region number as a key. Since this formula overwrites regions which causes some numbers to be eliminated, and because I felt that they needed to have nicer region numbers, the regions dictionary renumbers the previous dictionary before being returned by the function.

compute_statistics:

This function computes the area of each blob by counting all the pixels within it, and it finds the center of each blob by finding the highest, lowest, rightmost, and leftmost coordinate of the blob (ie, the maximum x and y values, and the minimum x and y values), and uses those values to find the geometric center of the blob.

mark_regions_image:

Using the centers and areas computed by the previous function, the image has points created where each center is, and the area of that blob written next to it. 

In contrast to the matrices used by the rest of the program, cv2's drawing functions require coordinates in (x, y) format. 