# -*- coding : utf-8  -*-
"""
    @All right reserved:qiu121
    @Date_start: 2022-4-20
    @Author: qiu121
    @Email: qiu0089@foxmail.com
    @Description: a student management system with mysql-DBMS to store student information
                    and manage student information
    @Date_end: 2022-4-24
    @Version: 1.0.0
    @Python_version: 3.10.4
    @OS_version: Windows 10
    @mysql_version:8.0.28
    @Version: 1.0.0
    @Python_version: 3.10.4
    @OS_version: Windows 10
    @mysql_version:8.0.28
    @License: MIT
"""

import sys
import pymysql

host = input("Please input the host:")
user = input("Please input the user:")
passwd = input("Please input the password:")
port = int(input("Please input the port:"))

# 数据库初步连接，创建一个新的数据库
db1 = pymysql.connect(
    host=host,
    user=user,
    password=passwd,
    port=port,
    charset='utf8'
)
cursor1 = db1.cursor()
# cursor1.execute('DROP DATABASE IF EXISTS test')
# 创建一个新的数据表 test
cursor1.execute('CREATE DATABASE IF NOT EXISTS test')
db1.close()
# 如果数据表已经存在使用 execute() 方法删除表。
# cursor.execute("DROP TABLE IF EXISTS test1")
# 数据库连接
db = pymysql.connect(
    host=host,
    user=user,
    db="test",
    passwd=passwd,
    port=port,
    charset="utf8"
)
# 创建游标
cursor = db.cursor()

# 将常用的sql语句设为全局变量
sql_select_id = "SELECT * FROM students WHERE id = %s"
sql_delete_id = "DELETE FROM students WHERE id = %s"
sql_select_name = "SELECT * FROM students WHERE name = %s"
sql_delete_name = "DELETE FROM students WHERE name = %s"

# 创建一个students数据表
try:
    # cursor.execute('DROP TABLE IF EXISTS students')
    sql = '''
        CREATE table if not exists students(
        id INT(2)  NOT NULL,
        name VARCHAR (10) NOT NULL,
        age INT NOT NULL ,
        py_score INT NOT NULL ,
        data_score INT NOT NULL ,
        total_score INT NOT NULL , 
        PRIMARY KEY (id)
    )
    '''
    cursor.execute(sql)
    db.commit()

except Exception as e:
    print(e)
    print("创建数据表失败")
    sys.exit()


def menu():
    """主菜单"""
    print("学生管理系统".center(40, '='))
    print("1.显示所有学生信息")
    print("2.添加所有学生信息")
    print("3.删除指定学生信息")
    print("4.修改指定学生信息")
    print("5.查找指定学生信息")
    print("6.退出系统")
    select = input("输入你的选择：")
    if select == '1':
        try:
            print("显示所有学生信息\n")
            show()
        # 处理错误输入操作的异常
        except ValueError as e1:
            print(e1)
            show()
    elif select == '2':
        try:
            print("添加所有学生信息\n")
            add()
        except Exception as e2:
            print(e2)
            print("添加失败")
    elif select == '3':
        try:
            print("删除指定学生信息\n")
            delete()
        except ValueError:
            print("输入错误，请重新输入!!!")
            delete()
    elif select == '4':
        try:
            print("修改指定学生信息\n")
            update()
        except Exception as e2:
            print(e2)
            print("修改失败")
    elif select == '5':
        try:
            print("查找指定学生信息\n")
            retrieve()
        except ValueError as e3:
            print(e3)
            retrieve()
    elif select == '6':
        print("退出系统")
        sys.exit()
    else:
        print("输入错误，请重新输入!!!")
        menu()


