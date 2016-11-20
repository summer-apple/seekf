import openpyxl
from order import OrderService

odsvs = OrderService()

class Exporter:


    def _is_defective(self, defective):
        if defective == '0':
            return '是'
        else:
            return '-'

    def export(self, trans_day):
        wb = openpyxl.Workbook()

        total_amount = 0
        total_packages = 0

        model_sheet = wb.create_sheet('统计-型号',0)


        model = odsvs.stat_by_model(trans_day)
        model_sheet.append(['型号', '件数', '双数', '单价', '折扣', '总价'])
        for d in model:
            model_sheet.append([
                d['model'],
                d['packages'],
                d['pairs'],
                d['price'],
                d['discount'],
                d['amount']
            ])
            total_amount = total_amount + d['amount']
            total_packages = total_packages + d['packages']

        model_sheet.append(['总件数', total_packages])
        model_sheet.append(['总销售额',total_amount])
        model_sheet.merge_cells(start_row=len(model)+2, end_row=len(model)+2, start_column=2, end_column=6)
        model_sheet.merge_cells(start_row=len(model) + 3, end_row=len(model) + 3, start_column=2, end_column=6)






        model_price_sheet = wb.create_sheet('统计-型号-价格',1)
        model_price = odsvs.stat_by_model_price(trans_day)
        model_price_sheet.append(['型号', '件数', '双数', '单价', '折扣', '总价'])
        for d in model_price:
            model_price_sheet.append([
                d['model'],
                d['packages'],
                d['pairs'],
                d['price'],
                d['discount'],
                d['amount']
            ])






        detail_sheet = wb.create_sheet('明细',2)
        detail = odsvs.get_orders_by_date(trans_day)
        detail_sheet.append(['型号','件数','双数','单价','折扣','总价','次品'])
        for d in detail:
            detail_sheet.append([
                d['model'],
                d['packages'],
                d['pairs'],
                d['price'],
                d['discount'],
                d['amount'],
                self._is_defective(d['defective'])

            ])

        wb.save(filename='%s日叶卡销售中心销售情况明细.xlsx' % trans_day)




if __name__ == '__main__':
    e = Exporter()
    e.export('2016-10-23')