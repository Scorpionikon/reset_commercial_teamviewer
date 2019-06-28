import os
import pathlib
import subprocess


class TeamViewer:

    def __new__(cls, *args, **kwargs):
        line_len = os.environ
        if line_len["USER"] != "root":
            raise PermissionError("User is no root")
        code = subprocess.call("ifconfig")
        if code > 1:
            raise subprocess.CalledProcessError(code, "ifconfig")
        return super().__new__(cls)

    def del_conf(self):
        self._del_opt_conf()
        self._del_teamviewer_conf()

    def _del_teamviewer_conf(self):
        home = pathlib.Path("/home/")
        user_list = home.iterdir()
        for u in user_list:
            path = u.joinpath(str(u) + "/.config/teamviewer")
            if path.exists():
                self._delete_folder(path)

    def _del_opt_conf(self):
        path = "/opt/teamviewer/config/global.conf"
        if os.path.isfile("/opt/teamviewer/config/global.conf"):
            os.remove(path)

    def _delete_folder(self, pth):
        for sub in pth.iterdir():
            if sub.is_dir():
                self._delete_folder(sub)
            else:
                sub.unlink()
        pth.rmdir()  # if you just want to delete dir content, remove this line

    @staticmethod
    def deamon_stop():
        subprocess.call(['teamviewer', '--daemon', 'stop'])

    @staticmethod
    def deamon_start():
        subprocess.call(['teamviewer', '--daemon', 'start'])




