import importlib
import typing


class HandleOutputIntegrations():
    @staticmethod
    def send_event(uuid: str, events: typing.Dict):
        for integrate in events:
            try:
                module = importlib.import_module(f'integration.{integrate}')
                handler = module.Handler(uuid)
                
                for event in events[integrate]:
                    handler.send_event(event)

            except BaseException:
                pass