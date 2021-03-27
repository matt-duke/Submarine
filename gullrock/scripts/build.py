import subprocess as sp
from pathlib import Path
import shutil

BUILD_TYPE = "Debug"
APP_DIR = "apps"
APPS = ["app_manager",
        "mcu_manager",
        "config_controller",
        "camera_controller",
        "io_controller",
        "motion_controller"
]
APPS = ["app_manager"]
THIRPARTY_DIR = Path(__file__).parent.absolute().joinpath("thirdparty")

def build_apps():
    for app in APPS:
        try:
            cwd = Path(__file__).parent.absolute()
            cwd = cwd.joinpath(APP_DIR, app)
            print(cwd)
            cmd = ["cmake", "-DCMAKE_BUILD_TYPE={}".format(BUILD_TYPE), "CMakeLists.txt"]
            with sp.Popen(cmd, cwd=cwd, stdout=sp.PIPE) as proc:
                print(proc.stdout.read())
            cmd = ["cmake", "--build", "CMakeLists.txt"]
            with sp.Popen(cmd, cwd=cwd, stdout=sp.PIPE) as proc:
                print(proc.stdout.read())
        except Exception as e:
            print("Error making {}: {}".format(app, e))

def redis_time_series():
    cmd = ["make", "build"]
    cwd = THIRPARTY_DIR.joinpath("RedisTimeSeries")
    try:
        with sp.Popen(cmd, cwd=cwd, stdout=sp.PIPE) as proc:
            print(proc.stdout.read())
        for file in cwd.joinpath("bin").iterdir():
            print(file)
            if not file.is_file():
                continue
            if BUILD_TYPE == "Debug":
                shutil.copy(file, Path("/apps").joinpath(file.name))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    #build_apps()
    redis_time_series()