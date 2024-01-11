from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        print(f'File {event.src_path} has been modified.')

if __name__ == "__main__":
    path = '\\Users\\c0a21155fe\\try'  # 監視するディレクトリのパスを指定してください
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        print("ファイルの変更を監視中...")
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

