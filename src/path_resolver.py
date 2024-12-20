import os


def retrieve_current_dir() -> str:
    current_path = os.getcwd()
    current_dir = current_path.split("/")[-1]
    return current_dir


def retrieve_latest_dir() -> str:
    dirs = os.listdir("./diary")
    dirs.remove("figures")
    latest_dir = sorted(dirs)[-1]
    return latest_dir
