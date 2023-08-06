# -*- coding: utf-8 -*-
"""
专门给异步使用的Request封装了很多函数，可以和正常的request一样使用
"""

from .. import constants


class VirtualRequest(object):

    trigger = None

    task = None
    box = None

    def __init__(self, task, trigger):
        self.task = task
        self.trigger = trigger

        # 只有write_to_client，且只传入dict时需要用到self.box
        if task.body:
            box = self.trigger.box_class()
            box.unpack(task.body)
            self.box = box

    def write_to_client(self, data):
        if isinstance(data, self.trigger.box_class):
            data = data.pack()
        elif isinstance(data, dict):
            data = self.box.map(data).pack()

        task = self.task.map(dict(
            cmd=constants.CMD_WRITE_TO_CLIENT,
            body=data,
        ))

        return self.trigger._write(task.pack())

    def login_client(self, uid, userdata=None):
        task = self.task.map(dict(
            cmd=constants.CMD_LOGIN_CLIENT,
            uid=uid,
            userdata=userdata or 0,
        ))

        return self.trigger._write(task.pack())

    def logout_client(self):
        task = self.task.map(dict(
            cmd=constants.CMD_LOGOUT_CLIENT,
        ))

        return self.trigger._write(task.pack())

    def close_client(self):
        task = self.task.map(dict(
            cmd=constants.CMD_CLOSE_CLIENT,
        ))

        return self.trigger._write(task.pack())

    def write_to_users(self, *args, **kwargs):
        return self.trigger.write_to_users(*args, **kwargs)

    def write_to_worker(self, *args, **kwargs):
        return self.trigger.write_to_worker(*args, **kwargs)

    def close_users(self, *args, **kwargs):
        return self.trigger.close_users(*args, **kwargs)

    def clear_client_tasks(self):
        task = self.task.map(dict(
            cmd=constants.CMD_CLEAR_CLIENT_TASKS,
        ))

        return self.trigger._write(task.pack())
