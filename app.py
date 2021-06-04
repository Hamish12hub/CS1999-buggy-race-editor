from flask import Flask, render_template, request, jsonify
import sqlite3 as sql

# app - The flask application where all the magical things are configured.
app = Flask(__name__)

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"

#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM buggies")
        record = cur.fetchone(); 
        return render_template("buggy-form.html", buggy = record )
        


    elif request.method == 'POST':
        msg=""
        qty_wheels = int(request.form['qty_wheels'])
        power_type = request.form["power_type"] 
        power_units = request.form["power_units"]
        aux_power_type = request.form["aux_power_type"]
        hamster_booster = request.form["hamster_booster"]
        flag_color = request.form["flag_color"]
        flag_pattern = request.form["flag_pattern"]
        flag_color_secondary = request.form["flag_color_secondary"]
        tyres = request.form["tyres"]
        qty_tyres = request.form["qty_tyres"]
        armour = request.form["armour"]
        attack = request.form["attack"]
        qty_attacks = request.form["qty_attacks"]
        fireproof = request.form["fireproof"]
        insulated = request.form["insulated"]
        antibiotic = request.form["antibiotic"]
        banging = request.form["banging"]
        algo = request.form["algo"]
        powerunits = int(request.form["power_units"])
        
        
        cost = 0


        if power_type == "petrol":
            cost = 4*power_units
        elif power_type == "fusion":
            cost = 400*power_units
        elif power_type == "steam":
            cost = 3*power_units
        elif power_type == "bio":
            cost = 5*power_units
        elif power_type == "electric":
            cost = 20*power_units
        elif power_type == "rocket":
            cost = 16*power_units
        elif power_type == "hamster":
            cost = 3*power_units
        elif power_type == "thermo":
            cost = 300*power_units
        elif power_type == "solar":
            cost = 40*power_units
        elif power_type == "wind":
            cost = 20*power_units

        if aux_power_type == "knobbly":
            cost = 15*power_units
        elif aux_power_type == "slick":
            cost = 10*power_units
        elif aux_power_type == "steelband":
            cost = 20*power_units
        elif aux_power_type == "reactive":
            cost = 40*power_units
        elif aux_power_type == "maglev":
            cost = 50*power_units
        

        if hamster_booster == "yes":
            cost += 5
        else:
            cost += 0

        if armour == "none":
            cost = 0 + (0.1 * qty_wheels)
        elif armour == "wood":
            cost = 40 + (0.1 * qty_wheels)
        elif armour == "aluminium":
            cost = 200 + (0.1 * qty_wheels)
        elif armour == "thinsteel":
            cost = 100 + (0.1 * qty_wheels)
        elif armour == "thicksteel":
            cost = 200 + (0.1 * qty_wheels)
        elif armour == "titanium":
            cost = 290 + (0.1 * qty_wheels)


    





















        if antibiotic == "yes":
            cost += 90
        else:
            cost += 0
        
        print(cost)

        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute(
                    "UPDATE buggies set qty_wheels=?, power_type=?, power_units=?, aux_power_type=?, hamster_booster=?, flag_color=?, flag_pattern=?, flag_color_secondary=?, tyres=?, qty_tyres=?, armour=?, attack=?, qty_attacks=?, fireproof=?, insulated=?, antibiotic=?, banging=?, algo=?, cost=? WHERE id=?",
                    (qty_wheels, power_type, power_units, aux_power_type, hamster_booster, flag_color, flag_pattern, flag_color_secondary, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, cost, DEFAULT_BUGGY_ID)
                )
                con.commit()
                msg = "Record successfully saved"
        except Exception as e:
            print('error')
            print(e)
            con.rollback()
            msg = "error in update operation"
        finally:
            con.close()
        return render_template("updated.html", msg = msg)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone(); 
    return render_template("buggy.html", buggy = record)


#------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
#------------------------------------------------------------
@app.route('/edit')
def edit_buggy():
    return render_template("buggy-form.html")

#------------------------------------------------------------
# You probably don't need to edit this... unless you want to ;)
#
# get JSON from current record
#  This reads the buggy record from the database, turns it
#  into JSON format (excluding any empty values), and returns
#  it. There's no .html template here because it's *only* returning
#  the data, so in effect jsonify() is rendering the data.
#------------------------------------------------------------
@app.route('/json')
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))

    buggies = dict(zip([column[0] for column in cur.description], cur.fetchone())).items() 
    return jsonify({ key: val for key, val in buggies if (val != "" and val is not None) })

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
