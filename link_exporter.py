import json,asyncio,aiohttp
from flask import Response, Flask

host_info = {"https://main.confluxrpc.com":"cfx_epochNumber",
             "https://main.confluxrpc.org":"cfx_epochNumber",
             "https://eth-mainnet.g.alchemy.com/v2/cmlKon8xAj75Cv7s9nObf4BsnoVDTTmX":"eth_blockNumber"
            }

headers = {'Content-Type': 'application/json'}


async def post(session, url, method, node_height):
    data = { "jsonrpc": "2.0", "method": method, "params": [], "id": 1 }
    try:
        async with session.post(url,headers=headers, data=json.dumps(data)) as resp:
            height = await resp.json()
            result = int(height['result'],16)
    except:
        result = 0
    node_height.append(f'node_height{{node="{url}",id="1",method="{method}",jsonrpc="2.0"}} {result}\n')

async def get_node_height(node_height):
    timeout = aiohttp.ClientTimeout(total=7)
    conn = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(timeout=timeout, connector=conn) as session:
        tasks = []
        for url,method in host_info.items():
            task = asyncio.create_task(post(session, url, method, node_height))
            tasks.append(task)
        for task in tasks:
            await task

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route("/metrics")
def metrics():
    node_height = ["# HELP node_height 节点高度\n","# TYPE node_height gauge\n"]
    asyncio.run(get_node_height(node_height))
    return Response(''.join(node_height).encode('utf-8'),mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9926)
