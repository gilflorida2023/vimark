#!/usr/bin/env python3

import argparse
import signal
import sys
from pathlib import Path
from threading import Event

import markdown
from PyQt6.QtCore import QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow

# Markdown extensions for complete GFM support (tables, syntax highlighting, etc.)
EXTENSIONS = [
    'markdown.extensions.tables',
    'markdown.extensions.fenced_code',
    'markdown.extensions.codehilite',
    'pymdownx.highlight',  # Better syntax highlighting
    'pymdownx.superfences',  # Nested code blocks
    'pymdownx.inlinehilite',  # Inline code highlighting
    'markdown.extensions.md_in_html',  # Markdown in HTML tags
    'pymdownx.arithmatex',  # Math support (optional)
    'pymdownx.tasklist',  # Task lists
    'pymdownx.tilde',  # Strikethrough
]

class MarkdownWebPage(QWebEnginePage):
    """Custom WebPage to handle reload signals."""
    reload_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reload_signal.connect(self._reload_slot)

    @pyqtSlot()
    def _reload_slot(self):
        """Slot to trigger page reload."""
        self.reload()

class MarkdownViewer(QMainWindow):
    def __init__(self, file_path: Path, reload_event: Event, quit_event: Event):
        super().__init__()
        self.file_path = file_path
        self.reload_event = reload_event
        self.quit_event = quit_event
        self.web_view = QWebEngineView()
        self.page = MarkdownWebPage(self.web_view)
        self.web_view.setPage(self.page)
        
        # Set up timer to poll events (for signal responsiveness)
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_events)
        self.timer.start(100)  # Poll every 100ms
        
        self.setCentralWidget(self.web_view)
        self.setWindowTitle(f"Render: {file_path.name}")
        self.resize(800, 600)
        
        # Initial load
        self.load_markdown()

    def load_markdown(self):
        """Convert Markdown to HTML and load into web view."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                md_text = f.read()
        except IOError as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return
        
        md = markdown.Markdown(extensions=EXTENSIONS)
        html = md.convert(md_text)
        
        # Wrap in basic HTML for styling (light theme)
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{self.file_path.name}</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    max-width: 800px; 
                    margin: 0 auto; 
                    padding: 20px; 
                    background-color: white; 
                    color: black; 
                }}
                h1 {{ color: #333; }}
                h2 {{ color: #555; }}
                h3 {{ color: #666; }}
                code {{ background: #f4f4f4; padding: 2px 4px; }}
                pre {{ background: #f4f4f4; padding: 10px; overflow: auto; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                blockquote {{ border-left: 4px solid #ccc; margin: 0; padding-left: 16px; color: #666; }}
                ul, ol {{ padding-left: 20px; }}
                li {{ margin-bottom: 4px; }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        self.web_view.setHtml(full_html)
        print(f"Markdown loaded and rendered for: {self.file_path}")

    def check_events(self):
        """Poll for reload or quit events."""
        if self.reload_event.is_set():
            print("Reload triggered!")  # Debug print
            self.reload_event.clear()
            self.load_markdown()
        if self.quit_event.is_set():
            print("Quit triggered!")  # Debug print
            self.quit_event.clear()
            self.close()

    def closeEvent(self, event: QCloseEvent):
        """Handle window close."""
        self.quit_event.set()
        event.accept()

def signal_handler(signum, frame):
    global reload_event, quit_event
    if signum == signal.SIGINT:  # Ctrl+C
        print("SIGINT received!")  # Debug print
        quit_event.set()
    elif signum == signal.SIGHUP:  # Reload
        print("SIGHUP received!")  # Debug print
        reload_event.set()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Graphical Markdown renderer with live reload.")
    parser.add_argument("file", help="Path to the Markdown file")
    args = parser.parse_args()
    
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    
    # Global events for signals
    reload_event = Event()
    quit_event = Event()
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    
    # Set up Qt app
    app = QApplication(sys.argv)
    viewer = MarkdownViewer(file_path, reload_event, quit_event)
    viewer.show()
    
    sys.exit(app.exec())
