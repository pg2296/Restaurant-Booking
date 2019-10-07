from models import *
import json
def capitalize_string(input_str):
    str_list=input_str.split(" ")
    output=" ".join([part.capitalize() for part in str_list])
    return output

def get_table_count(no_of_persons):
    table_count={"T2":0,"T4":0,"T6":0}
    while no_of_persons>0:

        if no_of_persons>6:
            table_count['T6']+=no_of_persons//6
            no_of_persons=no_of_persons%6
            print(no_of_persons)
        elif no_of_persons<=6 and no_of_persons>4:
            table_count['T6']+=1
            no_of_persons=0

        elif no_of_persons<=4 and no_of_persons>2:
            table_count['T4']+=1
            no_of_persons=0
        elif no_of_persons<=2 and no_of_persons>0:
            table_count['T2']+=1
            no_of_persons=0
    return table_count

def check_availability(rest_id,booking_date,selected_slot,no_of_persons):
    table_count=get_table_count(no_of_persons)

    out={}
    check_table_count={}

    for t_type,count in table_count.items():

        if not count==0:

            tables=Tables.query.filter_by(restaurant_id=rest_id,table_type=t_type).all()

            if tables:
                check=0
                for row in tables:
                    table_status=row.Availablity.filter_by(booking_date=booking_date).first()

                    if table_status:

                        slots=json.loads(table_status.slots)
                        if slots[selected_slot]:
                            check+=1


                    else:
                        check+=1
                    if check==count:
                        check_table_count[t_type]=count
                        break

            else:
                out["message"] ="We are unable to fetch the Availablity for given restaurant. Please contact restaurant for booking"
                return out
        else:
            check_table_count[t_type]=count

    if check_table_count==table_count:
        out['message']="Available, You can proceed with the booking"

    else:
        out['message']="Not Available!!, Please check for other time slots or dates"
    return out

def calculate_bill(rest_id,selected_menu,no_of_persons):
    table_count=get_table_count(no_of_persons)
    results=Restaurant.query.filter_by(id=rest_id).first()
    menus=results.menus.all()


    bill=0
    for item in selected_menu:
        for menu in menus:
            if menu.name==item[0]:
                bill+= item[1]*menu.price
    for t_type,count in table_count.items():
        if not count==0:
            bill+=count*results.table_types.filter_by(type=t_type).first().price

    return bill
