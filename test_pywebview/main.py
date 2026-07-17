import time
import math
import sys
import threading
import multiprocessing

from flask import Flask, render_template, jsonify

from follow_wall import LidarExplorer


app = Flask(__name__)

latest_data = {
    "scan": [],
    "point_count": 0,
    "min_distance": 0.0,
    "max_distance": 0.0,
    "running": False,
    "coordinate_type": "local_mm"
}

run_event = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status")
def status():
    return jsonify(latest_data)


@app.route("/api/start")
def start():
    if run_event is not None:
        run_event.set()

    latest_data["running"] = True

    return jsonify({
        "result": "started"
    })


@app.route("/api/stop")
def stop():
    if run_event is not None:
        run_event.clear()

    latest_data["running"] = False
    latest_data["scan"] = []
    latest_data["point_count"] = 0

    return jsonify({
        "result": "stopped"
    })


def flask_run():
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )


def main():
    multiprocessing.set_start_method(
        "spawn",
        force=True
    )

    print("=========================================")
    print(" LiDAR 자체 검증 시스템 시작")
    print("=========================================")

    data_queue = multiprocessing.Queue(maxsize=3)
    stop_event = multiprocessing.Event()

    global run_event
    run_event = multiprocessing.Event()
    run_event.clear()

    lidar_process = LidarExplorer(
        data_queue=data_queue,
        stop_event=stop_event,
        run_event=run_event
    )

    flask_thread = threading.Thread(
        target=flask_run,
        daemon=True
    )

    try:
        flask_thread.start()
        lidar_process.start()

        print("[System] Flask Server Started")
        print("[System] Open Browser : http://192.168.0.58:5000")
        print("[System] 시작 버튼을 누르면 LiDAR 스캔을 표시합니다.")
        print("[System] 종료하려면 Ctrl+C")

        while True:
            received_data = None

            try:
                while not data_queue.empty():
                    received_data = data_queue.get_nowait()
            except Exception:
                pass

            if received_data is not None:
                latest_data.update(received_data)

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n[System] 사용자 종료 감지")

    finally:
        stop_event.set()
        run_event.clear()

        if lidar_process.is_alive():
            lidar_process.join(timeout=3.0)

        if lidar_process.is_alive():
            print("[System] LiDAR 프로세스 강제 종료")
            lidar_process.terminate()
            lidar_process.join()

        print("=========================================")
        print(" LiDAR 검증 시스템 종료")
        print("=========================================")

        sys.exit(0)


if __name__ == "__main__":
    main()