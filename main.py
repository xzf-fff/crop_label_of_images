from crop_label import *
image = np.array(Image.open('test_images/SARShip-1.0-30.tif'))
[cropped_images,ind] = crop_image(image, 416, 416, 2)
for i in range(len(cropped_images)):
    a=Image.fromarray(cropped_images[i])
    a.save("test_images/output"+str(i)+".tif")
print(cropped_images.shape)
labels=[]
with open("SARShip-1.0-30.txt") as f:
    for line in f:
        labels.append(line)
crop_label=crop_label(image,labels,3000,3000,416,416,2,ind)