import argparse
import gi
import cv2

# import required library like Gstreamer and GstreamerRtspServer
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject, GLib


class SensorFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, **properties):
        super(SensorFactory, self).__init__(**properties)
        self.cap = cv2.VideoCapture(opt.link)
        self.image_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.image_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.number_frames = 0
        self.wm = cv2.imread("test.png")
        self.res_wm = cv2.resize(self.wm, (self.image_width, self.image_height))
        self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=BGR,width={},height={},framerate={}/1 ' \
                             '! videoconvert ! video/x-raw,format=I420 ' \
                             '! x264enc speed-preset=ultrafast tune=zerolatency ' \
                             '! rtph264pay config-interval=1 name=pay0 pt=96' \
            .format(self.image_width, self.image_height, self.fps)

    def on_need_data(self, src, length):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.addWeighted(frame, 0.1, self.res_wm, 0.3, 0)
                data = frame.tobytes()
                buf = Gst.Buffer.new_allocate(None, len(data), None)
                buf.fill(0, data)
                buf.duration = self.duration
                timestamp = self.number_frames * self.duration
                buf.pts = buf.dts = int(timestamp)
                buf.offset = timestamp
                self.number_frames += 1
                retval = src.emit('push-buffer', buf)
                print('pushed buffer, frame {}, duration {} ns, durations {} s'.format(self.number_frames,
                                                                                       self.duration,
                                                                                       self.duration / Gst.SECOND))
                if retval != Gst.FlowReturn.OK:
                    print(retval)

    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)

    def do_configure(self, rtsp_media):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)


# Rtsp server implementation where we attach the factory sensor with the stream uri
class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
        super(GstServer, self).__init__(**properties)
        self.factory = SensorFactory()
        self.factory.set_shared(True)
        self.set_service(str(opt.port))
        self.get_mount_points().add_factory("/", self.factory)
        self.attach(None)
        self._print_start_server()

    @staticmethod
    def _print_start_server() -> None:
        print('***************')
        print('Сервер запущен')
        print('***************')


if __name__ == '__main__':
    # getting the required information from the user
    parser = argparse.ArgumentParser()
    parser.add_argument("link", type=str, help="rtsp video stream uri")

    parser.add_argument("port", default=8554, help="port to stream video", type=int)
    opt = parser.parse_args()

    print('Для запуска потока в ffmpeg в командной строке, скопируйте следующую строчку:')
    print(f'ffplay rtsp://127.0.0.1:{opt.port}/')
    print('Ожидайте уведомления о запуске сервера!')

    # initializing the threads and running the stream on loop.
    Gst.init(None)
    server = GstServer()
    loop = GLib.MainLoop()
    loop.run()
