# -*- coding:utf-8 -*-
"""
常量类
@author: baostock.com
@group : baostock.com
@contact: baostock@163.com
"""
# 版本信息
BAOSTOCK_CLIENT_VERSION = "00.6.10"
BAOSTOCK_AUTHOR = "baostock.com"
BAOSTOCK_SERVER_IP = "www.baostock.com"  # localhost  www.baostock.com
BAOSTOCK_SERVER_PORT = 10030


BAOSTOCK_PER_PAGE_COUNT = 10000  # 默认每页查询条数


MESSAGE_SPLIT = "\1"  # 消息内部的分隔符

DELIMITER = "\n"  # 分隔符号,消息与消息之间的分隔符

# 参数各属性间的分隔符，如queryHistoryKData中的fields
ATTRIBUTE_SPLIT = ","
# 消息头中，消息体长度，占的位数
MESSAGE_HEADER_BODYLENGTH = 10
# message头长度
MESSAGE_HEADER_LENGTH = 21

# 以下为消息请求类型

MESSAGE_TYPE_LOGIN_REQUEST = "00"  # 登陆请求
MESSAGE_TYPE_LOGIN_RESPONSE = "01"  # 登陆响应
MESSAGE_TYPE_LOGOUT_REQUEST = "02"  # 登出请求
MESSAGE_TYPE_LOGOUT_RESPONSE = "03"  # 登出响应
MESSAGE_TYPE_EXCEPTIONS = "04"  # 错误信息
MESSAGE_TYPE_GETKDATA_REQUEST = "11"  # 获取历史K线数据请求
MESSAGE_TYPE_GETKDATA_RESPONSE = "12"  # 获取历史K线数据响应
MESSAGE_TYPE_QUERYDIVIDENDDATA_REQUEST = "13"  # 估值指标（季频）,股息分红 请求
MESSAGE_TYPE_QUERYDIVIDENDDATA_RESPONSE = "14"  # 估值指标（季频）,股息分红 响应

# 以上为消息请求类型


# 方法名及包名的对应关系
MESSAGE_PACKAGE_MAPPING = {
    "__query_history_k_data_page": "baostock.security.history"

}

# 以下是错误代码
# 正确返回值
BSERR_SUCCESS = "0"

# 用户未登陆
BSERR_NO_LOGIN = "10001001"

# 用户名或密码错误
BSERR_USERNAMEORPASSWORD_ERR = "10001002"

# 获取用户信息失败
BSERR_GETUSERINFO_FAIL = "10001003"

# 客户端版本号过期
BSERR_CLIENT_VESION_EXPIRE = "10001004"

# 账号登陆数达到上限
BSERR_LOGIN_COUNT_LIMIT = "10001005"

# 用户权限不足
BSERR_ACCESS_INSUFFICIENCE = "10001006"

# 需要登录激活
BSERR_NEED_ACTIVATE = "10001007"


BSERR_USERNAME_EMPTY = "10001008"  # 用户名为空


BSERR_PASSWORD_EMPTY = "10001009"  # 密码为空


BSERR_LOGOUT_FAIL = "10001010"  # 用户登出失败

# 用户未登录
ESERR_NOT_LOGIN = "10001011"


# 网络错误
BSERR_SOCKET_ERR = "10002001"

# 网络连接失败
BSERR_CONNECT_FAIL = "10002002"

# 网络连接超时
BSERR_CONNECT_TIMEOUT = "10002003"

# 网络接收时连接断开
BSERR_RECVCONNECTION_CLOSED = "10002004"

# 网络发送失败
BSERR_SENDSOCK_FAIL = "10002005"

# 网络发送超时
BSERR_SENDSOCK_TIMEOUT = "10002006"

# 网络接收错误
BSERR_RECVSOCK_FAIL = "10002007"

# 网络接收超时
BSERR_RECVSOCK_TIMEOUT = "10002008"

# 解析数据错误
BSERR_PARSE_DATA_ERR = "10004001"

# gzip 解压失败
BSERR_UNGZIP_DATA_FAIL = "10004002"

# 客户端未知错误
BSERR_UNKNOWN_ERR = "10004003"

# 数组越界
BSERR_OUTOF_BOUNDS = "10004004"

# 传入参数为空
BSERR_INPARAM_EMPTY = "10004005"

# 参数错误
BSERR_PARAM_ERR = "10004006"

# 起始日期格式不正确
BSERR_START_DATE_ERR = "10004007"


BSERR_END_DATE_ERR = "10004008"  # 截止日期格式不正确


BSERR_START_BIGTHAN_END = "10004009"  # 起始日期大于终止日期


BSERR_DATE_ERR = "10004010"  # 日期格式不正确

BSERR_CODE_INVALIED = "10004011"  # 无效的证券代码

BSERR_INDICATOR_INVALIED = "10004012"  # 无效的指标

# 超出日期支持范围
BSERR_BEYOND_DATE_SUPPORT = "10004013"

# 不支持的混合证券品种
BSERR_MIXED_CODES_MARKET = "10004014"

# 不支持的证券代码品种
BSERR_NO_SUPPORT_CODES_MARKET = "10004015"

# 交易条数超过上限
BSERR_ORDER_TO_UPPER_LIMIT = "10004016"

# 不支持的交易信息
BSERR_NO_SUPPORT_ORDERINFO = "10004017"

# 指标重复
BSERR_INDICATOR_REPEAT = "10004018"

# 消息格式不正确
BSERR_MESSAGE_ERROR = "10004019"

# 错误的消息类型
BSERR_MESSAGE_CODE_ERROR = "10004020"

# 系统级别错误
BSERR_SYSTEM_ERROR = "10005001"

# 以上是错误代码


# 客户端参数错误
CLIENT_ERROR_PARAM = "参数错误，请检查。"
