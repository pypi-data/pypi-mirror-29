# noinspection PyPackageRequirements
from sanic.exceptions import NotFound

from ..api import Gino as _Gino, GinoExecutor as _Executor
from ..local import enable_task_local, disable_task_local
from ..connection import GinoConnection as _Connection
from ..pool import GinoPool as _Pool


class SanicModelMixin:
    @classmethod
    async def get_or_404(cls, *args, **kwargs):
        # noinspection PyUnresolvedReferences
        rv = await cls.get(*args, **kwargs)
        if rv is None:
            raise NotFound('{} is not found'.format(cls.__name__))
        return rv


# noinspection PyClassHasNoInit
class GinoExecutor(_Executor):
    async def first_or_404(self, *args, **kwargs):
        rv = await self.first(*args, **kwargs)
        if rv is None:
            raise NotFound('No such data')
        return rv


# noinspection PyClassHasNoInit
class GinoConnection(_Connection):
    async def first_or_404(self, *args, **kwargs):
        rv = await self.first(*args, **kwargs)
        if rv is None:
            raise NotFound('No such data')
        return rv


# noinspection PyClassHasNoInit
class GinoPool(_Pool):
    async def first_or_404(self, *args, **kwargs):
        rv = await self.first(*args, **kwargs)
        if rv is None:
            raise NotFound('No such data')
        return rv


# noinspection PyClassHasNoInit
class Gino(_Gino):
    """Support Sanic web server.

    By :meth:`init_app` GINO registers a few hooks on Sanic, so that GINO could
    use database configuration in Sanic `config` to initialize the bound pool.

    A lazy connection context is enabled by default for every request. You can
    change this default behavior by setting `DB_USE_CONNECTION_FOR_REQUEST`
    config value to `False`. By default, a database connection is borrowed on
    the first query, shared in the same execution context, and returned to the
    pool on response. If you need to release the connection early in the middle
    to do some long-running tasks, you can simply do this:

        await request['connection'].release()

    Here `request['connection']` is a :class:`LazyConnection` object, see its
    doc string for more information.
    """
    model_base_classes = _Gino.model_base_classes + (SanicModelMixin,)
    query_executor = GinoExecutor
    connection_cls = GinoConnection
    pool_cls = GinoPool

    def init_app(self, app):
        task_local_enabled = [False]

        if app.config.setdefault('DB_USE_CONNECTION_FOR_REQUEST', True):
            @app.middleware('request')
            async def on_request(request):
                request['connection_ctx'] = ctx = self.acquire(lazy=True)
                request['connection'] = await ctx.__aenter__()

            @app.middleware('response')
            async def on_response(request, _):
                ctx = request.pop('connection_ctx', None)
                request.pop('connection', None)
                if ctx is not None:
                    await ctx.__aexit__(None, None, None)

        @app.listener('before_server_start')
        async def before_server_start(_, loop):
            if app.config.setdefault('DB_USE_CONNECTION_FOR_REQUEST', True):
                enable_task_local(loop)
                task_local_enabled[0] = True

            await self.create_pool(
                host=app.config.setdefault('DB_HOST', 'localhost'),
                port=app.config.setdefault('DB_PORT', 5432),
                user=app.config.setdefault('DB_USER', 'postgres'),
                password=app.config.setdefault('DB_PASSWORD', ''),
                database=app.config.setdefault('DB_DATABASE', 'postgres'),
                min_size=app.config.setdefault('DB_POOL_MIN_SIZE', 5),
                max_size=app.config.setdefault('DB_POOL_MAX_SIZE', 10),
                loop=loop,
            )

        @app.listener('after_server_stop')
        async def after_server_stop(_, loop):
            await self._bind.close()
            if task_local_enabled[0]:
                disable_task_local(loop)
                task_local_enabled[0] = False

    async def first_or_404(self, *args, **kwargs):
        rv = await self.first(*args, **kwargs)
        if rv is None:
            raise NotFound('No such data')
        return rv
