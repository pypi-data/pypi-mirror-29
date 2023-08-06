# -*- coding: utf-8 -*-

import os
import socket
import thread
from netkit.contrib.tcp_client import TcpClient
from ..task import Task
import time
from .. import constants
from ..log import logger


class Connection(object):

    work_progress = None

    def __init__(self, app, address, conn_timeout):
        self.app = app
        # 直接创建即可
        self.client = TcpClient(Task, address=address, timeout=conn_timeout)
        # TCP_NODELAY 打开，确保消息即时发出
        self.client.tcp_nodelay = True

    def run(self):
        thread.start_new_thread(self._monitor_work_timeout, ())
        while self.app.enable:
            try:
                self._handle()
            except KeyboardInterrupt:
                break
            except:
                logger.error('exc occur. app: %s', self.app, exc_info=True)

    def _monitor_work_timeout(self):
        """
        监控work超时
        :return:
        """

        while self.app.enable:
            time.sleep(1)

            work_progress = self.work_progress
            if work_progress:
                past_time = time.time() - work_progress['begin_time']
                if self.app.work_timeout is not None and past_time > self.app.work_timeout:
                    # 说明worker的处理时间已经太长了
                    logger.error('work timeout: %s / %s, request: %s',
                                 past_time, self.app.work_timeout, work_progress['request'])
                    # 强制从子线程退出worker
                    os._exit(-1)

    def _handle(self):
        while self.app.enable and self.closed():
            if not self._connect():
                logger.error('connect fail. app: %s, address: %s, sleep %ss',
                             self.app, self.client.address, constants.TRY_CONNECT_INTERVAL)
                time.sleep(constants.TRY_CONNECT_INTERVAL)

        if not self.app.enable:
            # 安全退出
            return

        # 跟gateway要task
        self._ask_for_task()
        self._read_message()

    def _ask_for_task(self):
        task = Task()
        task.cmd = constants.CMD_WORKER_ASK_FOR_TASK

        return self.write(task.pack())

    def _connect(self):
        try:
            self.client.connect()
        except KeyboardInterrupt, e:
            raise e
        except:
            return False
        else:
            self.app.events.create_conn(self)
            for bp in self.app.blueprints:
                bp.events.create_app_conn(self)

            return True

    def write(self, data):
        """
        发送数据    True: 成功   else: 失败
        """
        if self.client.closed():
            logger.error('connection closed. app: %s, data: %r', self.app, data)
            return False

        # 只支持字符串
        self.app.events.before_response(self, data)
        for bp in self.app.blueprints:
            bp.events.before_app_response(self, data)

        ret = self.client.write(data)
        if not ret:
            logger.error('connection write fail. app: %s, data: %r', self.app, data)

        for bp in self.app.blueprints:
            bp.events.after_app_response(self, data, ret)
        self.app.events.after_response(self, data, ret)

        return ret

    def _read_message(self):
        req_task = None

        while 1:
            try:
                # 读取数据 task
                req_task = self.client.read()
            except socket.timeout:
                # 超时了
                if not self.app.enable:
                    return
                else:
                    # 继续读
                    continue
            else:
                # 正常收到数据了
                break

        if req_task:
            self._on_read_complete(req_task)

        if self.closed():
            self._on_connection_close()

    def _on_connection_close(self):
        # 链接被关闭的回调

        logger.error('connection closed. app: %s, address: %s', self.app, self.client.address)

        for bp in self.app.blueprints:
            bp.events.close_app_conn(self)
        self.app.events.close_conn(self)

    def _on_read_complete(self, data):
        """
        数据获取结束
        """
        request = self.app.request_class(self, data)

        # 设置task开始处理的时间和信息
        self.work_progress = dict(
            begin_time=time.time(),
            request=request,
        )
        self._handle_request(request)
        self.work_progress = None

    def _handle_request(self, request):
        """
        出现任何异常的时候，服务器不再主动关闭连接
        """

        if not request.is_valid:
            return False

        if request.task.cmd == constants.CMD_CLIENT_CREATED:
            self.app.events.create_client(request)
            for bp in self.app.blueprints:
                bp.events.create_app_client(request)
            return True
        elif request.task.cmd == constants.CMD_CLIENT_CLOSED:
            self.app.events.close_client(request)
            for bp in self.app.blueprints:
                bp.events.close_app_client(request)
            return True

        if not request.view_func:
            logger.info('cmd invalid. request: %s' % request)
            if not request.responded:
                request.write_to_client(dict(ret=constants.RET_INVALID_CMD))
            return False

        if not self.app.got_first_request:
            self.app.got_first_request = True
            self.app.events.before_first_request(request)
            for bp in self.app.blueprints:
                bp.events.before_app_first_request(request)

        self.app.events.before_request(request)
        for bp in self.app.blueprints:
            bp.events.before_app_request(request)
        if request.blueprint:
            request.blueprint.events.before_request(request)

        if request.interrupted:
            # 业务要求中断
            return True

        view_func_exc = None

        try:
            request.view_func(request)
        except Exception, e:
            logger.error('view_func raise exception. e: %s, request: %s',
                         e, request, exc_info=True)
            view_func_exc = e
            # 必须是没有回应过
            if not request.responded:
                request.write_to_client(dict(ret=constants.RET_INTERNAL))

        if request.blueprint:
            request.blueprint.events.after_request(request, view_func_exc)
        for bp in self.app.blueprints:
            bp.events.after_app_request(request, view_func_exc)
        self.app.events.after_request(request, view_func_exc)

        return True

    def close(self):
        """
        直接关闭连接
        """
        self.client.close()

    def closed(self):
        """
        连接是否已经关闭
        :return:
        """
        return self.client.closed()

