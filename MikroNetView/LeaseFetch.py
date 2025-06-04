from LeaseInfo import LeaseInfo
from RegInfo import RegInfo
import routeros_api

# FIXME: this is direct import of prototype, it must be improved
# FIXME: API connection cannot be created on each reload
# FIXME: this must be asynchronous, ideally separating lease and reginfo so it's parsed on front-end
def dumbFetchLeases(host: str, user: str, password: str) -> list[LeaseInfo]:
    connection = routeros_api.RouterOsApiPool(host, username=user, password=password, plaintext_login=True)
    api = connection.get_api()

    reginfos_raw=api.get_resource('/interface/wifi/registration-table').get()
    reginfos=[]
    for reginfo in reginfos_raw:
      try:
        myreginfo=RegInfo(reginfo)
        reginfos.append(myreginfo)
      except Exception as e:
        print(reginfo)
        print(f"Error processing reginfo: {e}")
        continue
      
    leases_raw=api.get_resource('/ip/dhcp-server/lease').get()
    leases=[]
    for lease in leases_raw:
      try:
        mylease=LeaseInfo(lease)
        reginfos_matching=[ri for ri in reginfos if ri.mac == mylease.mac]
        if len(reginfos_matching)==1:
          mylease.addWirelessInfo(reginfos_matching[0])
        else:
          mylease.addWirelessInfo(None)
          
        leases.append(mylease)
          
      except Exception as e:
        print(lease)
        print(f"Error processing lease: {e}")
        raise e
        continue
    leases.sort()
    connection.disconnect()
    return leases