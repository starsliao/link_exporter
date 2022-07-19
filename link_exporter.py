#!/usr/local/python3.8/bin/python3.8
import json,asyncio,aiohttp
from flask import Response, Flask

node_list = ['main.confluxrpc.com', 'main.confluxrpc.org']
headers = {'Content-Type': 'application/json'}
data = { "jsonrpc": "2.0", "method": "cfx_epochNumber", "params": [], "id": 1 }

async def post(session, node, node_height):
    url = f'https://{node}/'
    try:
        async with session.post(url,headers=headers, data=json.dumps(data)) as resp:
            height = await resp.json()
            result = int(height['result'],16)
    except:
        result = 0
    node_height.append(f'node_height{{node="{node}",id="1",method="cfx_epochNumber",jsonrpc="2.0"}} {result}\n')

async def get_node_height(node_height):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for node in node_list:
            task = asyncio.create_task(post(session, node, node_height))
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
