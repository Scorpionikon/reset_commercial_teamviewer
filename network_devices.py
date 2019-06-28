import re

import psutil
from mac import MAC
from subprocess import call, CalledProcessError, STDOUT, DEVNULL


class Device:

    def __init__(self, name, ip_address, mac_address, ):
        self.name = name
        self.ip = ip_address
        self.mac = MAC(mac_address)

    def __str__(self):
        return str(self.__dict__)

    def change_mac(self):
        self.stop()
        self.mac.reset_mac()
        command = ['ifconfig', self.name, 'hw', 'ether', str(self.mac)]
        code = call(command, stdout=DEVNULL, stderr=STDOUT)
        if code > 1:
            self.change_mac()
        self.start()

    def stop(self):
        command = ['ifconfig', self.name, "down"]
        code = call(command)
        if code > 1:
            raise CalledProcessError(code, command)

    def start(self):
        command = ['ifconfig', self.name, "up"]
        code = call(command)
        if code > 1:
            raise CalledProcessError(code, command)


class Devices:

    def __init__(self, exclude=None):
        if exclude is None:
            self._exclude = []
        elif isinstance(exclude, str):
            self._exclude = [exclude]
        elif isinstance(exclude, list):
            self._exclude = exclude
        device_list = psutil.net_if_addrs()
        for name, values in device_list.items():
            ip, mac = self._find_address(values)
            if ip not in ["127.0.0.1", "172.0.0.1"] and name not in self._exclude and \
                    mac not in ["00:00:00:00:00:00", "ff:ff:ff:ff:ff:ff", ""]:
                setattr(self, name, Device(name, ip, mac))

    @staticmethod
    def _find_address(device_data):
        ip_addr, mac_addr = None, None
        mac_mask = (r"[\d,a,b,c,d,e,f][\d,a,b,c,d,e,f]:" * 6)[:-1]
        ip_mask = r"\d*\.\d*\.\d*\.\d*"
        for d_ in device_data:
            d_ = d_.address
            if bool(mac_addr) is False:
                mac_addr = re.findall(mac_mask, d_) if bool(d_) else ""
            if bool(ip_addr) is False:
                ip_addr = re.findall(ip_mask, d_) if bool(d_) else ""
        yield ip_addr[0] if bool(ip_addr) else ""
        yield mac_addr[0] if bool(mac_addr) else ""

    def __iter__(self):
        iter_obg = self.__dict__
        iter_obg.pop("_exclude")
        for device in iter_obg.values():
            yield device

    def change_mac_all(self):
        [dev.change_mac() for dev in self]


if __name__ == '__main__':
    dev = Devices()
    name_device = input("enter name device: ")
    for d in dev:
        if d.name == name_device:
            d.change_mac()
