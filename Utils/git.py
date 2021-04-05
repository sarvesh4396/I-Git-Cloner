from shutil import which
def is_tool():
    return which('git') is not None
