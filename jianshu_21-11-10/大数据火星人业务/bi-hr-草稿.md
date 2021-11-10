问题：
1. 缺少 离职原因表 离职性质表  员工类型表  学历字典表

**employee**
1	0001	黄卫斌	NULL	26	39	83	NULL	NULL	1	1	1	20	NULLULL	2010-04-08 00:00:00.0	NULL	NULL	NULL	NULL	NULL	NULL	NULL	41	1	3304ULL	1	1	NULL	2021-06-08

  EID int, 
  Badge string, 工号 
  Name string, 姓名
  EName string,
  CompID int,
2681	2525	陈捷	  NULL	26
  DepID int, 部门id
  JobID int, 职位id
  ReportTo int,
  wfreportto int,
  EmpStatus int,
73	710	2582	NULL	1	
  JobStatus int,
  EmpType int,
  EmpGrade int,
  EmpCustom1 int,
  EmpCustom2 int,
1	1	4	NULL	1	
  EmpCustom3 int,
  EmpCustom4 int,
  EmpCustom5 int,
  WorkCity int,  工作地点
  JoinType int,
1	NULL	NULL	6	NULL	
 JoinDate string,  入职日期
  WorkBeginDate string,  
  JobBeginDate string,  
  PracBeginDate string,
  PracTerm int,  
2019-10-14 00:00:00.0   NULL   2019-11-08 00:00:00.0	NULL	NULL	
  PracEndDate string,
  ProbBeginDate string,  试用期开始日期
  ProbTerm int,  试用期（月）
  ProbEndDate string,  转正日期
  ConCount int,
NULL	2019-10-14 00:00:00.0	2	2019-12-13 00:00:00.0	2	
  contract int,
  ConType int,
  ConProperty int,
  ConNo string,
  ConBeginDate string,  合同开始日期    可能和入职日期不同
1	1	1	NULL	2020-10-14 00:00:00.0	
  ConTerm int,
  ConEndDate string,   合同结束时间
  LeaveDate string,  离职日期
  LeaveType int,  离职性质
  LeaveReason int,  离职原因
36	2023-10-13 00:00:00.0	NULL	NULL	NULL	
  Wyear_Adjust decimal(9,2),
  Cyear_Adjust decimal(9,2),
  Country int,
  CertType int,
  CertNo string,
NULL	NULL	41	1	330283199310071816	
  Gender int,
  BirthDay string,
  email string,
  Mobile string,
  office_phone string,
1     1993-10-07 00:00:00.0	chenjie@marssenger.com	18851703029	NULL	
  EZID int,
  Remark string,
  empcompany int,
  isprac int,
  isprob int,
100	NULL	NULL   2  2	
  isleave int,
  htfujian string,
  Leaveproperty int,
  isSchool int,
  school string,
NULL	NULL	NULL	NULL	NULL
  joborder int,
  joblevel int,   职级
  isStay int
2	10	NULL	2021-06-08

2469	2286	徐绍华	NULL	26	73	1041	2582	NULL	
2	1	1	3	NULL	1	1	NULL	NULL	6	NULL	
2019-07-08 00:00:00.0	NULL	2021-02-21 00:00:00.0	NULL	NULL	NULL	
2019-07-08 00:00:00.0	2	2019-09-07 00:00:00.0	2	1	1	1	NULL	
2020-07-08 00:00:00.0	36	2023-07-07 00:00:00.0	
2021-03-26 00:00:00.0	1	10	NULL	NULL	41	1	411423199604250014	1	
1996-04-25 00:00:00.0	xushaohua@marssenger.com	15515547083	NULL	
100	NULL	NULL	2	2	NULL	NULL	2	1	NULL	2	10	NULL	2021-06-08




**job**
83	zc	总经理	总经理	39	NULL	NULL	1	NULL	1	NULL	2010-04-08 00:00:00.0	NULL	NULL	NULL	NULL	NULL	NULL	NULL	NULL	NULL	100	2	2021-06-08
39	ZC	总经理室	总经理室	26	NULL	1	1	1	NULL	1	NULL	NULL	NULL	2010-04-08 00:00:00.0	NULL	NULL	NULL	NULL	1829	NULL	NULL	NULL	NULL	NULL	100	2021-06-08



**ecdjoblevel**
1	M7	NULL	NULL	1	2021-06-08

**ecdempgrade**
1	01	2	2	NULL	NULL	NULL	NULL	2021-06-08


**edetails**
1	NULL	1	13	NULL	11	NULL	NULL	NULL	2	NULL	NULL	浙江省海宁市紫薇花园4幢2单元	浙江省海宁市紫薇花园4幢2单元	NULL	NULL	NULL	NULL	NULL	NULL	NULL	NULL	169	1166	浙江省海宁市紫薇花园4幢2单元	NULL	13600568888	NULL	2021-06-08

2681	NULL	1	13	NULL	12	3	NULL	电子科学与技术	1	NULL	1	浙江省奉化市锦屏街道河头路２１幢４０１室	浙江省杭州市下城区流水西苑19号楼1单元502	13858352106	NULL	NULL	NULL	NULL	NULL	NULL	NULL	NULL	1131	浙江省宁波市奉化区锦屏街道河头路21幢	北京世纪一家网电子商务有限公司	18851703029	NULL	2021-06-08

2469	NULL	1	3	NULL	12	3	NULL	计算机科学与技术	1	NULL   1河南省宁陵县城关回族镇近溪街１１号	杭州市下城区万家星城35幢2单元1801号	13781607521徐礼勇      NULL	NULL	NULL	NULL	NULL	NULL	NULL	NULL	1803	河南省宁陵县乔楼镇白庄村委孟庄	郑州佰知科技有限公司	15515547083	NULL	2021-06-08

  EID int,
  BirthPlace string,
  nation int,
  party int,
  partydate string,
  HighLevel int,
  HighDegree int,
  HighTitle int,
  Major string,
  Marriage int,
  Health int,
  Resident int,
  residentAddress string,
  Address string,
  TEL string,
  Postcode string,
  QQ string,
  eMail_pers string,
  Wechart string,
  Weibo string,
  BloodType string,
  Constellation string,
  sfzfujian string,
  place int,
  letteraddress string,
  lastcomaddress string,
  Mobile string,
  email string

![image.png](https://upload-images.jianshu.io/upload_images/21580557-ff39f97ef77dd155.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/21580557-5feebe0e1de75c7e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```sh
#!/bin/bash

if [ -n "$1" ];then
  month=$1
else
  month=`date -d '-1 month' +"%Y-%m"`

SELECT 
  
FROM 
(
SELECT 
  Badge,
  Name,
  DepID,
  JobID,
  joblevel,
  JoinDate,
  ProbBeginDate,
  ProbEndDate,
  ConBeginDate,
  ConEndDate,
  LeaveDate,
  LeaveType,
  LeaveReason,
  
FROM ods_employee 
WHERE substr(leavedate,1,7)="2021-03"
)
```
