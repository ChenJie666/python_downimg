###对excel表进行筛选和排序
```py
import pandas

readPath = "C:\\Users\\Administrator\\Desktop\\2019普通类_全.xlsx"
savePath = "C:\\Users\\Administrator\\Desktop\\2019普通类_筛选排序.xlsx"

data = pandas.read_excel(readPath, '2019')
# print(data)

result = data.loc[data['位次'].apply(lambda x: len(x) == 6 and '１０００００' < x < '２０００００')]
result = result.sort_values(by='位次', ascending=True)
print(result)
```

###通过openpyxl库创建excel文件和sheet表格，并实现数据的追加
```py
# TODO 创建文件和表
filepath = 'test.xlsx'
wb = openpyxl.Workbook()
#默认表sheet1
ws1 = wb.active
#更改sheet1表名
ws1.title = 'normal'
#创建sheet2表
ws2 = wb.create_sheet('success')
#保存文件
wb.save(filepath)

#追加数据
wb = openpyxl.load_workbook(filepath)
ws = wb['success']
for x in datas:
    ws.append(x)
wb.save(filepath)
```


###通过pandas的to_csv创建excel文件并实现数据追加(没有sheet表格)
