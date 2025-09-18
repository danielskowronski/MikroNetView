from dataclasses import dataclass
import ipaddress
from ouilookup import OuiLookup
from RegInfo import RegInfo
import json
import re


from functools import lru_cache

_global_oui = OuiLookup()


@lru_cache(maxsize=1024)
def _lookup_oui_cached(mac: str) -> dict:
    return _global_oui.query(mac)[0]


def split_time_parts(s):
    return re.findall(r"\d+[wdhms]", s)


def time_fmt(s):
    stp = split_time_parts(s)
    if len(stp) >= 2:
        return stp[0].rjust(3, "0") + "" + stp[1].rjust(3, "0")
    elif len(stp) == 1:
        return stp[0].rjust(6, "_")
    else:
        return "______"


LeaseInfoProps = "status,comment,id,address,active-address,active-mac-address,mac-address,host-name,dynamic,last-seen"


# FIXME: this is direct import of prototype, it must be improved
@dataclass
class LeaseInfo:
    id: str
    net: str
    ip: ipaddress.IPv4Address
    mac: str
    macFmt: str
    oui: str
    status: str
    lastSeen: str
    hostname: str
    dynamic: bool
    name: str
    comment: str
    details: str
    locallyAdministered: bool
    connection: str
    isWireless: bool

    def addWirelessInfo(self, reginfo: RegInfo | None):
        self.reginfo = reginfo
        if reginfo:
            self.isWireless = True
            self.connection = (
                f"{reginfo.getBandInfo()} @{reginfo.interface[0]} {reginfo.signal} dBm"
            )
        else:
            self.isWireless = False
            self.connection = "---------"

    def __init__(self, rosl: dict):
        self.status = rosl.get("status", "unknown")
        info = json.loads(rosl.get("comment", "{}"))
        self.comment = info.get("comment", "no comment")

        if self.status == "bound":
            self.ip = ipaddress.IPv4Address(rosl.get("active-address", "0.0.0.0/0"))
            self.mac = rosl.get("active-mac-address", "00:00:00:00:00:00")
        else:
            self.ip = ipaddress.IPv4Address(rosl.get("address", "0.0.0.0/0"))
            self.mac = rosl.get("mac-address", "00:00:00:00:00:00")

        if rosl.get("dynamic", "false") == "false":
            self.name = info.get("name", "?????")
        else:
            self.name = rosl.get("host-name", "?????")

        self.id = rosl.get("id", "???")
        oui = _lookup_oui_cached(self.mac)
        self.macFmt = list(oui)[0]
        self.oui = oui.get(self.mac, "None")
        if (
            (self.mac[1] in ("2", "6", "A", "E"))
            and self.mac[0:8] != "D0:D0:D0"  # non-Apple, personal prefix
            and self.mac[0:8] != "EE:EC:00"  # non-Apple, personal prefix
            and self.mac[0:8] != "F2:F2:F2"  # non-Apple, personal prefix
            and self.mac[0:8] != "E2:D2:5E"  # non-Apple, random OrangePi
        ):
            self.locallyAdministered = True
            self.oui = "Locally Administered"
        else:
            self.locallyAdministered = False

        self.lastSeen = time_fmt(rosl.get("last-seen", "_never"))
        self.hostname = rosl.get("host-name", "")

        self.dynamic = rosl.get("dynamic", "false") != "false"
        self.net = info.get("net", "g")

        if self.comment:
            self.details = self.comment
        elif self.hostname:
            self.details = self.hostname
        else:
            self.details = self.oui

        self.extraClasses = ""
        if self.dynamic:
            self.extraClasses += " dynamic"
        self.macClass = ""
        if self.locallyAdministered:
            self.macClass += "locallyAdministered"

        self.ip_shared = (
            self.ip.exploded.split(".")[0] + "." + self.ip.exploded.split(".")[1] + "."
        )
        self.ip_unique = (
            self.ip.exploded.split(".")[2] + "." + self.ip.exploded.split(".")[3]
        )

        self.connection = "----"

    def __lt__(self, other):
        return self.ip < other.ip
