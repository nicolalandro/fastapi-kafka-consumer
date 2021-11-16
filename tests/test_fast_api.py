from fastapi.testclient import TestClient
import mock
import json
import asyncio

try:
    import main
except:
    import sys

    sys.path.insert(0, './')

import main


def test_setup():
    main._state = 0
    data = json.dumps({'message_id': 0, 'text': 'some text', 'state': 10})
    message = type('test', (object,), {})()
    message.value = data
    class FakeConsumer:
        def __init__(self, x,loop,bootstrap_servers,group_id):
            self.iter_status = 0
        
        async def start(self):
            pass

        async def stop(self):
            pass
    
        def __aiter__(self):
            return self
        
        async def __anext__(self):
            #await asyncio.sleep(0)
            if self.iter_status == 0:
                self.iter_status += 1
                return message
            else:
                raise StopAsyncIteration
    
    with mock.patch('aiokafka.AIOKafkaConsumer', FakeConsumer):
        with TestClient(main.app) as client:
            response = client.get('/state')
            assert response.status_code == 200
            assert response.json() == {"state": 10}


    assert main._state == 10
