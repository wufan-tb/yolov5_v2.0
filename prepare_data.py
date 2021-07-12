# -*- coding: utf-8 -*-
import os,random,shutil,argparse,yaml
import xml.etree.ElementTree as ET

#参数修改
#================================
parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='/data/gongdi', help='dataset path, contain jpgs and xmls')
parser.add_argument('--data_yaml', type=str, default='data/gongdi.yaml',help="split by ,")
parser.add_argument('--split', type=float, default=0.8, help='split ratio')
args = parser.parse_args()
#================================
with open(args.data_yaml, encoding='utf-8') as file:
    yaml = yaml.full_load(file)
classes = yaml['names']
dataset_path = args.dataset
train_percent = args.split
print(classes,dataset_path,train_percent)

sets = ['train', 'val']
xmlfilepath = os.path.join(dataset_path,'Annotations')
txtsavepath = os.path.join(dataset_path,'ImageSets')
os.makedirs(txtsavepath,exist_ok=True)
total_xml = os.listdir(xmlfilepath)

ftrain = open(os.path.join(txtsavepath,'train.txt'), 'w')
fval = open(os.path.join(txtsavepath,'val.txt'), 'w')
for i in range(len(total_xml)):
    name = total_xml[i][:-4] + '\n'
    temp=random.random()
    if temp < train_percent:
        ftrain.write(name)
    else:
        fval.write(name)

ftrain.close()
fval.close()

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(image_id):
    in_file = open(os.path.join(dataset_path,'Annotations','%s.xml'%(image_id)))
    out_file = open(os.path.join(dataset_path,'temp','%s.txt'%(image_id)), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

def locate(path):
    temp = []
    with open(os.path.join(path,'val.txt'),'rb') as f:
        for line in f.readlines():
            temp.append(str(line.strip()).split("'")[1])
    return temp    

def object_save(path,pic,pic_save): 
    temp = locate(path)
    os.makedirs(os.path.join(pic_save,'val'),exist_ok=True)
    os.makedirs(os.path.join(pic_save,'train'),exist_ok=True) 
    for item in os.listdir(pic):
        before=os.path.join(pic,item)
        if item[:-4] in temp:
            shutil.copyfile(before,os.path.join(pic_save,'val',item))  
        else:
            shutil.copyfile(before,os.path.join(pic_save,'train',item))

for image_set in sets:
    os.makedirs(os.path.join(dataset_path,'temp'),exist_ok=True)
    image_ids = open(os.path.join(dataset_path,'ImageSets','%s.txt'%(image_set))).read().strip().split()
    for image_id in image_ids:
        convert_annotation(image_id)
    
pic_path = os.path.join(dataset_path,'JPEGImages')
pic_save_path = os.path.join(dataset_path,'images')
object_save(txtsavepath,pic_path,pic_save_path)

labels_path = os.path.join(dataset_path,'temp')
labels_save_path = os.path.join(dataset_path,'labels')
object_save(txtsavepath,labels_path,labels_save_path)

shutil.rmtree(os.path.join(dataset_path,'temp'))
shutil.rmtree(os.path.join(dataset_path,'ImageSets'))

print("prepare done!")



