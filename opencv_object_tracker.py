import pyrealsense2 as rs
import numpy as np
import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
#分析命令参数
ap=argparse.ArgumentParser()
ap.add_argument("-t","--tracker",type=str,default="csrt",help="OpenCV object tracker type")
args=vars(ap.parse_args())
#创建追踪函数
OPENCV_OBJECT_TRACKER={
    "csrt":cv2.TrackerCSRT_create,
    "kcf":cv2.TrackerKCF_create,
    "boosting":cv2.TrackerBoosting_create,
    "mil":cv2.TrackerMIL_create,
    "tld":cv2.TrackerTLD_create,
    "medianflow":cv2.TrackerMedianFlow_create,
    "mosse":cv2.TrackerMOSSE_create
}
initBB=None
tracker=OPENCV_OBJECT_TRACKER[args["tracker"]]()
# try to enable color and depth frame
pipeline = rs.pipeline()
# Create a config and configure the pipeline to stream
# different resolutions of color and depth streams
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
# Start streaming
pipeline.start(config)
# align depth and color
align_to = rs.stream.color
align = rs.align(align_to)
while True:
    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
    # get depth frame and use location in color image to get point's depth
    depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame().as_frame()
    color_image = np.asanyarray(color_frame.get_data())
    images = color_image
    if not depth_frame or not color_frame:
        continue
        # 目标物体选定之后，我们就可以用以下代码进行处理：
    # 目标物体选定之后，我们就可以用以下代码进行处理：
    if initBB is not None:
        (succss, box) = tracker.update(images)

        if succss:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(images, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # get distance, or we can say, z
            right = x + w
            left = x
            top = y + h
            bottom = y
            point_0 = int((right + left) / 2)
            point_1 = int((top + bottom) / 2)
            point_2 = rs.depth_frame(depth_frame).get_distance(point_0, point_1)

            # recover x,y from int to float to fit to rs2_deproject_pixel_to_point
            # deproject pixel to real point to get x,y in world's coordinate
            point_0 = (right + left) / 2
            point_1 = (top + bottom) / 2
            x_r, y_r, z_r = rs.rs2_deproject_pixel_to_point(color_intrinsics, [point_0, point_1], point_2)
            centre = [x_r, y_r, z_r]
            print(centre)
        fps.update()
        fps.stop()

        info = [
            ("Tracker", args["tracker"]),
            ("Success", "Yes" if succss else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]
        for (i, (k, v)) in enumerate(info):
            text = "{}:{}".format(k, v)
            (H, W) = images.shape[:2]
            cv2.putText(images, text, (10, H - ((i * 20) + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    # present
    color_intrinsics = color_frame.profile.as_video_stream_profile().intrinsics
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', images)
    key=cv2.waitKey(1)&0xFF
    if key == ord("s"):
        initBB = cv2.selectROI("RealSense", images, fromCenter=False, showCrosshair=True)
        tracker.init(images,initBB)
        fps = FPS().start()
    elif key == ord("q"):
        break
pipeline.stop()
cv2.destroyAllWindows()





