import cv2
import os
import math
import sys
from pathlib import Path

promptDir = Path(sys.argv[1] if len(sys.argv) > 1 else input('gimme prompt directory:'))

if promptDir.exists() is False:
    print("i can't find that")

title = promptDir.stem
print(title)

#images = [int(image.stem.split('.')[0][1:]) for image in promptDir.glob('*.png')]
images = [int(image.stem.split('.')[0]) for image in promptDir.glob('*.png')]
images.sort()
images = [str(promptDir.joinpath(f'{image}').with_suffix('.png')) for image in images]
frame = cv2.imread(images[0])
h,w,l = frame.shape

vidLength = 30
images.extend(reversed(images))
numFrames = len(images)
fps = math.ceil(numFrames / vidLength)

vid = cv2.VideoWriter(f'vids/{title}_{vidLength}s.mp4', 0, fps, (w, h))

print('stitching video together')
percentage = lambda x: f'{(x / numFrames) * 100}%'
peekInterval = 0.1 * numFrames
for framesWritten, image in enumerate(images, start=1):
    vid.write(cv2.imread(image))
    if framesWritten % peekInterval == 0:
        print(percentage(framesWritten))
cv2.destroyAllWindows()
vid.release()
print('all done')