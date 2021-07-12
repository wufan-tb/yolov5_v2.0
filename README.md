## yolov5 v2.0 from [yolov5](https://github.com/ultralytics/yolov5)

# 1.preparpe data:
    python prepare_data.py --data_yaml data/gongdi.yaml --dataset /data/gongdi --split 0.8

# 2.change {dataset}.yaml

# 3.Train:
    python train.py --data gongdi.yaml --cfg yolov5l.yaml --weights '' --batch-size 8
                                             yolov5m                                16
                                             yolov5l                                24
                                             yolov5x                                36