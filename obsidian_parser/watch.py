import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from settings import Settings, parse_settings
from core import get_files
import sys
import os


class Watcher:
    def __init__(self, settings: Settings):
        self._settings = settings
        self.observer = Observer()

    def run(self):
        event_handler = Handler(self._settings)
        vaultDir = os.path.abspath(
            os.path.expanduser(os.path.expandvars(settings.vaultDirectory))
        )

        self.observer.schedule(event_handler, vaultDir, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, settings: Settings, *args, **kwargs):
        super().__init__()
        self._settings = settings

    # @staticmethod
    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type == "created":
            print("Received created event - %s." % event.src_path)
        elif event.event_type == "modified":
            print("Received modified event - %s." % event.src_path)
            get_files(self._settings)
            # else:
            #    print(event)


if __name__ == "__main__":
    settings_file = "settings.json"
    if len(sys.argv) >= 2:
        settings_file = sys.argv[1]
    settings = parse_settings(settings_file)
    # get_files(settings)
    w = Watcher(settings)
    w.run()
