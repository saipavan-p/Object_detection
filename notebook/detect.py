import numpy as np
import cv2
import os

# image_path = 'uploads/'

uploads_folder = "uploads"
image_files = [f for f in os.listdir(uploads_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

if not image_files:
    print("No image files found in the 'uploads/' directory.")
    exit()

# Select the first image file
image_filename = image_files[0]
image_path = os.path.join(uploads_folder, image_filename)

output_folder = "output/"

prototxt_path = "models/MobileNetSSD_deploy.prototxt.txt"
model_path = "models/MobileNetSSD_deploy.caffemodel"

label_map_path = 'Label_Map.txt'

min_confidence = 0.2

# Load class labels from label map file
with open(label_map_path, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

np.random.seed(543210)

colors = np.random.uniform(0, 255, size=(len(classes), 3))

net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

image = cv2.imread(image_path)
height, width = image.shape[0], image.shape[1]
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007, (300,300), 130)

net.setInput(blob)
detected_objects = net.forward()

for i in range(detected_objects.shape[2]):

  confidence = detected_objects[0][0][i][2]

  if confidence > min_confidence:

    class_index = int(detected_objects[0, 0, i, 1])

    upper_left_x = int(detected_objects[0,0,i,3]* width)
    upper_left_y = int(detected_objects[0,0,i,4]* height)
    lower_right_x = int(detected_objects[0,0,i,5]* width)
    lower_right_y = int(detected_objects[0,0,i,6]* height)

    # Get the name of the detected object
    object_name = classes[class_index]

    prediction_text = f"{object_name}: {confidence:.2f}%"
    cv2.rectangle(image,(upper_left_x, upper_left_y), (lower_right_x, lower_right_y), colors[class_index], 3)
    cv2.putText(image, prediction_text, (upper_left_x, upper_left_y - 15 if upper_left_y > 30 else upper_left_y +15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[class_index], 2)


# cv2.imshow("Detected objects", image)
# cv2.waiteKey(0)
# cv2.destroyAllWindows()

# Save the output image to a folder
output_filename = "output_result.jpg" 
output_path = os.path.join(output_folder, output_filename)
cv2.imwrite(output_path, image)
