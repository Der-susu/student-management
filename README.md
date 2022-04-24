# Student-Management  
##  学生信息管理系统
 a student management system with mysql-DBMS to store student information and manage student information  
 ## 说明  
 - 此项目为一个用mysql数据库存储数据的简易学生信息管理系统（初始的数据表字段较少）
 - 此项目开发时用的是本地数据库，因此使用该项目首先配置登陆个人数据库
 - 此项目使用的是 **input** 输入数据库登陆相关参数（host,user,port,passwd and etc.）
 - 此项目处理了几乎所有笔者考虑到的异常错误（包括但不限于错误输入）

## 注意  
- 本项目将连接两次数据库
- 第一次初步连接以创建一个新的名为 ***test*** 的数据库，为便于后续创建数据表，这里会直接将名为 **test** 数据库 **直接删除**（如果存在）  
     `DROP DATABASE IF EXISTS test`  
     `CREATE DATABASE IF NOT EXISTS test`  
     如若在您个人数据库存在test数据库，建议您对此重命名，或者更改项目源码
- 第二次连接将在数据库test下创建名为 ***students*** 的数据表   
      `CREATE  IF NOT EXITS students(field1,field2,field3 ...) `   
        

## 后记
- 此项目算是笔者第一个比较完整的项目  
- 此项目只是通过控制台输出，后续会增加UI界面,比如小型UI库tkinter，或者直接推出带UI的完整新项目
- 项目写于疫情防控下的南昌某高校，利用业余时间完成（多是夜晚） 

## 赞助  
- 您的赞助是对笔者最大的鼓励与支持  
![sponsor-QRcode](./images/5119D4B90F47C4B706737C4E8BE28C7D)

## 交流
- 如若您看后有若干意见或建议，欢迎大佬指正  
- [联系我](qiu0089@foxmail.com)
