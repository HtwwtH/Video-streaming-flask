import cv2
import threading
from VideoGet import VideoGet
from flask import Flask, render_template, Response

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    def gen():
        while True:
            if video_getter.stopped:
                video_getter.stop()
                break
            video_getter.e.set()                                          # без ожидания evt - закомментить
            frame = video_getter.read()
            frame = cv2.resize(frame, (768, 432))

            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

            # time.sleep(0.035)

    @app.route('/video_feed')
    def video_feed():
        return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

    app.run(host='127.0.0.1', port = 61)

if __name__ == '__main__':
    e = threading.Event()                                           # без ожидания evt - закомментить
    source = 'sunset.mp4'
    cap = cv2.VideoCapture(source)

    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    video_getter = VideoGet(source,e).start()
    # video_getter = VideoGet(source).start()                                          # без ожидания evt

    app = create_app()