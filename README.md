# MikroNetView

Simple web-app for monitoring status of MikroTik based network - DHCP, WiFi clients and system stats.

Developed as a replacement for [AiMeshClientMonitor](https://github.com/danielskowronski/AiMeshClientMonitor). 

## Absolute requirements

### Target device

This tool expects RouterOS 7 exposing standard API (see [RouterOS-api](https://pypi.org/project/RouterOS-api/) docs).

### Entry metadata

This tool strictly requires some objects to have comment with JSON-encoded metadata matching [HomeOps](https://github.com/skowronski-cloud/HomeOps).

DHCP server lease **must** have [metadata](https://github.com/skowronski-cloud/HomeOps/blob/master/HomeOpsTerraformRoot/NetClients/leases.tf) with following fields:

- `net` - ID of network (`net` in IP Pool)
- `name` - name of lease
- `comment` - longer description
- *subject to change*

IP Pool *should* have [metadata](https://github.com/skowronski-cloud/HomeOps/blob/master/HomeOpsTerraformRoot/NetCore/dhcp.tf) with following fields:

- `net` - ID of network (matching one from leases)
- `name` - name of lease
- `comment` - longer description
- *subject to change*

## Running

For now, only web-app mode is supported. Either via locally `python3 app.py` or Docker-Compose or via [Docker image](https://github.com/danielskowronski/MikroNetView/pkgs/container/mikronetview) or via [Helm Chart](./charts/MikroNetView/Chart.yaml)

### Configuration - default

Config file pointed by env variable `MNV_CONF` defaulting to `/app/config/config.yaml`:

```yaml
---
server:
  host: "0.0.0.0"
  port: 9001
  debug: true
mikrotik:
  host: "192.168.0.1"
  user: "admin"
  password: "admin"
```

### Configuration - fallback 

Device is targeted by setting following env vars:

```bash
export MNV_HOST='192.168.0.1'
export MNV_USER='admin'
export MNV_PASS='admin'
```