def show():
    """显示所有学生信息"""
    print("选择显示排序方式：")
    print("1.按照学号排序\n2.按照总成绩排序\n")
    option_show = input("输入你的选择：")
    # 按学号排序
    if option_show == '1':
        print('按学号排序')
        try:
            sql_select = "SELECT id,name,py_score,data_score,total_score " \
                         "FROM students " \
                         "ORDER BY id"  # 默认升序
            n = cursor.execute(sql_select)  # 返回受影响的行数
            data = cursor.fetchall()
        # 异常执行
        except pymysql.err.OperationalError:
            print("查询失败")
            sys.exit()
        # 无异常执行
        else:
            # 空元组，判断是否查询到数据
            if data == ():
                print("结果为空!")
            else:
                print("id\t" + "name\t" + "py\t" + "data\t" + "total\t\n")
                # print("id".center(10, ' ') + "name".center(10, ' ') + "py".center(10, ' ') + "data".center(10, ' ') + "total".center(10, ' '))
                for records in range(len(data)):
                    for fields in range(len(data[0])):
                        print(data[records][fields], end='\t')
                    print("\n")
                print(f"已按学号显示 {n} 条学生成绩信息")
    # 按总成绩排序
    elif option_show == '2':
        print('按总成绩排序')
        try:
            # 解决怎么查询总分最高的学生
            # 总成绩降序,二级排序，学号升序
            sql_select_total = '''SELECT id,name,py_score,data_score,total_score
                FROM students 
                ORDER BY total_score DESC ,id'''
            cursor.execute(sql_select_total)
            data = cursor.fetchall()
        # 异常执行
        except pymysql.err.OperationalError:
            print("查询失败")
            sys.exit()
        # 无异常执行
        else:
            if not data:  # 空元组，返回值为False，判断是否查询到数据
                print("结果为空!")
            else:
                print("id  " + "name  " + "py  " + "data  " + "total  \n")
                for records in range(len(data)):
                    for fields in range(len(data[0])):
                        print(data[records][fields], end='\t')
                    print("\n")
                print(f"已按总成绩显示 {len(data)} 条学生成绩信息")
    else:
        raise ValueError("输入错误，请重新输入！！！")
    # 是否继续
    next_option = input("显示完成,是否继续?(y/n)")
    if next_option == 'y' or next_option == 'Y':
        menu()
    else:
        sys.exit()


def add():
    """添加学生信息"""
    # 添加数据
    n = int(input('输入要添加信息的学生数：'))
    for students in range(int(n)):
        print("请输入第%d个学生的信息：" % (students + 1))
        num = int(input("输入学生学号:"))
        name = input("输入学生姓名:")
        age = int(input("输入学生年龄:"))
        py = input("输入python成绩:")
        data_1 = input("输入数据结构成绩:")
        # 数据类型错误
        total = int(py) + int(data_1)
        length = [0] * n
        length[students] = (num, name, age, py, data_1, total)
        # 插入数据
        try:
            sql_insert = '''INSERT INTO students(id,name,age,py_score,data_score,total_score)
                                    VALUES(%s,%s,%s,%s,%s,%s)
                                '''
            cursor.execute(sql_insert, length[students])  # 批量插入
            db.commit()
        # 异常执行
        except pymysql.err.IntegrityError:  # 学号设为主键，唯一存在
            print("添加失败，该学号已存在")
            option_update = input("是否进行修改操作?(y/n)")
            if option_update == 'y' or option_update == 'Y':
                update()
            db.rollback()
        # 无异常执行
        else:
            print("添加成功")
            # 是否继续
            next_option = input("添加完毕,是否继续?(y/n)")
            if next_option == 'y' or next_option == 'Y':
                menu()
            else:
                print("程序退出")
                sys.exit()


def delete():
    """删除指定学生信息"""
    print("选择查找方式：")
    print("1.按学号查找\n2.按姓名查找\n")
    option = int(input("输入你的选择："))

    if option == 1:
        print("按学号查找")
        num = int((input("输入学生学号:")))
        # 先执行查询，验证是否存在
        cursor.execute(sql_select_id, num)
        # 将cursor.fetchone()方法的返回值，赋值给data，只返回查找的第一条 ,类型为元组
        data = cursor.fetchone()
        # 获取的数据为元组,若为空返回为None
        if data is None:  # 如果查询的学号不在数据库中,data[0]为数据表i第一列，即学号
            print("查无此人")
        else:
            # 查找成功，可以直接进行删除
            # 返回单个的元组，也就是一条记录(row)，如果没有结果, 则返回None
            print("查找成功，结果如下：")
            print("id " + "name " + "age " + "py " + "data " + "total \n")
            # 提前已判断是否查询为空，可以直接实现len()方法，【查询为空返回结果为None，NoneType 没有len()】
            for row in range(len(data)):
                print(data[row], end=" ")
            print("\n")
            # 是否删除
            option_del = input("是否删除该记录？(y/n)")
            if option_del == 'y':
                cursor.execute(sql_delete_id, num)
                db.commit()
                print("删除成功")

    elif option == 2:
        # 允许姓名不唯一存在
        print("按姓名查找")
        name = input("输入学生姓名:")
        # 执行查询,提前确定是否查询为空
        cursor.execute(sql_select_name, name)
        # 返回多个元组(二维数组)，即返回多条记录(rows),如果没有结果,则返回 (),空元组为False,不是None
        data = cursor.fetchall()
        if not data:
            print("查无此人!")
        # 查询数据不为空，即为查询操作有效，进行删除操作
        else:
            cursor.execute(sql_select_name, name)
            data = cursor.fetchall()
            print("查找成功")
            print("id" + " name" + " age" + " py" + " data" + " total\n")
            for records in range(len(data)):
                for fields in range(len(data[0])):
                    print(data[records][fields], end=' ')
                print('\n')
            print(f"查找出 {cursor.rowcount} 条有关数据")
            # 若查找结果多于1条，选择致指定删除数据或者全部删除
            if len(data) > 1:
                print("检测到查询结果多于1条，请选择删除一条或多条：")
                print("1.删除指定记录\n2.全部删除\n")
                option = input("请选择删除操作：")
                if option == '1':
                    num = input("请输入该学生学号:")
                    cursor.execute(sql_select_id, num)
                    data = cursor.fetchone()
                    print("对应学生记录如下：")
                    print("id " + "name " + "age " + "py " + "data " + "total \n")
                    for row in range(len(data)):
                        print(data[row], end=" ")
                    print("\n")
                    option_del = input("确认删除？(y/n)")
                    if option_del == 'y':
                        cursor.execute(sql_delete_id, num)
                        db.commit()
                        print("删除成功")
                elif option == '2':
                    option_del = input("是否全部删除？(y/n)")
                    if option_del == 'y':
                        cursor.execute(sql_delete_name, name)
                        db.commit()
                        print("删除成功")
            else:
                option = input("是否删除该记录？(y/n)")
                if option == 'y':
                    cursor.execute(sql_delete_name, name)
                    db.commit()
                    print("删除成功！")
    else:
        raise ValueError("输入错误,请重新输入！！！")
    # 是否继续
    next_option = input("操作完成,是否继续?(y/n)")
    if next_option == 'y' or next_option == 'Y':
        menu()
    else:
        sys.exit()


