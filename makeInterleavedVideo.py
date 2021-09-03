import cv2
import os
import math
import sys
from pathlib import Path
from icecream import ic

promptDir = Path(sys.argv[1] if len(sys.argv) > 1 else input('gimme prompt directory:'))
prompt2Dir = Path(sys.argv[1] if len(sys.argv) > 1 else input('gimme prompt2 directory:'))

if promptDir.exists() is False:
    print("i can't find that")

title = promptDir.stem + prompt2Dir.stem
print(title)

#images = [int(image.stem.split('.')[0][1:]) for image in promptDir.glob('*.png')]
def prepare(prompt):
    images = [int(image.stem.split('.')[0]) for image in prompt.glob('*.png')]
    images.sort()
    images = [str(prompt.joinpath(f'{image}').with_suffix('.png')) for image in images]
    return images
images = prepare(promptDir)
images2 = prepare(prompt2Dir)
frame = cv2.imread(images[0])
h,w,l = frame.shape

if len(images) < len(images2): 
    images2 = images2[:len(images)]
else:
    images = images[:len(images2)]
numFrames = len(images) * 4
#vidType = 'insta'
vidType = 'default'
vidLength = 60
if vidType == 'insta':
    fps = 30
else:
    fps = math.ceil(numFrames / vidLength)
    #vidLength = numFrames / fps
numFramesToBeWritten = int(fps * vidLength)
halfWrite = int(numFramesToBeWritten / 2)
if vidType == 'insta':
    images = images[:halfWrite]
    images2 = images2[:halfWrite]
images.extend(reversed(images))
images2.extend(reversed(images2))
skipInterval = int((ic(numFrames) / ic(numFramesToBeWritten)))
ic(skipInterval)
saveCount = 0
savePath = f'vids/{title}_{vidLength}s0.mp4'
while Path.exists(Path(savePath)):
    savePath = f'{savePath[:-5]}{saveCount}.mp4'
    saveCount += 1
vid = cv2.VideoWriter(savePath, 0, fps, (w, h))

print('stitching video together')
percentage = lambda x: f'{(x / numFrames) * 100}%'
peekInterval = int(0.1 * numFrames)

chunkSize = 1
numChunks = int(numFramesToBeWritten / (2 * chunkSize))

buff1 = []
buff2 = []

for frames, image in enumerate(zip(images, images2), start=1):
    if (vidType == 'insta' and frames % skipInterval == 0) or vidType == 'default':
        vid.write(cv2.imread(image[0]))
        vid.write(cv2.imread(image[1]))
        #buff1.append(image[0])
        #buff2.append(image[1])
    framesWritten = frames * 2
    if framesWritten % peekInterval in [0, 1]:
        print(percentage(framesWritten))
""" for chunk in range(numChunks):
    startdex = chunk * chunkSize
    stopdex = startdex + chunkSize
    writeBuff = buff1[startdex:stopdex]
    writeBuff.extend(buff2[startdex:stopdex])
    for frame in writeBuff:
        vid.write(cv2.imread(frame)) """
cv2.destroyAllWindows()
vid.release()
print('all done')