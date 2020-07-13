"""
工具包
"""
import pymongo


def connect_mongodb(myquery):
    """
    连接芒果数据库,并根据查询条件进行查询
    :param myquery:查询条件
    :return:返回查询结果
    """
    myclient = pymongo.MongoClient("mongodb://localhost:27017")
    mydb = myclient["admin"]
    test = mydb["test"]
    result = test.find(myquery)
    return result[0]


if __name__ == '__main__':
    print(connect_mongodb({"username": "liqiang@qq.com","password":"12345"}))