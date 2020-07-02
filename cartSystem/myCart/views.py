from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
import json
from itertools import combinations
from math import ceil
from django.contrib.sessions.models import Session
from django.contrib.auth import logout
import pyodbc

from .models import Person, Product, ProductCategory, ForRecommendation,sub_Product, ADD_item_toCart, checkmylogin, for_Checkout_Registration, ForList, ViewList, ViewTempData, viewOrder, forCashier
# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'myCart/login.html')


def home(request, myid):

    if request.session.has_key('is_logged'):

        p = Product()
        product_list = p.showAll(myid)

        pc = ProductCategory()
        product_cat_list = pc.showAll()
        params = {'allProds': product_list, 'tt': product_cat_list}

        return render(request, 'myCart/home.html', params)

    else:
        return render(request, 'myCart/login.html')


def subpro(request, myid, myid2):
    if request.session.has_key('is_logged'):
        p = sub_Product()
        product_list = p.showAll(myid, myid2)

        pc = ProductCategory()
        product_cat_list = pc.showAll()
        params = {'allProds': product_list, 'tt': product_cat_list}

        return render(request, 'myCart/subproducts.html', params)

    else:
        return render(request, 'myCart/login.html')


def vieworder(request):
    if request.session.has_key('is_logged'):
        vo = viewOrder()
        tl = vo.vieworder()
        return HttpResponse(
            json.dumps({'result': tl}),
            content_type="application/json"
        )

    else:
        return render(request, 'myCart/login.html')


def checker(reqeust):
    return render(reqeust, 'myCart/checker.html')


def view_admin(request):

    return render(request, 'myCart/admin_vp.html')


def myview(request):
    if request.POST:
        p = Product()
        product_list = p.showAllproducts()
        # print(product_list)

        newlist = []
        for x in product_list:
            newlist.append(list(x))

        print(newlist)
        return HttpResponse(
            json.dumps({'result': "ok"}),
            content_type="application/json"
        )

    else:
        return Http404


def basic(request):
    if request.session.has_key('is_logged'):
        p = ProductCategory()
        product_list = p.showAll()
        params = {'tt': product_list}
        return render(request, 'myCart/basic.html', params)
    else:
        return render(request, 'myCart/login.html')


def add_to_list(request, sub_id):
    if request.session.has_key('is_logged'):

        for_list = ForList()
        cust_id = request.session['is_logged']
        subpro_details = for_list.addList(cust_id,sub_id)
        p = sub_Product()
        product_list = p.showAll(subpro_details[0][1], subpro_details[0][2])
        pc = ProductCategory()
        product_cat_list = pc.showAll()
        params = {'allProds': product_list, 'tt': product_cat_list}
        return render(request, 'myCart/subproducts.html', params)
    else:
        return render(request, 'myCart/login.html')
def delete_confirm(request):
    order_id = request.GET.get('order_id')
    myObj= for_Checkout_Registration ()
    x=myObj.deleteCheckoutRejection(order_id=order_id)
    return render(request, 'myCart/checker.html')

def searchmap(request):
    if request.session.has_key('is_logged'):

        return render(request, 'myCart/map.html')
    else:
        return render(request, 'myCart/login.html')


def a_searchmap(request):
    spname = request.GET.get('spname')
    dpc = sub_Product()

    prolist = dpc.pc_spcJoin(spname=spname)

    return HttpResponse(
        json.dumps({'result': prolist}),
        content_type="application/json"
    )


def map_pro_view(request):
    x = request.GET.get('x')
    y = request.GET.get('y')
    myobj = sub_Product()
    prolist = myobj.map_pro(x=x, y=y)
    print(prolist)
    return HttpResponse(
        json.dumps({'result': prolist}),
        content_type="application/json"
    )


def id_to_list(request):
    pro_id = request.GET.get('pro_id')
    print(pro_id+" in view")
    cust_id = request.session['is_logged']
    myobj = ForList()
    list_of_pro=myobj.addList(cust_id,pro_id=pro_id)
    return HttpResponse(
        json.dumps({'result': "true"}),
        content_type="application/json"
    )


def pro_details(request, myid):
    if request.session.has_key('is_logged'):

        sp = sub_Product()
        prolist = sp.showpro(myid)
        pc = ProductCategory()
        product_cat_list = pc.showAll()
        params = {'allProds': prolist, 'tt': product_cat_list}
        return render(request, 'myCart/prodetails.html', params)
    else:
        return render(request, 'myCart/login.html')


