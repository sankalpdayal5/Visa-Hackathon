import uuid


def addToCart(mysql,qty,ProductID,Name,Description,Price,merchant_id,status,finalPrice,finalDiscountPrice,negotiatedrequestAmount):

    cur = mysql.connection.cursor()
    cur.execute('select NegotiationID from Negotiation ORDER BY NegotiationID')
    a = cur.fetchall()
    negotiation_id = 1
    for  i in range(0,len(a)):
        if a[i]['NegotiationID']!=str(negotiation_id):
            continue
        else:
            negotiation_id += 1

    cart_id = uuid.uuid1()

    try:
        cur.execute('INSERT INTO Cart(CartID, Total,Status, MerchantID) VALUES(%s,%s,%s,%s)',(cart_id,finalDiscountPrice,status,merchant_id))
        mysql.connection.commit()
    except Exception as e:
        print("Problem in inserting in db"+ str(e))
        return None
    loop = len(ProductID)
    for i in range(0,loop):
        try:
            cur.execute('INSERT INTO ProductCart(CartID, ProductID,Quantity) VALUES(%s,%s,%s)',(cart_id,ProductID[i],qty[i]))
            mysql.connection.commit()
        except Exception as e:
            print("Problem in inseting into db"+str(e))
            return None

    try:
        cur.execute('INSERT INTO Negotiation(NegotiationID,Status,CartID,Price) VALUES(%s,%s,%s,%s)',(negotiation_id,"pending",cart_id,negotiatedrequestAmount))
        mysql.connection.commit()
    except Exception as e:
        print("Problem in inserting in db"+ str(e))
        return None
    cur.close()