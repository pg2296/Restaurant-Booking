from booking_app import app,db
from models import *
from flask import request,Blueprint
from flask_sqlalchemy import inspect
from validations import capitalize_string,get_table_count,check_availability,calculate_bill
import json,ast,requests



booking_blueprint = Blueprint('booking',__name__)
table_dict={"T2":"Table For 2","T4":"Table For 4","T6":"Table For 6"}

@booking_blueprint.route('/search/',methods=['GET','POST'])
def search_restaurant():
    rest_name=capitalize_string(request.args.get("rest_name"))
    results=Restaurant.query.filter_by(name=rest_name).all()
    print(results)
    out={}
    count=1
    if results:
        for obj in results:
            out['Restaurnt'+str(count)]={"Name":obj.name,"Address":obj.address}
            count+=1
    else:
        return {"message":"Given Restaurant is not registered with us!!"}
    return out

@booking_blueprint.route('/restaurant/details/',methods=['GET','POST'])
def restaurant_details():
    rest_id=request.args.get("rest_id")
    results=Restaurant.query.filter_by(id=rest_id).first()
    if results:
        out={'Restaurant Name':results.name,
             'Restaurant Address': results.address,
             'Restaurant Contact and Email': results.contact+" "+results.email,
             'Restaurant_Tables' : {},
             'Restaurant_menu':{}
            }
        menus=results.menus.all()
        tables=results.table_types.all()
        print(tables)
        rest_menu={}

        if menus:
            for row in menus:
                rest_menu[row.name]=row.price
        else:
            rest_menu["message"]="Unable to fetch the Menu, Kindly contact restaurant for more details."
        out['Restaurant_menu']=rest_menu

        if tables:
            rest_table=[table_dict[row.type] for row in tables]
            out['Restaurant_Tables']['Table Varities Available']=rest_table
        else:
            out['Restaurant_Tables']={'message':"Please contact restaurant to get table details"}

    else:
        return {"message":"Given Restaurant is not registered with us!!"}

    return out


@booking_blueprint.route('/restaurant/availablity/',methods=['GET','POST'])
def restaurant_availablity():
    rest_id=request.args.get("rest_id")
    booking_date=request.args.get("booking_date").split("-")
    booking_date=datetime(int(booking_date[0][1:]),int(booking_date[1]),int(booking_date[2][:-1]))
    selected_slot=request.args.get("selected_slot")
    no_of_persons=int(request.args.get("no_of_persons"))
    booking_date[:-4]

    return check_availability(rest_id,booking_date,selected_slot,no_of_persons)

@booking_blueprint.route('/booking/',methods=['GET','POST'])
def book_table():
    rest_id=request.args.get("rest_id")
    booking_date=request.args.get("booking_date").split("-")
    booking_date=datetime(int(booking_date[0][1:]),int(booking_date[1]),int(booking_date[2][:-1]))
    selected_slot=request.args.get("selected_slot")
    no_of_persons=int(request.args.get("no_of_persons"))
    selected_menu=request.args.get("selected_menu").split("-")
    selected_menu=[ast.literal_eval(items) for items in selected_menu]
    print(selected_menu)

    result=check_availability(rest_id,booking_date,selected_slot,no_of_persons)
    out={}

    if "proceed" in result['message']:
        bill=calculate_bill(rest_id,selected_menu,no_of_persons)
        result=Booking.query.order_by(Booking.id.desc()).first()
        if result:
            id=result.id+1
        else:
            id=1
        payment_api_url=" http://127.0.0.1:5002/payment/"
        params={'amount':bill,'booking_id':id}
        response=requests.get(payment_api_url,params=params)
        if response.status_code==200:
            if response.json()["payment_status"]=="Success":
                payment_status="Paid"
                status="Confirmed"
                book=Booking(id,rest_id,booking_date,status,no_of_persons,selected_menu,payment_status,selected_slot)
                db.session.add(book)
                db.session.commit()
                out['Booking ID']=id
                out['Booking Date and Slot']=booking_date[0:12]+"  "+selected_slot
                out['Menu Selected']=selected_menu
                out['Booking Status']=status
            else:
                out['message']="Payment Failed!! Try again"
        else:
            out['message']="We are facing some issues please try again after some time"


    else:
        out['message']="Sorry!! The Slot was just booked by another user. Please change slot or date"
    return out
