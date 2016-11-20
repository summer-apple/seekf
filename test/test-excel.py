import openpyxl
wb=openpyxl.Workbook()
ws=wb.create_sheet('今日统计',0)

for irow in range(100):
    ws.append(['%d' % i for i in range(20)])
wb.save(filename='test.xlsx')