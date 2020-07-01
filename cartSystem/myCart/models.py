# from django.db import models
import pyodbc
import datetime
from django.db import models
# Create your models here.
from django.contrib.sessions.models import Session


class Person:
    def showAll(self):
        person_list = []
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Cart.dbo.Person')

        for i in cursor:

            person_list.append(i)

        return person_list


class Product:
    def showAll(self, id):
        person_list = []
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM Cart.dbo.myCart_prodtable where ProductCatID='+str(id))

        for i in cursor:
            person_list.append(i)

        return person_list

    def showAllproducts(self):
        product_list = []
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Cart.dbo.sub_products')

        for i in cursor:
            product_list.append(i)

        return product_list


class sub_Product:
    def showAll(self, pr_id, s_id):
        person_list = []
        print(pr_id)
        print(s_id)
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Cart.dbo.sub_products where ProductCatID=' +
                       str(pr_id)+'and ProductID='+str(s_id))

        for i in cursor:
            person_list.append(i)

        return person_list

    def showpro(self, s_id):
        person_list = []
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM Cart.dbo.sub_products where sub_product_id='+str(s_id))

        for i in cursor:
            person_list.append(i)

        return person_list

    def pc_spcJoin(self, spname):

        person_list = []
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute('''SELECT pc.location_x, pc.location_y, spc.name from Cart.dbo.myCart_procategory pc  JOIN Cart.dbo.myCart_prodtable spc ON pc.ProductCatID = spc.ProductCatID; ''')
        f1 = []
        for i in cursor:
            person_list.append(list(i))

        for i in range(len(person_list)):
            if person_list[i][2] == spname:
                kool = (person_list[i][0], person_list[i][1])
                f1.append(list(kool))
        print(f1)
        return f1

    def map_pro(self, x, y):

        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Cart.dbo.myCart_procategory')
        catid = 0
        catname = ""
        for i in cursor:
            pro_list = list(i)
            if(int(x) >= int(pro_list[4]) and int(x) <= int(pro_list[2]) and int(y) >= int(pro_list[5]) and int(y) <= int(pro_list[3])):
                catid = pro_list[0]
                catname = pro_list[1]

        person_list = []
        person_list.append(catname)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM Cart.dbo.sub_products where ProductCatID=' + str(catid))

        for i in cursor:
            person_list.append(list(i))

        return person_list
class ForRecommendation:
    def getAllData(self):
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()

        cursor.execute(
            '''select mo.order_id, sp.name from Cart.dbo.product_order po inner join Cart.dbo.myorder mo on mo.order_id=po.order_id inner join Cart.dbo.sub_products sp on po.product_id=sp.sub_product_id; ''')

        all_Transactions=[]
        str=""
        order=""
        for i in cursor:
            samp = list(i)
            if order==samp[0]:
                str = str + " " + samp[1]
            else:
                if str!="":
                    all_Transactions.append(str)
                order = samp[0]
                str=samp[1]


        return  all_Transactions












class ForList:
    def addList(self, cust_id, pro_id):
        print(pro_id)
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()

        cursor.execute(
            'SELECT * FROM Cart.dbo.sub_products where sub_product_id=' + str(pro_id))
        sub_Product_id = []

        for i in cursor:
            sub_Product_id.append(list(i))

        myq = '''INSERT INTO Cart.dbo.temp_list(Customer_id, sub_prod_id) VALUES(?,?);'''
        values = ([cust_id, sub_Product_id[0][0]])
        cursor.execute(myq, values)
        conn.commit()

        return sub_Product_id


class ViewList:
    def showList(self, cust_id):
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute(
            'SELECT sub_prod_id FROM Cart.dbo.temp_list where Customer_id=' + str(cust_id))
        sub_pro_id = []
        for i in cursor:
            sub_pro_id.append(i)

        sub_pro_details = []
        for item in sub_pro_id:
            cursor.execute(
                'SELECT * FROM Cart.dbo.sub_products where sub_product_id=' + str(item[0]))
            for i in cursor:
                sub_pro_details.append(list(i))

        return sub_pro_details


