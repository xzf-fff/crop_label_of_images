import numpy as np
from PIL import Image
import math
class index:
    def __init__(self,x0,y0):
        self.x0=x0
        self.y0=y0

def calculate_crop_number(image, crop_height, crop_width, oc):
    height = image.shape[0]
    width = image.shape[1]
    height_number = math.ceil(height / crop_height)
    height_number = oc * (height_number - 1) + 1
    width_number = math.ceil(width / crop_width)
    width_number = oc * (width_number - 1) + 1
    output = height_number * width_number
    return output, height_number, width_number


def test_and_complement(image, crop_height, crop_width):
    if image.shape[0] != crop_height or image.shape[1] != crop_width:
        if len(image.shape) == 2:
            complement = np.zeros([crop_height, crop_width]).astype(image.dtype)
        else:
            complement = np.zeros([crop_height, crop_width, image.shape[2]]).astype(image.dtype)
        complement[0:image.shape[0], 0:image.shape[1]] = image
        return complement
    else:
        return image


def crop_image(image, crop_height, crop_width, oc):
    total_output_number, height_number, width_number = calculate_crop_number(image, crop_height, crop_width, oc)
    if len(image.shape) == 2:
        output = np.zeros([total_output_number, crop_height, crop_width]).astype(image.dtype)
    else:
        output = np.zeros([total_output_number, crop_height, crop_width, image.shape[2]]).astype(image.dtype)
    count = 0
    ind=[]
    for i in range(height_number):
        ind.append([])
        for j in range(width_number):
            a=index(int(crop_width / oc * j),int(crop_height / oc * i))
            ind[i].append(a)
            unit_crop_image = image[int(crop_height / oc * i):int(crop_height / oc * i) + crop_height,
                              int(crop_width / oc * j):int(crop_width / oc * j) + crop_width]
            unit_crop_image = test_and_complement(unit_crop_image, crop_height, crop_width)
            output[count] = unit_crop_image
            count += 1
    return [output,ind]


def recover_image(cropped_image, height, width, crop_height, crop_width, oc):
    in_height_number = math.ceil(height / crop_height)
    height_number = oc * (in_height_number - 1) + 1
    in_width_number = math.ceil(width / crop_width)
    width_number = oc * (in_width_number - 1) + 1
    if len(cropped_image.shape) == 3:
        output_image = np.zeros([in_height_number * crop_height, in_width_number * crop_width]).astype(
            cropped_image.dtype)
    else:
        output_image = np.zeros([in_height_number * crop_height,
                                 in_width_number * crop_width, cropped_image.shape[3]]).astype(cropped_image.dtype)
    assert crop_height * (oc - 1) % (2 * oc) == 0 and crop_width * (oc - 1) % (2 * oc) == 0, \
        'The input crop image size and overlap coefficient cannot meet the exact division'
    h_sec_pos = int(crop_height * (oc - 1) / (2 * oc))
    w_sec_pos = int(crop_width * (oc - 1) / (2 * oc))
    h_thi_pos = int(crop_height * (oc + 1) / (2 * oc))
    w_thi_pos = int(crop_width * (oc + 1) / (2 * oc))
    h_half_pos = int(crop_height / oc)
    w_half_pos = int(crop_width / oc)

    for i in range(height_number):
        if i == 0:
            for j in range(width_number):
                if height_number == 1:
                    if j == 0:
                        if width_number == 1:
                            output_image[0:crop_height, 0:crop_width] = \
                                cropped_image[i * width_number + j][0:crop_height, 0:crop_width]
                        else:
                            output_image[0:crop_height, 0:w_thi_pos] = \
                                cropped_image[i * width_number + j][0:crop_height, 0:w_thi_pos]
                    elif j == (width_number - 1):
                        output_image[0:crop_height, j * w_half_pos + w_sec_pos:] = \
                            cropped_image[i * width_number + j][0:crop_height, w_sec_pos:crop_width]
                    else:
                        output_image[0:crop_height, w_thi_pos + (j - 1) * w_half_pos:w_thi_pos + j * w_half_pos] = \
                            cropped_image[i * width_number + j][0:crop_height, w_sec_pos:w_thi_pos]

                else:
                    if j == 0:
                        if width_number == 1:
                            output_image[0:h_thi_pos, 0:crop_width] = \
                                cropped_image[i * width_number + j][0:h_thi_pos, 0:crop_width]
                        else:
                            output_image[0:h_thi_pos, 0:w_thi_pos] = \
                                cropped_image[i * width_number + j][0:h_thi_pos, 0:w_thi_pos]
                    elif j == (width_number - 1):
                        output_image[0:h_thi_pos, j * w_half_pos + w_sec_pos:] = \
                            cropped_image[i * width_number + j][0:h_thi_pos, w_sec_pos:crop_width]
                    else:
                        output_image[0:h_thi_pos, w_thi_pos + (j - 1) * w_half_pos:w_thi_pos + j * w_half_pos] = \
                            cropped_image[i * width_number + j][0:h_thi_pos, w_sec_pos:w_thi_pos]
        elif i == (height_number - 1):
            for j in range(width_number):
                if j == 0:
                    if width_number == 1:
                        output_image[i * h_half_pos + h_sec_pos:, 0:crop_width] = \
                            cropped_image[i * width_number + j][h_sec_pos:crop_height, 0:crop_width]
                    else:
                        output_image[i * h_half_pos + h_sec_pos:, 0:w_thi_pos] = \
                            cropped_image[i * width_number + j][h_sec_pos:crop_height, 0:w_thi_pos]
                elif j == (width_number - 1):
                    output_image[i * h_half_pos + h_sec_pos:, j * w_half_pos + w_sec_pos:] = \
                        cropped_image[i * width_number + j][h_sec_pos:crop_height, w_sec_pos:crop_width]
                else:
                    output_image[i * h_half_pos + h_sec_pos:,
                    w_thi_pos + (j - 1) * w_half_pos:w_thi_pos + j * w_half_pos] = \
                        cropped_image[i * width_number + j][h_sec_pos:crop_height, w_sec_pos:w_thi_pos]
        else:
            for j in range(width_number):
                if j == 0:
                    if width_number == 1:
                        output_image[h_thi_pos + (i - 1) * h_half_pos:h_thi_pos + i * h_half_pos,
                        0:crop_width] = cropped_image[i * width_number + j][h_sec_pos:h_thi_pos, 0:crop_width]
                    else:
                        output_image[h_thi_pos + (i - 1) * h_half_pos:h_thi_pos + i * h_half_pos,
                        0:w_thi_pos] = cropped_image[i * width_number + j][h_sec_pos:h_thi_pos, 0:w_thi_pos]
                elif j == (width_number - 1):
                    output_image[h_thi_pos + (i - 1) * h_half_pos:h_thi_pos + i * h_half_pos,
                    j * w_half_pos + w_sec_pos:] = \
                        cropped_image[i * width_number + j][h_sec_pos:h_thi_pos, w_sec_pos:crop_width]
                else:
                    output_image[h_thi_pos + (i - 1) * h_half_pos:h_thi_pos + i * h_half_pos,
                    w_thi_pos + (j - 1) * w_half_pos:w_thi_pos + j * w_half_pos] = \
                        cropped_image[i * width_number + j][h_sec_pos:h_thi_pos, w_sec_pos:w_thi_pos]
    output_image = output_image[0:height, 0:width]
    return output_image
