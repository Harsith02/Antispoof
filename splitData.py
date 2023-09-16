import shutil
import os
import random
from itertools import islice

outputFolderPath = "Dataset/SplitData"
inputFolderPath = "Dataset/all"
splitRatio = {"train": 0.7, "test": 0.2, "val": 0.1}
classes = ["fake", "real"]

try:
    shutil.rmtree(outputFolderPath)
    # print("Removed Directory")
except OSError as e:
    os.mkdir(outputFolderPath)

os.makedirs(f"{outputFolderPath}/train/images", exist_ok=True)
os.makedirs(f"{outputFolderPath}/train/labels", exist_ok=True)
os.makedirs(f"{outputFolderPath}/val/images", exist_ok=True)
os.makedirs(f"{outputFolderPath}/val/labels", exist_ok=True)
os.makedirs(f"{outputFolderPath}/test/images", exist_ok=True)
os.makedirs(f"{outputFolderPath}/test/labels", exist_ok=True)

listNames = os.listdir(inputFolderPath)
# print(listNames)
# print(len(listNames))
uniqueNames = []
for name in listNames:
    uniqueNames.append(name.split('.')[0])
uniqueNames = list(set(uniqueNames))
# print(len(uniqueNames))

random.shuffle(uniqueNames)

lenTrain = int(len(uniqueNames)*splitRatio['train'])
lenVal = int(len(uniqueNames)*splitRatio['val'])
lenTest = int(len(uniqueNames)*splitRatio['test'])

if len(uniqueNames) != lenTrain+lenTest+lenVal:
    remaining = len(uniqueNames) - (lenTrain+lenTest+lenVal)
    lenTrain += remaining

lengthToSplit = [lenTrain, lenVal, lenTest]
Input = iter(uniqueNames)
Output = [list(islice(Input, elem))for elem in lengthToSplit]
print(f"Total Images: {len(uniqueNames)} \n Split: {len(Output[0])} {len(Output[1])} {len(Output[2])}")

sequence = ['train', 'val', 'test']
for i, out in enumerate(Output):
    for fileName in out:
        shutil.copy(f'{inputFolderPath}/{fileName}.jpg', f'{outputFolderPath}/{sequence[i]}/images/{fileName}.jpg')
        shutil.copy(f'{inputFolderPath}/{fileName}.txt', f'{outputFolderPath}/{sequence[i]}/labels/{fileName}.txt')
print("Split Process Completed.........")

dataYaml = f'path: ../Data\n\
train: ../train/images\n\
val: ../val/images\n\
test: ../test/images\n\
\n\
nc: {len(classes)}\n\
names: {classes}'

f = open(f"{outputFolderPath}/data.yaml", 'a')
f.write(dataYaml)
f.close()
print("DataYaml Created..........")
