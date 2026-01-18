import cv2
import numpy as np

# Load image in grayscale
image = cv2.imread('test image.jpg', cv2.IMREAD_GRAYSCALE)
image_colour = cv2.imread('test image.jpg', cv2.IMREAD_COLOR)

cv2.imshow('Original Image', image)
cv2.waitKey(0)

# Apply Gaussian Blur to reduce noise
blurred = cv2.GaussianBlur(image, (5, 5), 0)

cv2.imshow('Blurred Image', blurred)
cv2.waitKey(0)

# Detect edges using Canny
edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

cv2.imshow('Image Edges', edges)
cv2.waitKey(0)

# Blur with edge preservation using the Bilateral Filter
bilateral = cv2.bilateralFilter(image, 9, 75, 75)

cv2.imshow('Bilateral Filter', bilateral)
cv2.waitKey(0)


# Sharpen image with EXTREME kernel
kernel = np.array([
    [ 0, -1,  0],
    [-1,  10, -1],
    [ 0, -1,  0]
])
sharpened = cv2.filter2D(image, -1, kernel)

cv2.imshow('Sharpened', sharpened)
cv2.waitKey(0)

# Filter image for the colour green (RGB)
green_filter =cv2.inRange(image_colour, np.array([0, 100, 0]), np.array([100, 255, 100]))
cv2.imshow('Filtered for green', green_filter)
cv2.waitKey(0)

# Hough Line Transform
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)

# Convert grayscale to BGR for colored lines
output = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

# Draw lines
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Show result
cv2.imshow('Hough Lines', output)
cv2.waitKey(0)
cv2.destroyAllWindows()