from helper import run_cmd


class Flatpak:
    @staticmethod
    def do(cmd):
        """run an unimplemented command"""
        run_cmd(f"flatpak {cmd}")

    @staticmethod
    def update():
        Flatpak.do("update")

    @staticmethod
    def remote_add(name, url, *args):
        cmd = f"remote-add {name} {url}"
        for arg in args:
            cmd += " " + arg
        Flatpak.do(cmd)

    @staticmethod
    def install(package):
        Flatpak.do(f"install -y {package}")
