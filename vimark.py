#!/usr/bin/env python3

import argparse
import os
import signal
import sys
from pathlib import Path
from subprocess import Popen, DEVNULL
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MarkReloadHandler(FileSystemEventHandler):
    """Watchdog handler to send SIGHUP to mark on file modification."""
    def __init__(self, mark_pid):
        self.mark_pid = mark_pid

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            # Silent: No prints
            try:
                os.kill(self.mark_pid, signal.SIGHUP)
            except ProcessLookupError:
                # Silent fail
                pass

def main():
    parser = argparse.ArgumentParser(description="Vimark: Integrated Markdown editor and live viewer.")
    parser.add_argument("file", nargs="?", help="Path to the Markdown file (.md)")
    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        sys.exit(1)

    file_path = Path(args.file)
    if not file_path.exists() or not file_path.suffix == '.md':
        print(f"Error: '{file_path}' must be an existing .md file.", file=sys.stderr)
        sys.exit(1)

    # Step 3: Spawn mark as detached background process (non-blocking, no TTY)
    mark_proc = Popen([sys.executable, 'mark.py', str(file_path)], 
                      stdout=DEVNULL, stderr=DEVNULL, 
                      start_new_session=True)  # Detach fully

    if mark_proc.poll() is not None:
        print("Error: Failed to start mark.", file=sys.stderr)
        sys.exit(1)

    mark_pid = mark_proc.pid

    # Step 4: Start file watcher thread for SIGHUP on modify
    event_handler = MarkReloadHandler(mark_pid)
    event_handler.observer = Observer()  # For stop in handler
    event_handler.observer.schedule(event_handler, path=str(file_path.parent), recursive=False)
    event_handler.observer.start()

    try:
        # Step 2: Spawn and block on vim (foreground, inherits TTY)
        vim_exit_code = os.system(f"vim {file_path}")
    except KeyboardInterrupt:
        pass
    finally:
        # Step 5: Stop watcher and kill mark
        event_handler.observer.stop()
        event_handler.observer.join()
        try:
            os.killpg(mark_pid, signal.SIGKILL)  # Kill process group for detached
        except ProcessLookupError:
            pass
        mark_proc.wait()  # Cleanup
        sys.exit(0)

if __name__ == "__main__":
    main()
