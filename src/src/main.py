import logging
import asyncio
from argparse import ArgumentParser
from asyncua import ua, Client
from asyncua.common import ua_utils
import opcua_scan as ops
from action import browse_nodes,print_tree



format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=format)

async_logger = logging.getLogger("asyncua")

class param:
    '''
    Class to pass arguments to opcua_scan functions.
    '''
    def __init__(self, args):
        self.targets = args.target 
        self.verbose = False
        self.table_format = 'plain'

        if (args.action == "read" or args.action == "write" or args.action == "server_config"):
            self.root_node = args.node
            self.repeat = args.repeat if hasattr(args, 'repeat') else 1
            self.single = 'aaaa'
            self.output_verbose = False
            if args.action == "server_config":
                self.node_attributes = args.node_attributes if hasattr(args, 'node_attributes') else ["DisplayName", "Description", "Value"]
                self.servers = False
                self.nodes_writable = args.nodes_writable if hasattr(args, 'nodes_writable') else False
                self.nodes_executable = args.nodes_executable if hasattr(args, 'nodes_executable') else False
            if args.action == "write":
                self.data = args.value if hasattr(args, 'value') else False
                self.dtype = ua.VariantType.UInt32
        

        if args.action == "hello":
            self.ip_addresses = args.ip_address
            self.ports = args.port
            self.output = args.output if hasattr(args, 'output') else "hello_output.txt"
            self.name = args.name
            self.timeout = 5.0
            

        ### Authentication parameters
        self.username = args.username if hasattr(args, 'username') else ""
        self.password = args.password if hasattr(args, 'password') else ""
        self.certificate = args.certificate if hasattr(args, 'certificate') else ""
        self.private_key = args.private_key if hasattr(args, 'private_key') else ""
        self.mode = args.mode if hasattr(args, 'mode') else "None"
        self.policy = args.policy if hasattr(args, 'policy') else "None"
        self.authentication = args.authentication if hasattr(args, 'authentication') else ""



if async_logger.isEnabledFor(logging.INFO):
    async_logger.setLevel(logging.WARNING)
    async_logger.addHandler(logging.StreamHandler())
    async_logger.propagate = False
    async_logger.info("AsyncUA logger set to WARNING level.")



def add_read_args(parser):
    '''
    Function to add read options to the argument parser.
    '''
    parser.add_argument(
        "-n", "--node", type=str, required=True, help="Node ID to read from"
    )
    parser.add_argument(
        "-a", "--attribute", type=int, default=13, help="Attribute ID to read (default: 13)"
    )
    parser.add_argument(
        "-r", "--repeat", type=int, default=1, help="Number of times to read the value (default: 1)"
    )
    parser.add_argument(
        "--wait", type=float, default=0.0, help="Wait time between reads in seconds (default: 0.0)"
    )

    

def add_write_parser(parser):
    '''
    Function to add write options to the argument parser.
    '''
    parser.add_argument(
        "-n", "--node", type=str, required=True, help="Node ID to write to"
    )
    parser.add_argument(
        "-v", "--value", type=float, required=True, help="Value to write to the node"
    )

def add_hello_parser(parser):
    '''
    Function to add hello options to the argument parser.
    '''
    parser.add_argument(
        "-ip", "--ip_address", type=str, default="localhost", help="IP address of the server (default: localhost)"
    )
    parser.add_argument(
        "-p", "--port", type=str, default='4840', help="Port of the server (default: 4840)"
    )
    parser.add_argument(
        "-out", "--output", type=str, default="hello_output.txt", help="Output file for hello response (default: hello_output.txt)"
    )
    parser.add_argument(
        "-n", "--name", type=str, default="", help="Name of the server (default: empty)"
    )