class checkmylogin:
    def showAll(self, cnic, password):
        person_list = []
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()

        cmd = "SELECT * FROM Cart.dbo.Customer where cnic='" + \
            cnic+"' and Password='"+password+"'"
        cursor.execute(cmd)

        for i in cursor:
            person_list.append(list(i))

        if(len(person_list) == 1):
            return person_list
        else:
            return False


class ProductCategory:
    def showAll(self):
        person_list = []
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Cart.dbo.myCart_procategory')

        for i in cursor:
            person_list.append(i)

        return person_list


class ADD_item_toCart:
    def showAll(self, cust_id, barcode, quantity):
        pro_details = []
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        if barcode == '8961014015683':
            barcode = 0000

        elif barcode == '4902806008944':
            barcode = 2002

        elif barcode == '6300020155037':
            barcode = 107
        cursor.execute(
            'SELECT * FROM Cart.dbo.temp_data where barcode=' + str(barcode) + 'and customer_id=' + str(cust_id))
        forInc = []
        for i in cursor:
            forInc.append(list(i))
        if(len(forInc)==0):
            cursor.execute(
                'SELECT * FROM Cart.dbo.sub_products where barcode=' + str(barcode))

            for i in cursor:
                pro_details.append(i)
            total = int(pro_details[0][6]) * int(quantity)

            myq = '''INSERT INTO Cart.dbo.temp_data(customer_id, sub_pro_id,name,Barcode,quantity,price,total) VALUES(?,?,?,?,?,?,?);'''
            values = ([cust_id, pro_details[0][0], pro_details[0][3], pro_details[0][5], quantity,
                       pro_details[0][6], total])
            cursor.execute(myq, values)
            conn.commit()
            cursor.execute(
                'SELECT * FROM Cart.dbo.temp_data where customer_id=' + str(cust_id))
            Append_list = []
            for i in cursor:
                Append_list.append(i)
            return Append_list
        else:

            increaseval = int(forInc[0][4]) + 1
            new_total = int(increaseval) * int(forInc[0][5])
            cursor = conn.cursor()
            cursor.execute('UPDATE Cart.dbo.temp_data SET quantity='+str(increaseval)+', total='+str(new_total)+'where Barcode=' + str(barcode) + 'and customer_id=' + str(cust_id))
            conn.commit()
            cursor.execute(
                'SELECT * FROM Cart.dbo.temp_data where customer_id=' + str(cust_id))
            Append_list = []
            for i in cursor:
                Append_list.append(list(i))
            return Append_list
    def decItem(self,cust_id,barcode):
        pro_details = []
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        if barcode == '8961014015683':
            barcode = 0000

        elif barcode == '4902806008944':
            barcode = 2002

        elif barcode == '6300020155037':
            barcode = 107
        cursor.execute(
            'SELECT * FROM Cart.dbo.temp_data where barcode=' + str(barcode) + 'and customer_id=' + str(cust_id))
        forDec = []
        for i in cursor:
            forDec.append(list(i))
        decseval = int(forDec[0][4]) - 1
        if(decseval==0):
            cursor.execute(
                'Delete Cart.dbo.temp_Data where barcode=' + str(barcode) + 'and customer_id=' + str(cust_id))
            cursor.commit()
        else:
            new_total = int(decseval) * int(forDec[0][5])
            cursor = conn.cursor()
            cursor.execute('UPDATE Cart.dbo.temp_data SET quantity=' + str(decseval) + ', total=' + str(
                new_total) + 'where Barcode=' + str(barcode) + 'and customer_id=' + str(cust_id))
            conn.commit()

        cursor.execute(
            'SELECT * FROM Cart.dbo.temp_data where customer_id=' + str(cust_id))
        Append_list = []
        for i in cursor:
            Append_list.append(list(i))
        return Append_list

    def delete_row(self,cust_id,barcode):
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        print(barcode)
        print(cust_id)

        cursor.execute(
            'Delete Cart.dbo.temp_Data where barcode=' + str(barcode)+'and customer_id=' + str(cust_id))
        cursor.commit()
        cursor.execute(
            'SELECT * FROM Cart.dbo.temp_data where customer_id=' + str(cust_id))
        Append_list = []
        for i in cursor:
            Append_list.append(list(i))
        return Append_list





