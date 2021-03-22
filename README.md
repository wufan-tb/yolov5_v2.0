## yolov5 v2.0 from [yolov5](https://github.com/ultralytics/yolov5)

# 1.preparpe data:
    python prepare_data.py --classes person,fuwuqi --dataset /data/jiadaiwu --split 0.8

# 2.change {dataset}.yaml

# 3.Train:
    python train.py --data jiadaiwu.yaml --cfg yolov5l.yaml --weights '' --batch-size 4
                                               yolov5m                                40
                                               yolov5l                                24
                                               yolov5x                                16