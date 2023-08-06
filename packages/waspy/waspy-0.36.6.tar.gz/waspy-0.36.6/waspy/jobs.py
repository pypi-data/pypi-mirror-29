import asyncio


class Job:
    def __init__(self, f):
        if callable(f):
            self._f = f
        else:
            self._f = None

    def __repr__(self):
        print(f'{self}')

    async def __call__(self, *args, **kwargs):
        return await self._f(*args, **kwargs)

    def run_task(self, *args, **kwargs):
        if asyncio.iscoroutinefunction(self._f):
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self._f(*args, **kwargs))
        else:
            return self._f(*args, **kwargs)


@Job
def some_func(a, b):
    pass


if __name__ == '__main__':
    print(some_func)