def update():
    """修改学生信息"""
    num = int(input("请输入要修改的学生学号："))
    cursor.execute(sql_select_id, num)
    data = cursor.fetchone()
    if data is None:  # 如果查询的学号不在数据库中,data[0]为数据表i第一列，即学号
        print("查无此人,无法进行修改操作")
    else:
        print("查找成功，结果如下：")
        print("id  " + "name  " + "age  " + "py  " + "data  " + "total  \n")
        # 提前已判断是否查询为空，可以直接实现len()方法，【查询为空返回结果为None，NoneType 没有len()】
        for row in range(len(data)):
            print(data[row], end='\t')
        print("\n")
        sql_update_id = '''update students
                            set py_score = %s,
                            data_score = %s,
                            total_score = %s
                            where id = %s
                              '''  # 更新语句,设置只能改成绩，总分
        py = input("请输入python成绩：")
        data_1 = input("请输入数据结构成绩：")
        total = py + data_1
        cursor.execute(sql_update_id, (py, data_1, total, num))
        db.commit()
        print("修改成功")
    next_option = input("操作完成,是否继续?(y/n)")
    if next_option == 'y' or next_option == 'Y':
        menu()
    else:
        sys.exit()


def retrieve():
    """查找学生信息"""
    print("选择查找方式：")
    print("1.按学号查找\n2.按姓名查找\n")
    option = int(input("输入你的选择："))
    if option == 1:
        # 学号唯一存在
        print("按学号查找")
        num = int(input("输入学生学号:"))
        # 执行查询,提前确定是否查询为空
        cursor.execute(sql_select_id, num)
        data = cursor.fetchone()
        if data is None:
            print("查无此人!")
        else:
            print("查找成功，结果如下：")
            print("id " + "name " + "age " + "py " + "data " + "total \n")
            for records in range(len(data)):
                print(data[records], end=' ')
            print("\n")
            print(f"查找出 {cursor.rowcount} 条有关数据")
    elif option == 2:
        print("按姓名查找")
        name = input("输入学生姓名:")
        # 执行查询,提前确定是否查询为空
        cursor.execute(sql_select_name, name)
        data = cursor.fetchall()
        if not data:
            print("查无此人!")
        else:
            print("查找成功，结果如下：")
            print("id " + "name " + "age " + "py " + "data " + "total \n")
            for records in range(len(data)):
                for fields in range(len(data[0])):
                    print(data[records][fields], end=' ')
                print('\n')
            print(f"查找出 {len(data)} 条有关数据")
    else:
        raise ValueError("输入错误,请重新输入！！！")

    # 是否继续
    next_option = input("操作完成,是否继续?(y/n)")
    if next_option == 'y' or next_option == 'Y':
        menu()
    else:
        sys.exit()


if __name__ == '__main__':
    menu()
    db.close()
