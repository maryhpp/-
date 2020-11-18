import os
import cv2

def video_to_frames(video_src):
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(video_src)

    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    frames = []
    # Read until video is completed
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            frames.append(frame)

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

    return frames, fps, size

def write_to_video(frames, video_dst, fps, size):
    """
    cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'),MPEG-4编码
    cv2.VideoWriter_fourcc('F', 'L', 'V', '1'),Flash编码
    """
    fourcc = cv2.VideoWriter_fourcc("X", "V", "I", "D")
    writer = cv2.VideoWriter(video_dst, fourcc, fps, size)
    for i in range(len(frames)):
        writer.write(frames[i])

if __name__ == '__main__':
    root_dir = os.getcwd()
	#待转换视频路径
    video_src = os.path.join(root_dir, 'video','test.mp4')
    frames, fps, size=video_to_frames(video_src)
    #图片序列保存路径
    out_dir = os.path.join(root_dir, 'output')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for i in range(len(frames)):
        cv2.imwrite(os.path.join(out_dir,str(i)+'.jpg'),frames[i])	
    #图片序列转为视频
    video_dst = os.path.join(root_dir, 'video','save.mp4')
    write_to_video(frames, video_dst, fps, size)
    print('done')