import sqlite3
from flask import Flask,jsonify,request,Response as re



app=Flask(__name__)

def connect_db():
    db=sqlite3.connect('groceries.db')
    db.execute('CREATE TABLE IF NOT EXISTS Items (item_id INTEGER PRIMARY KEY, item_name TEXT, item_price REAL, item_quant)')
    db.commit()

# connect_db()


@app.route('/')
@app.route('/home')
def home_page():
    endpoint={
        '/available_items(GET)':" lists all available items in the Items DB with the quantity <0",
        '/all_items(GET) ':" lists all items in the DB regardless quantity",
        '/add_item(POST) ':" adds an item to the db",
        '/get_item_by_id/<id>(GET) ':" displays an item of the id selected",
        '/available_items_total_cost ':" provides a sum of all products in the 'store' ",
        '/update_item/<id>(PUT) ':" updates item based on ID",
        '/delete_item/<id>(DELETE) ':" deletes item based on ID"
    }
    msg=f'Wellcome to the sotore!\n\nOur enpoints:\n'+'\n'+"\n".join([f"{x}:{y}" for x,y in endpoint.items()])
    return re(msg,mimetype='text/plain')


@app.route('/list_of_all_items',methods=['GET'])
def all_items():
    items=[]

    try:
        with sqlite3.connect('groceries.db') as db:
            db.row_factory=sqlite3.Row
            cursor=db.cursor()
            cursor.execute('SELECT * FROM Items')
            items=cursor.fetchall()
    except Exception as e:
        db.rollback()
        return jsonify('Error: '+str(e))
    finally:
        return jsonify([dict(x) for x in items]) if items else jsonify('No items in the DB')


@app.route('/add_item',methods=['POST'])
def add_item():
    msg=None

    try:
        data=request.get_json()
        item_name=data['item_name']
        item_price=data['item_price'] if data['item_price'] else 0
        item_quant=data['item_quant'] if data['item_quant'] else 0

        with sqlite3.connect('groceries.db') as db:
            cursor=db.cursor()
            cursor.execute('INSERT INTO Items (item_name,item_price,item_quant) VALUES (?,?,?)',(item_name,item_price,item_quant))
            db.commit()
            msg=f'Item {item_name} has been added to the DB with the quantity of {item_quant}!'
    except Exception as e:
        db.rollback()
        msg='Error: '+str(e)
    finally:
        return jsonify(msg=msg)
    







if __name__=='__main__':
    app.run(debug=True)
    
 