def add_item_toCart(request):
    if request.session.has_key('is_logged'):

        pc = ProductCategory()
        product_cat_list = pc.showAll()
        params = {'tt': product_cat_list}

        return render(request, 'myCart/index.html', params)
    else:
        return render(request, 'myCart/login.html')


def view_temp_data(request):
    if request.session.has_key('is_logged'):

        vp = ViewTempData()
        cust_id = request.session['is_logged']
        tl = vp.seedata(cust_id)
        return HttpResponse(
            json.dumps({'result': tl}),
            content_type="application/json"
        )
    else:
        return render(request, 'myCart/login.html')


def forcheckout(request):
    if request.session.has_key('is_logged'):

        p = for_Checkout_Registration()
        cust_id = request.session['is_logged']
        ret_list = p.addtoDb(cust_id)
        return render(request, 'myCart/index.html')
        # return HttpResponse(
        #         json.dumps({'result':"ok"}),
        #         content_type="application/json"
        #     )
    else:
        return render(request, 'myCart/login.html')

def make_confirm(request):
    order_id = request.GET.get('order_id')
    ViewOrder_ins=viewOrder()
    x=ViewOrder_ins.MakeConfirm(order_id=order_id)
    return HttpResponse(
        json.dumps({'result': x}),
        content_type="application/json"
    )
def f_checker(request):

    order_id = request.GET.get('oid')
    # print(order_id)

    fc = forCashier()
    mylist = fc.viewallpro(order_id=order_id)
    # params = {'allProds': mylist}

    firstlist = mylist['allProds']
    secondlist = mylist['allProds2']
    finallist = []
    fullfinalist = []
    # print(firstlist)
    # print(secondlist)
    # print(len(firstlist))
    # print(len(secondlist))
    val = 1
    for i in range(len(firstlist)):
        finallist.append(val)
        finallist.append(firstlist[i][1])
        finallist.append(secondlist[i][3])
        finallist.append(secondlist[i][5])
        finallist.append(firstlist[i][2])
        finallist.append(firstlist[i][3])
        finallist.append(firstlist[i][2]*firstlist[i][3])
        val = val+1

        fullfinalist.append(list(finallist))
        finallist.clear()

    params = {'od': fullfinalist,'order_id':order_id}
    return render(request, 'myCart/checker2.html', params)

def delete_row(request):
     barcode=request.GET.get('barcode')
     myobj=ADD_item_toCart()
     cust_id = request.session['is_logged']
     t=myobj.delete_row(cust_id,barcode=barcode)
     return HttpResponse(
         json.dumps({'result': t}),
         content_type="application/json"
     )


def decItem(request):
    barcode = request.GET.get('barcode')
    myobj = ADD_item_toCart()
    cust_id = request.session['is_logged']
    t = myobj.decItem(cust_id, barcode=barcode)
    return HttpResponse(
        json.dumps({'result': t}),
        content_type="application/json"
    )

def addlist(request):
    if request.session.has_key('is_logged'):

        barcode = request.GET.get('barcode')
        quantity = request.GET.get('quantity')
        cust_id = request.session['is_logged']
        p = ADD_item_toCart()
        Item_add = p.showAll(cust_id, barcode=barcode, quantity=quantity)

        # params = {'myproduct': Item_add}

        # print(params)

        # return HttpResponse(json.dumps(params), content_type="application/json")
        # lst=[(1,2,3,4),(5,6,7,8)]
        # list1={'a':lst}

        newlist = []

        for x in Item_add:
            newlist.append(list(x))

        # print(newlist)

        return HttpResponse(
            json.dumps({'result': newlist}),
            content_type="application/json"
        )

    else:
        return render(request, 'myCart/login.html')


def logout(request):
    if request.session.has_key('is_logged'):
        del request.session['is_logged']
        return render(request, 'myCart/login.html')
    else:

        return render(request, 'myCart/login.html')


def login(request):
    if request.session.has_key('is_logged'):
        return render(request, 'myCart/basic.html')
    else:

        return render(request, 'myCart/login.html')


