from collections import defaultdict

def compute_file_metrics(files):
    file_stats = defaultdict(lambda: {"count": 0, "lines": 0})

    for item in files:
        if item.get("isFolder") is True:
            continue
        path = item.get("path", "")
        ext = get_file_extension(path)
        lines = item.get("contentMetadata", {}).get("lineCount", 0)

        file_stats[ext]["count"] += 1
        file_stats[ext]["lines"] += lines or 0

    return file_stats

def get_file_extension(path):
    if "." in path.strip("/"):
        return path.rsplit(".", 1)[-1].lower()
    return "no_extension"
