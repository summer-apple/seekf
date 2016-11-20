from mysqlconn import MySQLHelper


class Order():
    def __init__(self, **kvs):
        self.__dict__.update(kvs)


class OrderService:

    def __init__(self):
        self.mysql = MySQLHelper()

    def get_orders_by_date(self, trans_day):
        return self.mysql.fetchall("select * from t_order where trans_day=%s", [trans_day, ])

    def get_order_by_id(self, order_id):
        return self.mysql.fetchone("select * from t_order where order_id=%s", [order_id, ])

    def create_order(self, args):
        sql = "insert into t_order(trans_day,model,packages,pairs,price,discount,amount) values(%s,%s,%s,%s,%s,%s,%s)"
        self.mysql.execute(sql, args)

    def delete_order_by_id(self,order_id):
        self.mysql.execute("delete from t_order where order_id=%s", [order_id, ])

    def stat_by_model_price(self,trans_day):
        return self.mysql.fetchall("select trans_day,"
                                        "model,"
                                        "sum(packages) as packages,"
                                        "pairs,price,"
                                        "sum(discount) as discount,"
                                        "sum(amount) as amount "
                                 "from t_order "
                                 "where trans_day=%s "
                                 "group by model,price "
                                 "order by model, price", [trans_day,])

    def stat_by_model(self,trans_day):
        return self.mysql.fetchall("select trans_day,"
                                        "model,"
                                        "sum(packages) as packages,"
                                        "pairs,"
                                        "format(sum(amount)/sum(packages)/pairs,2) as price,"
                                        "sum(discount) as discount,"
                                        "sum(amount) as amount "
                                 "from t_order "
                                 "where trans_day=%s "
                                 "group by model "
                                 "order by model", [trans_day,])








