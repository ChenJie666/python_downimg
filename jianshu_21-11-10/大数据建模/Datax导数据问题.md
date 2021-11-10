### 问题一：
- 描述：datax不能创建文件夹，所以无法分区，可能导致数据重复写入或load data时错拿数据；
- 解决：datax设置writeMode为nonConflict防止重复写入，导入的文件以<日期>开头，在load data时拿取对应日期的数据。
