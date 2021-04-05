import subprocess , os

def clone(link , path):
    print(path)
    if not os.path.exists(path):
        os.makedirs(path)
    subprocess.call(f"git clone {link} {path}" , shell=True)

