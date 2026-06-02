import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config.config import Config
from utils.logger import logger
from sentinel.processor import file_processor

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            filepath = event.src_path
            logger.info(f"New file detected: {filepath}")
            self.process_when_ready(filepath)

    def process_when_ready(self, filepath):
        """
        Waits until the file is completely written by checking its size over time.
        """
        previous_size = -1
        current_size = -1
        # Wait until the file size stops growing
        while True:
            try:
                current_size = os.path.getsize(filepath)
                if current_size == previous_size and current_size > 0:
                    break
                previous_size = current_size
                time.sleep(Config.WAIT_SECONDS)
            except OSError as e:
                # File might still be locked or just deleted
                logger.debug(f"Waiting for file {filepath} to be accessible... ({e})")
                time.sleep(Config.WAIT_SECONDS)
            
        logger.info(f"File {filepath} is ready. Processing...")
        file_processor.process(filepath)

def main():
    # Ensure the watch directory exists
    os.makedirs(Config.DIR_WATCH, exist_ok=True)
    
    logger.info(f"Sentinel starting... Monitoring directory: {Config.DIR_WATCH}")
    
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, Config.DIR_WATCH, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Sentinel stopping...")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
