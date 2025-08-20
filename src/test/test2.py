# my_opc_script.py
import asyncio
from asyncua import Client

namespace = "http://examples.freeopcua.github.io"

async def read_node():
    url = "opc.tcp://127.0.0.1:4840"
    print("Connecting to OPC UA server at", url)
    async with Client(url) as client:
        nsidx = await client.get_namespace_index(namespace)
        print(f"Namespace Index for '{namespace}': {nsidx}")
        # Get the variable node for read / write
        var = await client.nodes.root.get_child(f"0:Objects/{nsidx}:MyObject/{nsidx}:MyVariable")
        value = await var.read_value()
        print(f"Value of MyVariable ({var}): {value}")

if __name__ == "__main__":
    asyncio.run(read_node())