def add_server_config_parser(parser):
    '''
    Function to add server configuration options to the argument parser.
    '''
    parser.add_argument(
        "-n", "--node", type=str, default="", help="Root node to start browsing (default: RootFolder)"
    )
    parser.add_argument(
        "-na", "--node_attributes", type=str, nargs='*', default=["DisplayName", "Description", "Value"], 
        help="List of node attributes to retrieve (default: DisplayName, Description, Value)"
    )
    parser.add_argument(
        "-nw", "--nodes_writable", action='store_true', help="Check if nodes are writable"
    )
    parser.add_argument(
        "-ne", "--nodes_executable", action='store_true', help="Check if nodes are executable"
    )
    parser.add_argument(
        "-o", "--output_verbose", action='store_true', help="Enable verbose output for node attributes"
    )

def argparse():
    '''
    Function to parse command line arguments.
    '''
    parser = ArgumentParser(description="OPC UA Client")
    parser.add_argument(
        "-t", "--target", type=str, default="opc.tcp://localhost:4840/freeopcua/server/", help="URL of the OPC UA server"
    )
    parser.add_argument(
        "-n", "--namespace", type=str, default="http://examples.freeopcua.github.io", help="Namespace URI"
    )

    parser.add_argument(
        "-c", "--certificate", type=str, default="", help="Path to the client certificate"
    )
    parser.add_argument(
        "-k", "--private_key", type=str, default="", help="Path to the client private key"
    )
    parser.add_argument(
        "-m", "--mode", type=str, default="None", help="Security mode (None, Sign, SignAndEncrypt)"
    )
    parser.add_argument(
        "-p", "--policy", type=str, default="None", help="Security policy (None, Basic256, Basic256Sha256)"
    )
    parser.add_argument(
        "-a", "--authentication", type=str, default="", help="Authentication method (e.g., username:password)"
    )

    parser.add_argument(
        "-u", "--username", type=str, default="", help="Username for authentication"
    )
    parser.add_argument(
        "-w", "--password", type=str, default="", help="Password for authentication"
    )
    


    ### Action parsers
    subparser = parser.add_subparsers(dest="action",required=True, help="Action to perform")
    read_parser = subparser.add_parser("read", help="Read")
    add_read_args(read_parser)
    write_parser = subparser.add_parser("write", help="Write")
    add_write_parser(write_parser)
    hello_parser = subparser.add_parser("hello", help="Hello")
    add_hello_parser(hello_parser)
    subscribe_parser = subparser.add_parser("server_config", help="Server Configuration")
    add_server_config_parser(subscribe_parser)
    return parser

async def main_sync():
    '''
    Main function to run the OPC UA client synchronously.
    '''
    logging.info("*"*75)
    args = argparse().parse_args()

    if async_logger.isEnabledFor(logging.INFO):
        async_logger.addHandler(logging.StreamHandler())
        async_logger.propagate = False
        async_logger.info("Stopping asyncua logger propagation.")

    if (args.password and not args.username) or (args.username and not args.password):
        logger.error("Both username and password must be provided for authentication.")
        return

    if args.action == "read":
        # Read node information
        obj = param(args)             
        await ops.read_data(obj)
    elif args.action == "write":
        # Write node information
        obj = param(args)
        await ops.write_data(obj)
    elif args.action == "hello":
        obj = param(args)
        await ops.run_hello(obj)
    elif args.action == "server_config":
        obj = param(args)
        if obj.node_attributes:
            if not args.output_verbose:
                ops.pretty_log(
                    "Warning: No output file configured, the additional "
                    "targeted node attributes will not be retrieved",
                    lvl="critical"
                )
            else:
                old_attrs = obj.node_attributes
                obj.node_attributes = [
                    attr for attr in old_attrs if attr in ops.valid_node_attributes
                ]
                for attr in old_attrs:
                    if attr not in obj.node_attributes:
                        ops.pretty_log(
                            f"Warning: The attribute {attr} is not valid and "
                            "thus, ignored.",
                            lvl="critical"
                        )
            if obj.root_node:
            # Converts root_id to int if possible
                try:
                    root_id = int(obj.root_node)
                    obj.root_node = root_id
                except Exception:
                    pass

            await ops.run_server_config(obj)
    else:
        logger.error(f"Unknown action: {args.action}")
        return

if __name__ == "__main__":
    asyncio.run(main_sync())



        
