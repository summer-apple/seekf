import pymysql


class MySQLHelper:
    config = {'host': 'localhost',
              'user': 'root',
              'password': '',
              'port': 3306,
              'database': 'seekf'
              }

    cnn = pymysql.connect(**config)
    cur = cnn.cursor(pymysql.cursors.DictCursor)

    def execute(self, sql, args=[]):
        self.cur.execute(sql, args)
        self.cnn.commit()

    def executemany(self, sql, args=[]):
        self.cur.executemany(sql, args)
        self.cnn.commit()

    def fetchone(self, sql, args=[]):
        self.cur.execute(sql, args)
        return self.cur.fetchone()

    def fetchmany(self, sql, args=[], size=None):
        self.cur.execute(sql, args)
        return self.cur.fetchmany(size)

    def fetchall(self, sql, args=[]):
        self.cur.execute(sql, args)
        return self.cur.fetchall()

        # def batch_operate(self, sql, rdd, once_size=1000):
        #     '''
        #     批量数据库操作
        #     :param sql:要批量执行的语句
        #     :param rdd:数据源RDD，经过Map操作得到的tuple列表[(a,b,c),(d,e,f),(d.f.g)]
        #     :param once_size:每次执行的条数，默认每次一千条
        #     :return:
        #     '''
        #     temp = []
        #     for row in rdd.collect():
        #         if len(temp) >= once_size:
        #             self.executemany(sql, temp)
        #             temp.clear()
        #         temp.append(row)
        #
        #     if len(temp) != 0:
        #         self.executemany(sql, temp)
        #         temp.clear()



if __name__ == '__main__':
    h = MySQLHelper()
    result = h.fetchall('select * from t_order where order_id< %s', [5,])
    print(result)