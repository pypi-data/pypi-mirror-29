# -*- coding: utf-8 -*-

from ..task import Task
from ..maple_pb2 import RspToUsers, CloseUsers
from .client import Client
from .. import constants


class Trigger(object):

    box_class = None
    client = None

    def __init__(self, box_class, host, port, ensure=True):
        self.box_class = box_class
        self.client = Client((host, port), ensure)

    def write_to_worker(self, data, params=None):
        """
        透传到worker进行处理
        :param params 指定task的参数, dict类型
        """

        task = Task()
        task.cmd = constants.CMD_WRITE_TO_WORKER

        if params:
            for k, v in params.items():
                setattr(task, k, v)

        if isinstance(data, self.box_class):
            # 打包
            data = data.pack()
        elif isinstance(data, dict):
            data = self.box_class(data).pack()
            
        task.body = data

        return self._write(task.pack())

    def write_to_users(self, data_list):
        """
        格式为
        [(uids, box), (uids, box, userdata), (uids, box, userdata, exclude) ...]
        :param data_list: userdata可不传，默认为0，conn.userdata & userdata == userdata; exclude 代表排除的uid列表
        :return:
        """

        msg = RspToUsers()

        for data_tuple in data_list:
            if len(data_tuple) == 2:
                uids, data = data_tuple
                userdata = None
                exclude = None
            elif len(data_tuple) == 3:
                uids, data, userdata = data_tuple
                exclude = None
            else:
                uids, data, userdata, exclude = data_tuple

            if isinstance(data, self.box_class):
                data = data.pack()
            elif isinstance(data, dict):
                data = self.box_class(data).pack()

            row = msg.rows.add()
            row.buf = data
            row.userdata = userdata or 0
            row.uids.extend(uids)
            if exclude:
                row.exclude.extend(exclude)

        task = Task()
        task.cmd = constants.CMD_WRITE_TO_USERS
        task.body = msg.SerializeToString()

        return self._write(task.pack())

    def close_users(self, uids, userdata=None, exclude=None):
        msg = CloseUsers()
        msg.uids.extend(uids)
        msg.userdata = userdata or 0
        if exclude:
            msg.exclude.extend(exclude)

        task = Task()
        task.cmd = constants.CMD_CLOSE_USERS
        task.body = msg.SerializeToString()

        return self._write(task.pack())

    def _write(self, data):
        return self.client.write(data)

    def __repr__(self):
        return '<%s address: %s>' % (
            type(self).__name__, self.client.address
        )