def check_login(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        p = checkmylogin()
        person_list = p.showAll(email, password)
        print(person_list)
        if(person_list == False):
            return redirect('login')

        else:
            cust_id = person_list[0][0]
            print(cust_id)
            request.session['is_logged'] = cust_id
            p = ProductCategory()
            product_list = p.showAll()
            params = {'tt': product_list}
            return render(request, 'myCart/basic.html', params)


def ViewList_Customer(request):
    if request.session.has_key('is_logged'):
        vl = ViewList()
        cust_id = request.session['is_logged']
        sub_details = vl.showList(cust_id)
        p = ProductCategory()
        product_list = p.showAll()
        params = {'tt': product_list, 'allProds': sub_details}

        return render(request, 'myCart/list.html', params)

    else:
        return render(request, 'myCart/login.html')


xs = []
buyer = []
already = []


def recommended_items(request):
    if request.session.has_key('is_logged'):
        # takes arg like this [('i1', 'i4'),('i2','i3')]
        def getItemsetCountPairs(itemsets_):
            # print("inside getcandidate")
            Candidate_ = {itemset_: 0 for itemset_ in itemsets_}
            for itemset_ in itemsets_:  # itemset is a tuple
                #   print("\titemset: ",itemset_)
                for transaction in dataset:
                    ##print("\t\tdataset[transaction]: ", dataset[transaction])
                    ##print("\t\t",itemset_,"is subset of", set(dataset[transaction]),"?")

                    if str == type(itemset_):
                        ##print("\t\tSingleton set")
                        ##print("\t\t", set([itemset_]).issubset(set(dataset[transaction])))
                        if set([itemset_]).issubset(dataset[transaction]):
                            Candidate_[itemset_] += 1
                    else:
                        ##print("\t\t", set(itemset_).issubset(set(dataset[transaction])))
                        if set(itemset_).issubset(dataset[transaction]):
                            Candidate_[itemset_] += 1

            # returning something like this {('i1','i2'):2 ,('i2','i3'):3}
            return Candidate_

        def getShortlistedPairs(Candidate_):
            Candidate_2 = {}
            for itemset_ in Candidate_:
                SC = Candidate_[itemset_]
                if SC >= min_SC:
                    Candidate_2[itemset_] = Candidate_[itemset_]

            return Candidate_2

        def getItems(itemsets_):
            items = []
            for itemset in itemsets_:
                if tuple == type(itemset):
                    for item in itemset:
                        if item not in items:
                            items.append(item)
                elif str == type(itemset):
                    if itemset not in items:
                        items.append(itemset)
            return items

        def genAssociations(itemsets_):
            associations = []

            if type(itemsets_[0]) == str:
                itemset_set = set(itemsets_)  # because only one itemset
                for i in range(1, len(itemset_set)):
                    As_list = list(combinations(itemset_set, i))
                    for A in As_list:  # if bug itemset_set -> itemsets_
                        A_set = set(A)
                        B_set = itemset_set - A_set
                        associations.append([A_set, B_set])
                return associations

            for itemset in itemsets_:
                itemset_set = set(itemset)
                for i in range(1, len(itemset_set)):
                    As_list = list(combinations(itemset_set, i))

                    for A in As_list:  # if bug itemset_set -> itemsets_
                        A_set = set(A)
                        B_set = itemset_set - A_set
                        associations.append([A_set, B_set])
            return associations

        def getSupportCount(itemset_):
            supportCount = 0
            for transaction in dataset:
                if itemset_.issubset(dataset[transaction]):
                    supportCount += 1
            return supportCount

        def getConfidence(A_, B_):
            return getSupportCount(A_ | B_) / getSupportCount(A_)
        getRec=ForRecommendation()
        all_data=getRec.getAllData()
        # n_Ts = sum(1 for line in open('DataSet4.txt'))
        n_Ts=len(all_data)
        print(n_Ts)
        dataset = {"T" + str(_ + 1): [] for _ in range(n_Ts)}
        # f = open("DataSet4.txt", "r")
        for i in range(1, n_Ts):
            print("MY I IS : "+ str(i))
            # items = input("Enter items for T{}: ".format(i)).split()
            # items = (f.readline().format(i)).split()
            # print(items)
            # if i!=19:
            items=all_data[i].split()
            print(items)
            for item in items:
                dataset["T" + str(i)].append(item)
        # print(dataset)
        # f.close()
        min_SC = 5
        confidence_threshold = 30

        itemsets = []
        for key in dataset:  # Identifying Itemsets
            for item in dataset[key]:
                if item not in itemsets:
                    itemsets.append(item)

        # print(itemsets)
        Candidate = getItemsetCountPairs(itemsets)
        print(Candidate)
        Candidate = getShortlistedPairs(Candidate)
        # print("--------------------------------------")
        # print("After shortlisting")
        # print(Candidate)
        # Candidate = getCandidate([('i1', 'i2'), ('i2','i3')])
        # print(Candidate)
        Candidate_old = Candidate
        no_of_items_in_itemset = 1
        while max(Candidate.values()) >= min_SC:
            # print("___________________________________________________________")
            Candidate_old = Candidate
            ##print("before shortlisting: ", Candidate)
            Candidate = getShortlistedPairs(Candidate)
            ##print("After shortlisting", Candidate)

            no_of_items_in_itemset += 1
            # print(Candidate.keys())
            items = getItems(Candidate.keys())
            ##print("items=", items)
            if len(items) < no_of_items_in_itemset:
                Candidate_old = Candidate
                break
            itemsets = list(combinations(items, no_of_items_in_itemset))
            # print("itemsets:",itemsets)

            Candidate = getItemsetCountPairs(itemsets)

        ##print("Final", Candidate_old)

        frequent_sets = list(Candidate_old.keys())

        associations = genAssociations(frequent_sets)

        # print(associations)
        # print(len(associations))

        confidences = []
        confidence_percentages = []

        for association in associations:
            A, B = association
            confidences.append(getConfidence(A, B))

        # print("confidences",confidences)

        true_rules_indexes = []

        for i in range(len(confidences)):
            if confidences[i] * 100 > confidence_threshold:
                # icrementing by 1 for display
                true_rules_indexes.append(i + 1)

        recommend = []

        # print(true_rules_indexes)

        ############ Displaying final output #############
        print("\nFrequent itemset(s) are: ")
        for itemset_ in Candidate_old:
            print("itemset: {" + str(itemset_).strip("()") +
                  "} support count:", Candidate_old[itemset_])
        print()
        print("{: ^10}{: ^15}{: ^15}{: ^15}{: ^15}".format("Sr. No.", "Association Rule", "Support Count", "Confidence",
                                                           "Confidence %"))
        for i, association, confidence in zip(range(1, len(associations) + 1), associations, confidences):
            A_, B_ = association
            sc = getSupportCount(A | B)
            recommend.append(
                (str(i) + "," + str(A_).strip("{}") + "->" + str(B_).strip("{}")).replace("'", "").replace(" ", ""))
            print("{: ^10}{: ^15}{: ^15}{: ^15}{: ^15}".format(i, str(A_).strip("{}") + "->" + str(B_).strip("{}"), sc,
                                                               confidence, confidence * 100))
            # print(i, str(A_).strip("{}") + "->" + str(B_).strip("{}"), sc, confidence,confidence * 100)

        print()
        print("If the minimum confidence threshold is {} (Given),\n"
              "then only the rules {} are the output and \n"
              "final association rules generated which are strong.".format(confidence_threshold,
                                                                           str(true_rules_indexes).strip("[]")))
        best_ac = []
        for item in recommend:
            a = item.split(",")
            # print(true_rules_indexes)
            # print(a[0])
            if ((int(a[0])) in true_rules_indexes):
                best_ac.append(item)

        for item in best_ac:
            print(item)

        a = request.GET.get('my_value')
        print("values is " + str(a))
        # a =str(request.GET.get('text','default'))
        xs.append(a)
        buyer.append(a)

        for item in best_ac:
            lst = item.split("->")
            lst1 = lst[0].split(",")
            lst2 = lst[1].split(",")
            # print(lst)
            del lst1[0]
            check = True
            for aa in lst1:
                if aa not in buyer:
                    check = False
                    # break
            if (check == True):
                for x in lst2:
                    if x not in buyer:
                        if x not in already:
                            print("Recommended:- " + x)
                            already.append(x)

        # dic = {'item':'Your recommended item: '+str(already),'buyeritem':'Your cart items are : '+str(buyer)}
        print("testing")
        # k=0
        # for i in range(len(already)-k):
        #     print(already[i])
        #     if already[i] in buyer:
        #
        #         already.pop(i)
        #         k=k+1

        for item in already:
            if item in buyer:
                already.remove(item)

        print(buyer)
        print(already)
        # return render(request,'index.html',dic)
        return HttpResponse(
            json.dumps({'already_val': already, 'buyeritem': buyer}),
            content_type="application/json"
        )

    else:
        return render(request, 'myCart/login.html')

def getRec(request):
    return HttpResponse(
        json.dumps({'already_val': already}),
        content_type="application/json"
    )