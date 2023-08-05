import asyncio
from unittest import mock

from aioredis.commands import MultiExec
from aioredis.commands import Redis


def test_global_loop():
    conn = mock.Mock(spec=(
        'execute closed _transaction_error'
        .split()))
    try:
        old_loop = asyncio.get_event_loop()
    except (AssertionError, RuntimeError):
        old_loop = None
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    tr = MultiExec(conn, commands_factory=Redis)
    assert tr._loop is loop

    def make_fut(cmd, *args, **kw):
        fut = asyncio.get_event_loop().create_future()
        if cmd == 'PING':
            fut.set_result(b'QUEUED')
        elif cmd == 'EXEC':
            fut.set_result([b'PONG'])
        else:
            fut.set_result(b'OK')
        return fut

    conn.execute.side_effect = make_fut
    conn.closed = False
    conn._transaction_error = None

    async def go():
        tr.ping()
        res = await tr.execute()
        assert res == [b'PONG']
    loop.run_until_complete(go())
    asyncio.set_event_loop(old_loop)
