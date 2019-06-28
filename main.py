from linux_command import TeamViewer
from network_devices import Devices

if __name__ == '__main__':
    term = TeamViewer()
    term.deamon_stop()
    term.del_conf()
    device = Devices(exclude=["lo", "anbox0"])
    device.change_mac_all()
    term.deamon_start()