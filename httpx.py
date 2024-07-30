import httpx
import spnego
import socket
import sys

class AsyncHTTPKerberosAuth:
    def __init__(self, principal=None, service='HTTP', hostname_override=None, delegate=False, mutual_authentication=True, cbt_struct=None):
        self.principal = principal
        self.service = service
        self.hostname_override = hostname_override
        self.delegate = delegate
        self.mutual_authentication = mutual_authentication
        self.cbt_struct = cbt_struct
        self._context = {}
        if self.hostname_override is None:
            self.hostname_override = (lambda x: socket.getfqdn(x) if sys.platform == 'win32' else x)

    def _get_kerb_host(self, host):
        if self.hostname_override is not None:
            if callable(self.hostname_override):
                return self.hostname_override(host)
            else:
                return self.hostname_override
        return host

    async def _generate_request_header_spnego(self, host):
        gssflags = spnego.ContextReq.sequence_detect
        if self.delegate:
            gssflags |= spnego.ContextReq.delegate
        if not self.mutual_authentication:
            gssflags |= spnego.ContextReq.mutual_auth

        try:
            kerb_stage = "ctx init"
            kerb_host = self._get_kerb_host(host)
            self._context[host] = ctx = spnego.client(
                username=self.principal,
                hostname=kerb_host,
                service=self.service,
                channel_bindings=self.cbt_struct,
                context_req=gssflags,
                protocol="kerberos",
            )
            return await ctx.step(None)
        except Exception as e:
            raise KerberosExchangeError(f"{kerb_stage} step: {str(e)}")

    async def auth_flow(self, request):
        host = request.url.host
        auth_header = await self._generate_request_header_spnego(host)
        request.headers['Authorization'] = f'Negotiate {auth_header}'
        response = yield request
        return response

# Ejemplo de uso con httpx
async def fetch_url(url):
    auth = AsyncHTTPKerberosAuth()
    async with httpx.AsyncClient(auth=auth) as client:
        response = await client.get(url)
        return response

# Llama a la función fetch_url en un evento de bucle asíncrono
import asyncio
asyncio.run(fetch_url('https://example.com'))
