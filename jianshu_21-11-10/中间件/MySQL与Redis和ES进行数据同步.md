**同步Redis：**
1. MySQL进行新增操作时，不需要对Redis进行操作；
2. MySQL进行更新、删除操作时，在同一个线程中先对Redis进行操作，然后对MySQL进行操作，最后通过maxwell监控binlog文件再次对redis进行异步删除操作。

**同步ES：**
1. 监控MySQL的binlog，通过MQ异步对ES进行同步操作。
