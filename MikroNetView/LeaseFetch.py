from LeaseInfo import LeaseInfo, LeaseInfoProps
from RegInfo import RegInfo, RegInfoProps
import routeros_api
import time

_connection = None
def getApi(host: str, user: str, password: str):
    global _connection
    if _connection is None:
        print(f"Creating new API connection to {host} as {user}")
        _connection = routeros_api.RouterOsApiPool(host, username=user, password=password, plaintext_login=True)
    return _connection.get_api()



# FIXME: this is direct import of prototype, it must be improved
# FIXME: split leases fetching into bound (only those can be matched with reginfos) and unbound
# FIXME: verify if we can call both endpoints in parallel (with above - 3 calls at the same time)
# TODO: this could be asynchronous, ideally separating lease and reginfo so it's parsed on front-end
def dumbFetchLeases(host: str, user: str, password: str) -> list[LeaseInfo]:
    api = getApi(host, user, password)

    start_time = time.time()
    reginfos_raw=api.get_resource('/interface/wifi/registration-table').call('print', {'.proplist': RegInfoProps})
    end_time = time.time()
    print(f"Fetched {len(reginfos_raw)} registration infos in {end_time - start_time:.3f} seconds")
    reginfos=[]
    for reginfo in reginfos_raw:
      try:
        myreginfo=RegInfo(reginfo)
        reginfos.append(myreginfo)
      except Exception as e:
        print(reginfo)
        print(f"Error processing reginfo: {e}")
        continue
      
    start_time = time.time()
    leases_raw=api.get_resource('/ip/dhcp-server/lease').call('print', {'.proplist': LeaseInfoProps})
    end_time = time.time()
    print(f"Feteched {len(leases_raw)} leases in {end_time - start_time:.3f} seconds")
    leases=[]
    start_time = time.time()
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
    end_time = time.time()
    print(f"Processed {len(leases)} leases in {end_time - start_time:.3f} seconds")
    
    leases.sort()
    return leases