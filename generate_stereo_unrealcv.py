from unrealcv import client
import sys
import numpy as np
import cv2
import io

camera_poses=np.array([[-106.933, 459.372, 167.895, 0.213, -80.610, 0.000],
[-97.576, 413.807, 168.308, 2.901, -79.483, 0.000],
[-88.197, 346.847, 166.356, 3.644, -89.711, 0.000],
[-82.595, 278.711, 172.572, 5.711, -85.554, 0.000],
[-73.239, 149.936, 176.386, 0.058, -89.777, 0.000],
[-71.879, 58.805, 175.112, 1.199, -89.030, 0.000],
[-69.923, 10.021, 161.958, 4.062, -59.268, 0.000],
[-28.289, -68.530, 159.251, 2.186, -61.090, 0.000],
[-28.289, -68.530, 159.251, 2.831, -43.937, 0.000],
[-28.289, -68.530, 159.251, 1.782, 0.917, 0.000],
[-28.289, -68.530, 159.251, 3.708, 33.667, 0.000],
[-28.289, -68.530, 159.251, 0.167, 92.277, 0.000],
[-32.458, 5.207, 157.922, 2.922, 93.428, 0.000],
[-35.463, 90.040, 156.689, 1.045, 97.168, 0.000],
[-46.087, 180.173, 155.370, 1.167, 96.643, 0.000],
[-52.370, 234.121, 154.580, 1.167, 96.315, 0.000],
[-52.370, 234.121, 154.580, 3.425, 54.474, 0.000],
[-52.370, 234.121, 154.580, 5.985, 18.172, 0.000],
[-52.370, 234.121, 154.580, 5.675, -10.430, 0.000],
[-52.370, 234.121, 154.580, 11.879, -34.452, 0.000],
[-52.370, 234.121, 154.580, 13.122, -66.362, 0.000],
[-52.370, 234.121, 154.580, 14.454, -81.988, 0.000]])

fps = 45
times = np.arange(0,camera_poses.shape[0]*fps,fps)
filled_times = np.arange(0,camera_poses.shape[0]*fps)

filtered_poses = np.array([np.interp(filled_times, times, axis) for axis in camera_poses.T]).T

class UnrealcvStereo():

    def __init__(self):

        client.connect() 
        if not client.isconnected():
            print('UnrealCV server is not running. Run the game downloaded from http://unrealcv.github.io first.')
            sys.exit(-1)

    def __str__(self):
        return client.request('vget /unrealcv/status')

    @staticmethod
    def set_position(pose):

        # Set position of the first camera
        client.request(f'vset /camera/0/location {pose[0]} {pose[1]} {pose[2]}')
        client.request(f'vset /camera/0/rotation {pose[3]} {pose[4]} {pose[5]}')

    @staticmethod
    def get_stereo_pair(eye_distance):
        res = client.request('vset /action/eyes_distance %d' % eye_distance)
        res = client.request('vget /camera/0/lit png')
        left = cv2.imdecode(np.frombuffer(res, dtype='uint8'), cv2.IMREAD_UNCHANGED)
        res = client.request('vget /camera/1/lit png')
        right = cv2.imdecode(np.frombuffer(res, dtype='uint8'), cv2.IMREAD_UNCHANGED)

        return left, right

    @staticmethod
    def convert_depth(PointDepth, f=320):
        H = PointDepth.shape[0]
        W = PointDepth.shape[1]
        i_c = np.float(H) / 2 - 1
        j_c = np.float(W) / 2 - 1
        columns, rows = np.meshgrid(np.linspace(0, W-1, num=W), np.linspace(0, H-1, num=H))
        DistanceFromCenter = ((rows - i_c)**2 + (columns - j_c)**2)**(0.5)
        PlaneDepth = PointDepth / (1 + (DistanceFromCenter / f)**2)**(0.5)
        return PlaneDepth

    @staticmethod
    def get_depth():

        res = client.request('vget /camera/0/depth npy')
        point_depth = np.load(io.BytesIO(res))

        return UnrealcvStereo.convert_depth(point_depth)


    @staticmethod
    def color_depth(depth_map, max_dist):

        norm_depth_map = 255*(1-depth_map/max_dist)
        norm_depth_map[norm_depth_map < 0] =0
        norm_depth_map[depth_map == 0] =0

        return cv2.applyColorMap(cv2.convertScaleAbs(norm_depth_map,1), cv2.COLORMAP_MAGMA)


if __name__ == '__main__':

    eye_distance = 10
    max_depth = 5
    stereo_generator = UnrealcvStereo()

    for pose in filtered_poses:

        stereo_generator.set_position(pose)

        # Set the eye distance
        left, right = stereo_generator.get_stereo_pair(eye_distance)

        depth_map = stereo_generator.get_depth()

        color_depth_map = stereo_generator.color_depth(depth_map, max_depth)
        left = cv2.cvtColor(left, cv2.COLOR_BGRA2BGR)
        right = cv2.cvtColor(right, cv2.COLOR_BGRA2BGR)

        combined_image = np.hstack((left, right, color_depth_map))

        cv2.imshow("stereo", combined_image)
       
        # Press key q to stop
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

