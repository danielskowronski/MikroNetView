from dataclasses import dataclass

RegInfoProps = "id,mac-address,interface,ssid,uptime,lastActivity,signal,band,rx-rate,tx-rate,rx-bits-per-second,tx-bits-per-second"


# FIXME: this is direct import of prototype, it must be improved
@dataclass
class RegInfo:
    id: str
    mac: str
    interface: str
    ssid: str
    uptime: str
    lastActivity: str
    signal: int
    band: str
    rxRate: int
    txRate: int
    rxBps: int
    txBps: int

    def __init__(self, rosr: dict):
        self.id = rosr.get("id", "???")
        self.mac = rosr.get("mac-address", "00:00:00:00:00:00")
        self.interface = rosr.get("interface", "???")
        self.ssid = rosr.get("ssid", "???")
        self.uptime = rosr.get("uptime", "???")
        self.lastActivity = rosr.get("lastActivity", "???")
        self.signal = int(rosr.get("signal", 0))
        self.band = rosr.get("band", "???")
        self.rxRate = int(rosr.get("rx-rate", 0))
        self.txRate = int(rosr.get("tx-rate", 0))
        self.rxBps = int(rosr.get("rx-bits-per-second", 0))
        self.txBps = int(rosr.get("tx-bits-per-second", 0))

    def getBandInfo(self):
        return self.band[0] + (self.band[5:].ljust(1))