class forCashier:
    def viewallpro(self, order_id):
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()

        cursor.execute(
            'SELECT * FROM Cart.dbo.product_order where order_id=' + str(order_id))
        Append_list = []
        for i in cursor:
            Append_list.append(list(i))

        mainitemlist = []
        for item in Append_list:
            cursor.execute(
                'SELECT * FROM Cart.dbo.sub_products where sub_product_id=' + str(item[1]))
            for i in cursor:
                mainitemlist.append(list(i))

        mydic = {'allProds': Append_list, 'allProds2': mainitemlist}
        return mydic


class viewOrder:
    def vieworder(self):
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Cart.dbo.myorder where val_confirm !=1')
        Append_list = []
        for i in cursor:
            Append_list.append(list(i))
        return Append_list
    def MakeConfirm(self,order_id):
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')
        print(order_id)


        cursor = conn.cursor()
        cursor.execute('UPDATE Cart.dbo.myorder SET val_confirm=1 WHERE order_id ='+str(order_id))
        conn.commit()
        return "yes"




class ViewTempData:
    def seedata(self, custId):
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM Cart.dbo.temp_data where customer_id=' + str(custId))
        Append_list = []
        for i in cursor:
            Append_list.append(list(i))
        return Append_list


class for_Checkout_Registration:
    def deleteCheckoutRejection(self,order_id):
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')
        cursor = conn.cursor()
        print(order_id)
        cursor.execute(
            'DELETE Cart.dbo.myorder where order_id=' + str(order_id))
        conn.commit()
        cursor.execute(
            'DELETE Cart.dbo.product_order where order_id=' + str(order_id))
        conn.commit()

    def addtoDb(self, custId):
        temp_data = []
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0PJ76QG\SQLEXPRESS;'
                              'Database=Cart;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM Cart.dbo.temp_data where customer_id=' + str(custId))

        for i in cursor:

            temp_data.append(list(i))

        total_sum = 0

        for item in temp_data:
            total_sum += item[6]

        myq = '''INSERT INTO Cart.dbo.myorder(customer_id,total_amount,date) VALUES(?,?,?);'''
        values = ([custId, total_sum, '2019-11-14'])
        cursor.execute(myq, values)
        conn.commit()

        cursor.execute(
            'SELECT * FROM Cart.dbo.myorder where customer_id=' + str(custId))
        temp_cust_order = []

        for i in cursor:
            temp_cust_order.append(list(i))
        order_id = temp_cust_order[len(temp_cust_order)-1][0]

        for item in temp_data:

            total_sum += item[6]
            myq = '''INSERT INTO Cart.dbo.product_order(order_id, product_id,quantity,price) VALUES(?,?,?,?);'''
            values = ([order_id, item[1], item[4], item[5]])
            cursor.execute(myq, values)
            conn.commit()

        cursor.execute(
            'DELETE Cart.dbo.temp_data where customer_id='+str(custId))
        conn.commit()
        cursor.execute(
            'DELETE Cart.dbo.temp_list where customer_id=' + str(custId))
        conn.commit()
        return temp_data


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name


class ProCategory(models.Model):
    ProductCatID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    sx = models.IntegerField(default=0)
    ex = models.IntegerField(default=0)
    sy = models.IntegerField(default=0)
    ey = models.IntegerField(default=0)
    location_x = models.IntegerField(default=0)
    location_y = models.IntegerField(default=0)


class ProdTable(models.Model):
    ProductID = models.AutoField(primary_key=True)
    ProductCatID = models.IntegerField()
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='Pictures', default="")
