from pathlib import Path
import threading

import webview

from backend.server import CarApiServer

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"


def main():
    server = CarApiServer(FRONTEND_DIR)

    # Flask 서버 실행
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # UI 창 생성
    webview.create_window(
        title="RC Car Controller",
        url="http://127.0.0.1:5000",
        width=700,
        height=500,
        resizable=True
    )

    webview.start()


if __name__ == "__main__":
    main()
