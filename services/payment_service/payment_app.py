from flask import Flask,request

app=Flask(__name__)

@app.route('/payment/',methods=['GET','POST'])
def payment():
    amount=int(request.args.get("amount"))
    booking_id=request.args.get("booking_id")
    if amount>250:
        return {"payment_status":"Success"}
    else:
        return {"payment_status":"Failed"}
if __name__ == '__main__':
    app.run(debug=True,port=5002)