def crop_label(image,labels1, height, width, crop_height, crop_width, oc,index):
    in_height_number = math.ceil(height / crop_height)
    height_number = oc * (in_height_number - 1) + 1
    in_width_number = math.ceil(width / crop_width)
    width_number = oc * (in_width_number - 1) + 1
    assert crop_height * (oc - 1) % (2 * oc) == 0 and crop_width * (oc - 1) % (2 * oc) == 0, \
        'The input crop image size and overlap coefficient cannot meet the exact division'
    labels=[]
    for label in labels1:
        if len(image.shape) == 3:
            label[0] = label[0] * image.shape[2]
            label[1] = label[0] * image.shape[1]
            label[2] = label[2] * image.shape[2]
            label[3] = label[3] * image.shape[1]
        else:
            label=label.split()
            label0 = float(label[1]) * image.shape[1]
            label1 = float(label[2]) * image.shape[0]
            label2 = float(label[3]) * image.shape[1]
            label3 = float(label[4]) * image.shape[0]
            labels.append([label0,label1,label2,label3])
    #for i in range(len(labels)):
     #   print(labels[i])
    for i in range(height_number):
        for j in range(width_number):
            with open("label"+str(i*height_number+j)+".txt",'wt') as f:
                #print(index[i][j].x0,index[i][j].y0)
                for label in labels:
                    if(label[0]>index[i][j].x0 and label[0]<index[i][j].x0+crop_height and label[1]>index[i][j].y0 and label[1]<index[i][j].y0+crop_width):
                        #print(label[0],"  ",labels[1],"  ",index[i][j].x0,"  ",index[i][j].y0)
                        #print(label[0])
                        #print(index[i][j].x0)
                        label[0]=(label[0]-index[i][j].x0)/crop_width
                        label[1]=(label[1]-index[i][j].y0)/crop_height
                        label[2]=label[2]/crop_width
                        label[3]=label[3]/crop_height
                        a=str(label[0])+" "+str(label[1])+" "+str(label[2])+" "+str(label[3])
                        print(a)
                        f.write(str(label[0])+" "+str(label[1])+" "+str(label[2])+" "+str(label[3]))



