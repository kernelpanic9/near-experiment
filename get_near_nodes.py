import urllib, requests, json
main_rpc = "https://rpc.mainnet.near.org"

def get_peers(url):
  headers = {'Content-type': 'application/json'}
  res = requests.post(url, json={"jsonrpc":"2.0", "method":"network_info", "id":1}, timeout=2.0)

  data = res.json()

  peers = []
  for p in data["result"]["active_peers"]:
    peers.append(p["addr"].split(":")[0])

  return peers

init_peers = get_peers(main_rpc)
all_peers = list(init_peers)
connected_peers = set()
rpc_peers = set()

for i in range(2):
  disc_peers = []
  for p in all_peers:
    if p in connected_peers:
      continue
    peer_url = "http://"+p+":3030"
    print("Trying", peer_url)
    try:
      new_peers = get_peers(peer_url)
      connected_peers.add(p)
    except:
      continue
    rpc_peers.add(p)
    for p in new_peers:
      if p not in all_peers:
        disc_peers.append(p)
  all_peers.extend(x for x in disc_peers if x not in all_peers)

print("Total number of nodes: %d", len(all_peers))
print("Nodes with RPC enabled: %d", len(rpc_peers))
print(all_peers)


