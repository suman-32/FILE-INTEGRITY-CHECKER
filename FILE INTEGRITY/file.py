import os
import hashlib
import json
import argparse
import time
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False

BASELINE_FILE = "baseline_hashes.json"

def calculate_hash(filepath, algorithm="sha256", chunk_size=65536):
    h = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()

def load_baseline():
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_baseline(data):
    with open(BASELINE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def scan_directory(directory, algorithm="sha256"):
    curr = {}
    for root, _, files in os.walk(directory):
        for fname in files:
            path = os.path.join(root, fname)
            try:
                curr[path] = calculate_hash(path, algorithm)
            except (IOError, PermissionError):
                continue
    return curr

def compare_hashes(baseline, current):
    modified = [f for f in current if f in baseline and baseline[f] != current[f]]
    new = [f for f in current if f not in baseline]
    deleted = [f for f in baseline if f not in current]
    return {"modified": modified, "new": new, "deleted": deleted}

class WatchHandler(FileSystemEventHandler):
    def __init__(self, algo="sha256"):
        self.algo = algo
        self.base = load_baseline()

    def on_any_event(self, event):
        if event.is_directory: return
        event_type = event.event_type
        path = event.src_path
        if event_type in ("created", "modified"):
            try:
                new_hash = calculate_hash(path, self.algo)
            except Exception:
                return
            old = self.base.get(path)
            if old is None:
                print(f"[NEW] {path}")
            elif old != new_hash:
                print(f"[MODIFIED] {path}")
            self.base[path] = new_hash
        elif event_type == "deleted":
            print(f"[DELETED] {path}")
            if path in self.base:
                del self.base[path]
        save_baseline(self.base)

def init_baseline(dirpath, algo):
    baseline = scan_directory(dirpath, algo)
    save_baseline(baseline)
    print("Baseline initialized with", len(baseline), "files.")

def check_baseline(dirpath, algo):
    baseline = load_baseline()
    current = scan_directory(dirpath, algo)
    changes = compare_hashes(baseline, current)
    save_baseline(current)
    return changes

def main():
    parser = argparse.ArgumentParser(description="File Integrity Checker")
    parser.add_argument("mode", choices=["init", "check", "watch"], help="init: build baseline; check: compare; watch: continuous")
    parser.add_argument("directory", help="Target directory")
    parser.add_argument("--algo", choices=["sha256", "sha512"], default="sha256", help="Hash algorithm")
    args = parser.parse_args()

    if args.mode == "init":
        init_baseline(args.directory, args.algo)
    elif args.mode == "check":
        changes = check_baseline(args.directory, args.algo)
        print("Modified files:", *changes["modified"], sep="\n - ")
        print("New files:", *changes["new"], sep="\n - ")
        print("Deleted files:", *changes["deleted"], sep="\n - ")
    elif args.mode == "watch":
        if not WATCHDOG_AVAILABLE:
            print("Watchdog not installed; install with: pip install watchdog")
            return
        handler = WatchHandler(args.algo)
        observer = Observer()
        observer.schedule(handler, path=args.directory, recursive=True)
        observer.start()
        print("Watching directory:", args.directory)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
