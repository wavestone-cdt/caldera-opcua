import asyncio
import logging

from asyncua import Server, ua
import asyncua.crypto.permission_rules as Perm 

class UserManager:
    def get_user(self, iserver, username=None, password=None, certificate=None):
        if username == "foobar" and password == "hR&yjjGhP$6@nQ4e":
            return Perm.User(role=Perm.UserRole.User)
        return None





async def main():
    _logger = logging.getLogger(__name__)
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4841/freeopcua/server/")
    

    # set up our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    server.user_manager = UserManager()
    server.set_security_policy([
        ua.SecurityPolicyType.NoSecurity,
    ])
    server.set_security_IDs(["Username"])

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    myobj = await server.nodes.objects.add_object(idx, "MyObject")
    myvar = await myobj.add_variable(idx, "MyVariable", 6.7)
    # Set MyVariable to be writable by clients
    await myvar.set_writable()
    
    _logger.info("Starting server!")
    async with server:
        while True:
            try:
                myvar_value = await myvar.get_value()
                _logger.info("MyVariable value is: %s", myvar_value)
                myvar_value += 1
                await myvar.set_value(ua.Variant(myvar_value, ua.VariantType.Double))
                _logger.info("MyVariable value set to: %s", myvar_value)
                # wait for a second before next update
                await asyncio.sleep(1)
            except KeyboardInterrupt:
                _logger.info("Server stopped by user")
                await server.stop()




if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)