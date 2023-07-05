import cv2
import os
import numpy as np


def apply_average_filter(frame):
    kernel = (1/9) * np.ones((3, 3), dtype=np.float32)
    return cv2.filter2D(frame, -1, kernel)


output_folder = 'AvgFilter_ImgSeq'
os.makedirs(output_folder, exist_ok=True)


video_path = 'noisyvideo2.mp4'
cap = cv2.VideoCapture(video_path)


fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


output_path = os.path.join(output_folder, 'filtered_video.mp4')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))


frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break


    filtered_frame = apply_average_filter(frame)


    output_frame_path = os.path.join(output_folder, f'filtered_frame_{frame_count}.jpg')
    cv2.imwrite(output_frame_path, filtered_frame)


    output_video.write(filtered_frame)

    frame_count += 1

    if frame_count >= 10:
        break

cap.release()
output_video.release()




# Function to apply the pixel point transformation
def apply_pixel_transform(pixel_value):
    if pixel_value <= 100:
        transformed_value = (205 * pixel_value + 5000) / 100
    else:
        transformed_value = 255
    return transformed_value

output_folder = 'PixelTransform_ImgSeq'
os.makedirs(output_folder, exist_ok=True)

# the filtered frames
for frame_count in range(10):
    # Load the filtered frame
    filtered_frame_path = os.path.join('AvgFilter_ImgSeq', f'filtered_frame_{frame_count}.jpg')
    filtered_frame = cv2.imread(filtered_frame_path, cv2.IMREAD_GRAYSCALE)

    # pixel point transformation to each pixel
    transformed_frame = filtered_frame.copy()
    rows, cols = transformed_frame.shape
    for i in range(rows):
        for j in range(cols):
            transformed_frame[i, j] = apply_pixel_transform(filtered_frame[i, j])


    output_frame_path = os.path.join(output_folder, f'transformed_frame_{frame_count}.jpg')
    cv2.imwrite(output_frame_path, transformed_frame)