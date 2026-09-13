"""
carla_conversions.py  --  GP1 helper module (ENPM818Z)

Message-format plumbing for turning CARLA sensor callbacks into ROS 2
messages. None of this is the point of GP1, so it is provided.

What you still have to write yourself:
  * spawning the vehicle and attaching the sensors
  * reading every sensor parameter from carla_config.yaml
  * cleaning up actors on shutdown
  * the LiDAR-to-camera extrinsic in Task 5

Drop this file in ads_pipeline/ads_pipeline/ and import from it:

    from ads_pipeline.carla_conversions import (
        carla_timestamp_to_ros, carla_image_to_ros,
        carla_lidar_to_pointcloud2, carla_radar_to_markerarray,
        carla_gnss_to_navsatfix, carla_imu_to_imu,
        static_transforms_from_config,
    )
"""

import numpy as np
from builtin_interfaces.msg import Time
from geometry_msgs.msg import TransformStamped
from sensor_msgs.msg import Image, PointCloud2, PointField, NavSatFix, Imu
from std_msgs.msg import Header, ColorRGBA
from visualization_msgs.msg import Marker, MarkerArray
import tf_transformations


# --------------------------------------------------------------------------
# Timestamps
# --------------------------------------------------------------------------
def carla_timestamp_to_ros(carla_seconds: float) -> Time:
    """Convert a CARLA sensor timestamp into a ROS 2 Time.

    Use the timestamp carried on the sensor measurement, never the time the
    callback happened to run. The measurement records when the data was
    captured; the callback records when Python got around to it, and the gap
    between them is exactly the synchronisation error L2 warns about.
    """
    stamp = Time()
    stamp.sec = int(carla_seconds)
    stamp.nanosec = int((carla_seconds - int(carla_seconds)) * 1e9)
    return stamp


def _header(frame_id: str, carla_seconds: float) -> Header:
    header = Header()
    header.stamp = carla_timestamp_to_ros(carla_seconds)
    header.frame_id = frame_id
    return header


# --------------------------------------------------------------------------
# Cameras
# --------------------------------------------------------------------------
def carla_image_to_ros(carla_image, frame_id: str,
                       kind: str = "rgb") -> Image:
    """Convert a CARLA camera measurement into sensor_msgs/Image.

    kind:
      "rgb"     -- sensor.camera.rgb, published as bgr8
      "depth"   -- sensor.camera.depth, decoded to metres, 32FC1
      "semseg"  -- sensor.camera.semantic_segmentation, label ids as mono8

    Note that depth and semantic segmentation are ground truth rather than
    hardware. Use them to check your work, never to depend on.
    """
    buf = np.frombuffer(carla_image.raw_data, dtype=np.uint8)
    buf = buf.reshape((carla_image.height, carla_image.width, 4))

    msg = Image()
    msg.header = _header(frame_id, carla_image.timestamp)
    msg.height = carla_image.height
    msg.width = carla_image.width
    msg.is_bigendian = 0

    if kind == "rgb":
        data = buf[:, :, :3]                      # BGRA -> BGR
        msg.encoding = "bgr8"
        msg.step = msg.width * 3
    elif kind == "depth":
        # CARLA packs depth into R, G and B. Decode to metres.
        b = buf[:, :, 0].astype(np.float32)
        g = buf[:, :, 1].astype(np.float32)
        r = buf[:, :, 2].astype(np.float32)
        normalized = (r + g * 256.0 + b * 65536.0) / (256.0**3 - 1.0)
        data = (normalized * 1000.0).astype(np.float32)   # metres
        msg.encoding = "32FC1"
        msg.step = msg.width * 4
    elif kind == "semseg":
        data = buf[:, :, 2].copy()                # label id lives in R
        msg.encoding = "mono8"
        msg.step = msg.width
    else:
        raise ValueError(f"unknown camera kind: {kind!r}")

    msg.data = data.tobytes()
    return msg


# --------------------------------------------------------------------------
# LiDAR
# --------------------------------------------------------------------------
def carla_lidar_to_pointcloud2(measurement, frame_id: str) -> PointCloud2:
    """Convert a CARLA sensor.lidar.ray_cast measurement to PointCloud2.

    CARLA gives a flat float32 buffer of (x, y, z, intensity). Its y axis
    points the opposite way to the ROS convention, so it is negated here.
    The result is x forward, y left, z up, which is what RViz2 expects.
    """
    pts = np.frombuffer(measurement.raw_data, dtype=np.float32)
    pts = np.reshape(pts, (-1, 4)).copy()
    pts[:, 1] = -pts[:, 1]                        # CARLA y -> ROS y

    msg = PointCloud2()
    msg.header = _header(frame_id, measurement.timestamp)
    msg.height = 1
    msg.width = pts.shape[0]
    msg.is_dense = True
    msg.is_bigendian = False
    msg.fields = [
        PointField(name="x", offset=0, datatype=PointField.FLOAT32, count=1),
        PointField(name="y", offset=4, datatype=PointField.FLOAT32, count=1),
        PointField(name="z", offset=8, datatype=PointField.FLOAT32, count=1),
        PointField(name="intensity", offset=12,
                   datatype=PointField.FLOAT32, count=1),
    ]
    msg.point_step = 16
    msg.row_step = msg.point_step * msg.width
    msg.data = pts.tobytes()
    return msg


