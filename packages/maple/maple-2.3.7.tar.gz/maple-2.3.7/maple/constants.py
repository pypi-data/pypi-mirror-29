# -*- coding: utf-8 -*-

NAME = 'maple'

# 系统返回码
RET_INVALID_CMD = -10000
RET_INTERNAL = -10001

# 命令字
CMD_CLIENT_REQ              = 10  # 透传client请求
CMD_CLIENT_CREATED          = 15  # 客户端连接建立
CMD_CLIENT_CLOSED           = 20  # 客户端连接被关闭

CMD_WRITE_TO_WORKER         = 100 # trigger触发请求

CMD_WORKER_ASK_FOR_TASK     = 210 # 请求任务

CMD_WRITE_TO_CLIENT         = 220 # 回应
CMD_WRITE_TO_USERS          = 230 # 主动下发
CMD_CLOSE_CLIENT            = 240 # 关闭客户端(client_id为判断)
CMD_CLOSE_USERS             = 250 # 关闭多个客户端
CMD_LOGIN_CLIENT            = 260 # 登录用户
CMD_LOGOUT_CLIENT           = 270 # 登出用户
CMD_CLEAR_CLIENT_TASKS      = 280 # 清空客户端对应的所有任务


# 重连等待时间
TRY_CONNECT_INTERVAL = 1

# worker的env
WORKER_ENV_KEY = 'MAPLE_WORKER'

# 网络连接超时(秒)，包括 connect once，read once，write once
CONN_TIMEOUT = 3

# write_to_users / close_users 时的特殊连接集合
CONNS_AUTHED                = -1 # 所有已登录连接
CONNS_ALL                   = -2 # 所有连接
CONNS_UNAUTHED              = -3 # 所有未登录连接
