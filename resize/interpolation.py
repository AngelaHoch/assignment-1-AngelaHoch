#class interpolation:

def linear_interpolation(image, pt1, pt2, unknown):
    """Computes the linear interpolation for the unknown values using pt1 and pt2
    take as input
    pt1: known point pt1 and f(pt1) or intensity value
    pt2: known point pt2 and f(pt2) or intensity value
    unknown: take and unknown location
    return the f(unknown) or intensity at unknown"""
    f1 = (unknown[1] - pt1[1])/(pt2[1] - pt1[1])
    f1 = f1 *image[pt2[0]][pt2[1]]
    f2 = (pt2[1] - unknown[1])/(pt2[1] - pt1[1])*image[pt1[0]][pt2[1]]
    ft = f1 + f2

    return ft

def bilinear_interpolation(image, pt1, pt2, pt3, pt4, unknown):
    """Computes the linear interpolation for the unknown values using pt1 and pt2
    take as input
    pt1: known point pt1 and f(pt1) or intensity value
    pt2: known point pt2 and f(pt2) or intensity value
    pt1: known point pt3 and f(pt3) or intensity value
    pt2: known point pt4 and f(pt4) or intensity value
    unknown: take and unknown location
    return the f(unknown) or intensity at unknown"""

    """
    p1 -xy1- p2
    |        |
    |   xy   |
    |        |
    p3 -xy2- p4
    This is how I'm using the points.
    """
    #f(x, y1)
    currInt = 0
    
    if pt1[1] == pt2[1]:
        #if x1 == x2
        #only need interpolation on the y axis
        xy1 = image[pt1[0]][pt1[1]]
        xy2 = image[pt4[0]][pt4[1]]
    else:
        xy1 = linear_interpolation(image, pt1, pt2, unknown)
        xy2 = linear_interpolation(image, pt3, pt4, unknown)

    if pt1[0] == pt3[0]:
        #if y1 == y2
        #only need interpolation on the x axis
        currInt = int((xy1 + xy2)/2)
    else:
        f1 = (unknown[0] - pt3[0])/(pt1[0] - pt3[0])*xy2
        f2 = (pt1[0] - unknown[0])/(pt1[0] - pt3[0])*xy1
        currInt = f1 + f2
      
    return currInt
