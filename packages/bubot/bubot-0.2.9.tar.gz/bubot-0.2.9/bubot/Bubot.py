import os
import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_session import SimpleCookieStorage
from aiohttp_session import get_session, session_middleware

from bubot import BujectHelper
from bubot.Action import Action
from bubot.Buject import Buject, CloseBuject
from bubot.BujectError import UserError
from bubot.Ui import Ui
from bubot.Worker import Worker, WorkerQueue, BasicWorker


class Bubot(BasicWorker):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config_path = ''
        self.app = None
        self.app_handler = None
        self.server = None
        self.type = 'bubot'
        self.worker = []
        self.queue = {}

    def init(self):
        super().init()
        self.id = self.get_param('id')
        self.bubot = self.config['param']

    def run(self, file_name=None):
        res = Action('Bubot.run')
        self.config_path = file_name
        app = web.Application(middlewares=[session_middleware(SimpleCookieStorage()), self.authorize])
        app['bubot'] = self
        res.add_stat(self._init_config(app))
        res.add_stat(self.import_ui_handlers(app))
        port = self.get_param('web_port')

        app.on_startup.append(self.start_background_tasks)
        app.on_cleanup.append(self.cleanup_background_tasks)
        web.run_app(app, port=port)
        pass

    @staticmethod
    async def start_background_tasks(app):
        bubot = app['bubot']
        bubot.loop = app.loop
        await bubot.get_broker()
        app['broker'] = app.loop.create_task(bubot.broker.handler_msg())
        app['main'] = app.loop.create_task(bubot.main())

    @staticmethod
    async def cleanup_background_tasks(app):
        if not app['main'].done():
            app['main'].cancel()
            await app['main']
        if not app['broker'].done():
            app['broker'].cancel()
            await app['broker']
        pass

    @staticmethod
    def _init_config(app):
        self = app['bubot']
        # self.config_path = file_name
        res = Action("Bubot._read_bubot_config")
        user_config = BujectHelper.read_config(self.config_path) if self.config_path else {}
        def_config = BujectHelper.read_config(BujectHelper.get_path_default_config('bubot'))
        cache = {}
        self.config, cache = BujectHelper.update_config('bubot', 'Bubot', def_config, user_config, cache)
        for elem in self.config['buject']:
            try:
                buject_name = self.config['buject'][elem]['param']['buject']['value']
                self.config['buject'][elem], cache = BujectHelper.load_config('buject', cache, buject_name,
                                                                              self.config['buject'][elem])
            except KeyError:
                print('buject \'{0}\' - not defined base buject'.format(elem))
                continue

        for elem in self.config['ui']:
            self.config['ui'][elem], cache = BujectHelper.load_config('ui', cache, elem, self.config['ui'][elem])
        # self.config['worker'], cache = BubotConfig.load_config('Worker')

        self.config = BujectHelper.config_to_simple_dict(self.config)
        self.init()
        res.set_end()
        return res

    async def on_init(self):
        await super().on_init()
        res = Action('Bubot.on_init')
        res.add_stat(await self._init_bujects())
        res.add_stat(await self._init_workers())
        return res.set_end()
        pass

    async def on_ready(self):
        await Buject.on_ready(self)
        await self._run_bujects_in_worker(0)

    async def on_error(self):
        print(self.get_param('buject_status_detail'))
        raise CloseBuject(self.get_param('buject_status_detail'))

    @staticmethod
    def import_ui_handlers(app):
        res = Action("WebServer.import_ui_handlers")
        try:
            ui = BujectHelper.get_available_ui()
            ui = BujectHelper.config_to_simple_dict(ui)
        except Exception as e:
            print('Error BubotConfig.get_available_ui(): ', str(e))
            return res.set_end(False)
        try:
            app.router.add_static("/static", "./static")
        except ValueError as e:
            print('No static resources: ', str(e))
        # self.app.router.add_route('*', "/login", Login, name='login')
        template_loaders = {}
        for elem in ui:
            try:
                if os.path.isfile('./ui/{0}/{0}.py'.format(elem)):
                    ui_view = BujectHelper.get_class('ui.{0}.{0}.{0}'.format(elem))
                else:
                    ui_view = Ui
                ui_base_url = '/ui/{0}'.format(elem)
                ui_view.add_route(app, elem, ui_view)
                template_loaders[elem] = jinja2.FileSystemLoader('.' + ui_base_url)
                # template_path.append('.' + ui_base_url)
            except Exception as e:
                # raise RuntimeError('import_ui_handlers({1}): {0}'.format(e, elem))
                print('Error import_ui_handlers({1}): {0}'.format(e, elem))

        aiohttp_jinja2.setup(app, loader=jinja2.PrefixLoader(template_loaders),
                             block_start_string='<%',
                             block_end_string='%>',
                             variable_start_string='%%',
                             variable_end_string='%%'
                             # comment_start_string='<#',
                             # comment_end_string='#>'
                             )
        app['ui'] = ui
        return res.set_end()

    async def _init_workers(self):
        res = Action("Bubot._init_workers")
        count_worker = self.get_param('count_workers')
        if count_worker > 0:
            for i in range(count_worker):
                res.add_stat(self.action_add_worker({}))

        if self.config['queue']:
            for queue_id in self.config['queue']:
                for i in range(self.config['queue'][queue_id]):
                    res.add_stat(self.action_add_queue_worker({"queue": queue_id}))

        return res.set_end()

    def action_add_worker(self, data):
        res = Action('Bubot.action_add_worker')
        last_worker = len(self.worker)
        if last_worker:
            worker_id = self.worker[last_worker - 1].id + 1
        else:
            worker_id = 1
        # worker_config = self.broker.get_worker_param(data['worker_id'])
        worker = Worker(worker_id, bubot=self.bubot)
        worker.daemon = True
        worker.start()
        self.worker.append(worker)
        return res.set_end()

    def action_add_queue_worker(self, data):
        res = Action('Bubot.action_add_worker')
        queue = data['queue']
        if queue not in self.queue:
            self.queue[queue] = []
        last_worker = len(self.queue[queue])
        if last_worker:
            worker_id = self.queue[queue][last_worker - 1].id + 1
        else:
            worker_id = 1

        worker = WorkerQueue(worker_id, queue, bubot=self.bubot)
        worker.daemon = True
        worker.start()
        self.queue[queue].append(worker)
        return res.set_end()

    async def _init_bujects(self):
        res = Action("Bubot._init_bujects")
        for buject_id in self.config['buject']:
            res.add_stat(await self.action_add_buject(buject_id, self.config['buject'][buject_id]))
        return res.set_end()

    async def action_add_buject(self, buject_id, buject_config):
        res = Action("Bubot.action_add_buject")
        await self.broker.write_buject_config('buject_{0}'.format(buject_id), buject_config)
        return res.set_end()

    async def on_event_worker_ready(self, data):
        res = Action("Bubot.action_worker_on_ready")
        # передаем воркеру плагины для запуска
        worker_id = data['worker_id']
        res.add_stat(await self._run_bujects_in_worker(worker_id))
        return res.set_end()

    async def _run_bujects_in_worker(self, worker_id):
        res = Action("Bubot.action_worker_on_ready")
        run_buject = 0
        for buject_id in self.config['buject']:
            try:
                buject_worker_id = self.config['buject'][buject_id]['param']['worker_id']
            except KeyError:
                continue
            if buject_worker_id == worker_id:
                await self.action_run_buject_in_worker({'worker_id': worker_id, 'buject_id': buject_id})
                run_buject += 1
        return res.set_end(run_buject)

    async def action_run_buject_in_worker(self, data):
        res = Action("Bubot.action_run_buject_in_worker")
        try:
            worker_id = data['worker_id']
            buject_id = data['buject_id']
        except KeyError as e:
            raise UserError('Not defined action parameter', str(e))

        worker_uuid = 'worker_{0}'.format(worker_id)
        msg = self.broker.msg_class(
            receiver=worker_uuid,
            sender=self.get_uuid(),
            topic="run_buject",
            data={
                'buject_id': buject_id,
                'config': self.config['buject'][buject_id]
            }
        )
        await self.broker.send_msg(msg)
        return res.set_end()

    @staticmethod
    async def authorize(app, handler):
        async def middleware(request):
            session = await get_session(request)
            if session.get("user"):
                return await handler(request)
            else:
                # auth = 0
                try:
                    if issubclass(handler, Ui) and handler.need_auth(request):
                        raise web.HTTPFound("{0}?redirect={1}".format(app['bubot'].get_param('login_url'), request.path))
                        # auth = request.app['ui'][re.findall('^/ui/(.*)/', request.path)[0]]['param']['auth']
                finally:
                    pass
                    # if auth:
                    # url = request.app.router['login'].url()

            return await handler(request)

        return middleware
