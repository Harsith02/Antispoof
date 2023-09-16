from ultralytics import YOLO

model = YOLO('yolov8m.pt')

def main():
    model.train(data='Dataset/SplitData/data_offline.yaml', epochs=1)

if __name__ == '__main__':
    main()
