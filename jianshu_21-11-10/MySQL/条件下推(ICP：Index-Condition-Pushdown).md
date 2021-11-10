       “索引条件下推”，称为 Index Condition Pushdown (ICP)，这是MySQL提供的用某一个索引对一个特定的表从表中获取元组”，注意我们这里特意强调了“一个”，这是因为这样的索引优化不是用于多表连接而是用于单表扫描，确切地说，是单表利用索引进行扫描以获取数据的一种方式。 
        当没有icp时，存储引擎会运用索引定位到符合索引条件的行，将这些行发送给MySQL server去计算where 条件是否正确。当有icp时，如果where 条件的一部分可以通过索引来计算（意思就是索引中包含的信息可以计算这一部分where条件），那么MySQL Server就会将这部分索引条件下推到（index condition push）存储引擎（下推的意思可以看MySQL逻辑架构图）去计算，这样的话就可以返回尽量少的行给MySQL Server，也尽量少的让MySQL Server访问存储引擎层。简单来说就是索引中存储了计算where条件的信息，索引下推过滤后直接将符合条件的数据给到存储引擎计算，减少了IO。

关闭ICP：set optimizer_switch='index_condition_pushdown=off';
开启ICP：set optimizer_switch='index_condition_pushdown=on';

#关闭ICP后执行过程：
EXPLAIN SELECT * FROM t4 WHERE 1=t4.a4 AND t4.name like 'char%'; 
![image.png](https://upload-images.jianshu.io/upload_images/21580557-1660ec6b656f83bc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
过程解释：
①：MySQL Server发出读取数据的命令，这是在执行器中执行如下代码段，通过函数指针和handle接口调用存储引擎的索引读或全表表读。此处进行的是索引读。
    if (in_first_read)
    {
      in_first_read= false;
      error= (*qep_tab->read_first_record)(qep_tab); //设定合适的读取函数，如设定索引读函数/全表扫描函数
    }
    else
      error= info->read_record(info);
②、③：进入存储引擎，读取索引树，在索引树上查找，把满足条件的（经过查找，红色的满足）从表记录中读出（步骤④，通常有IO），从存储引擎返回⑤标识的结果。此处，不仅要在索引行进行索引读取（通常是内存中，速度快。步骤③），还要进行进行步骤④，通常有IO。
⑥：从存储引擎返回查找到的多条元组给MySQL Server，MySQL Server在⑦得到较多的元组。
⑦--⑧：⑦到⑧依据WHERE子句条件进行过滤，得到满足条件的元组。注意在MySQL Server层得到较多元组，然后才过滤，最终得到的是少量的、符合条件的元组。


#开启ICP后执行过程：
![image.png](https://upload-images.jianshu.io/upload_images/21580557-44a4e333ca0af0c8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
过程解释：
①：MySQL Server发出读取数据的命令，过程同图一。
②、③：进入存储引擎，读取索引树，在索引树上查找，把满足已经下推的条件的（经过查找，红色的满足）从表记录中读出（步骤④，通常有IO），从存储引擎返回⑤标识的结果。此处，不仅要在索引行进行索引读取（通常是内存中，速度快。步骤③），还要在③这个阶段依据下推的条件进行进行判断，不满足条件的，不去读取表中的数据，直接在索引树上进行下一个索引项的判断，直到有满足条件的，才进行步骤④，这样，较没有ICP的方式，IO量减少。
⑥：从存储引擎返回查找到的少量元组给MySQL Server，MySQL Server在⑦得到少量的元组。因此比较图一无ICP的方式，返回给MySQL Server层的即是少量的、符合条件的元组。
 另外，图中的部件层次关系，不再进行解释。

#四 实现细节
1 ICP只能用于辅助索引，不能用于聚集索引。
2 ICP只用于单表，不是多表连接是的连接条件部分（如开篇强调）
如果表访问的类型为：
3 EQ_REF/REF_OR_NULL/REF/SYSTEM/CONST: 可以使用ICP
4 range：如果不是“index tree only（只读索引）”，则有机会使用ICP
5 ALL/FT/INDEX_MERGE/INDEX_SCAN:  不可以使用ICP