def lidar_points_xyz(measurement) -> np.ndarray:
    """Return an (N, 3) array of LiDAR points in the SENSOR frame.

    This is what Task 5 projects. It does NOT flip y, because Task 5 works
    in CARLA's own convention and converts once, inside the extrinsic.
    """
    pts = np.frombuffer(measurement.raw_data, dtype=np.float32)
    return np.reshape(pts, (-1, 4))[:, :3].copy()


# --------------------------------------------------------------------------
# RADAR
# --------------------------------------------------------------------------
def carla_radar_to_markerarray(measurement, frame_id: str,
                               max_velocity: float = 20.0) -> MarkerArray:
    """Convert a CARLA sensor.other.radar measurement to a MarkerArray.

    There is no standard ROS 2 message for radar detections, so GP1 uses
    MarkerArray: one small sphere per detection, coloured by radial
    velocity. Red is closing, blue is receding.
    """
    stamp = carla_timestamp_to_ros(measurement.timestamp)
    array = MarkerArray()

    for i, det in enumerate(measurement):
        # CARLA reports azimuth and altitude in radians, depth in metres.
        x = det.depth * np.cos(det.altitude) * np.cos(det.azimuth)
        y = det.depth * np.cos(det.altitude) * np.sin(det.azimuth)
        z = det.depth * np.sin(det.altitude)

        m = Marker()
        m.header.stamp = stamp
        m.header.frame_id = frame_id
        m.ns = "radar"
        m.id = i
        m.type = Marker.SPHERE
        m.action = Marker.ADD
        m.pose.position.x = float(x)
        m.pose.position.y = float(-y)          # CARLA y -> ROS y
        m.pose.position.z = float(z)
        m.pose.orientation.w = 1.0
        m.scale.x = m.scale.y = m.scale.z = 0.4

        t = float(np.clip(
            (det.velocity + max_velocity) / (2 * max_velocity), 0.0, 1.0))
        m.color = ColorRGBA(r=1.0 - t, g=0.1, b=t, a=0.9)
        m.lifetime.nanosec = 200_000_000       # 0.2 s, so stale dots clear
        array.markers.append(m)

    return array


# --------------------------------------------------------------------------
# GNSS and IMU
# --------------------------------------------------------------------------
def carla_gnss_to_navsatfix(measurement, frame_id: str) -> NavSatFix:
    """Convert a CARLA sensor.other.gnss measurement to NavSatFix."""
    msg = NavSatFix()
    msg.header = _header(frame_id, measurement.timestamp)
    msg.latitude = measurement.latitude
    msg.longitude = measurement.longitude
    msg.altitude = measurement.altitude
    msg.status.status = 0                      # STATUS_FIX
    msg.status.service = 1                     # SERVICE_GPS
    msg.position_covariance_type = 0           # COVARIANCE_TYPE_UNKNOWN
    return msg


def carla_imu_to_imu(measurement, frame_id: str) -> Imu:
    """Convert a CARLA sensor.other.imu measurement to sensor_msgs/Imu.

    CARLA reports compass as radians clockwise from north. ROS expects a
    counter-clockwise yaw from east, hence the conversion below.
    """
    msg = Imu()
    msg.header = _header(frame_id, measurement.timestamp)

    yaw = -measurement.compass + np.pi / 2.0
    q = tf_transformations.quaternion_from_euler(0.0, 0.0, yaw)
    msg.orientation.x, msg.orientation.y = q[0], q[1]
    msg.orientation.z, msg.orientation.w = q[2], q[3]

    acc, gyr = measurement.accelerometer, measurement.gyroscope
    msg.linear_acceleration.x = acc.x
    msg.linear_acceleration.y = -acc.y         # CARLA y -> ROS y
    msg.linear_acceleration.z = acc.z
    msg.angular_velocity.x = -gyr.x
    msg.angular_velocity.y = gyr.y
    msg.angular_velocity.z = -gyr.z
    return msg


# --------------------------------------------------------------------------
# TF
# --------------------------------------------------------------------------
def static_transforms_from_config(mounts: dict,
                                  parent: str = "ego_vehicle") -> list:
    """Build the static TF tree from the mount transforms in your YAML.

    RViz2 cannot draw a point cloud and a camera image in the same scene
    until it knows where those sensors sit relative to one another, and that
    is what TF is for. Without this, RViz2 reports
    "Fixed Frame [map] does not exist" and shows nothing.

    `mounts` maps a frame_id to a dict with keys x, y, z, roll, pitch, yaw,
    matching the structure of carla_config.yaml. Publish the result with a
    tf2_ros.StaticTransformBroadcaster.
    """
    out = []
    for frame_id, m in mounts.items():
        t = TransformStamped()
        t.header.frame_id = parent
        t.child_frame_id = frame_id
        t.transform.translation.x = float(m.get("x", 0.0))
        t.transform.translation.y = float(-m.get("y", 0.0))   # CARLA -> ROS
        t.transform.translation.z = float(m.get("z", 0.0))
        q = tf_transformations.quaternion_from_euler(
            np.radians(float(m.get("roll", 0.0))),
            np.radians(-float(m.get("pitch", 0.0))),
            np.radians(-float(m.get("yaw", 0.0))),
        )
        t.transform.rotation.x, t.transform.rotation.y = q[0], q[1]
        t.transform.rotation.z, t.transform.rotation.w = q[2], q[3]
        out.append(t)
    return out
