from flask import Flask, render_template, request, redirect, url_for, jsonify
from Salad import Salad,Protein,Mapping,protein_sizes, Dots,Poke_Dots, Salad_Display_Names
from SaladDraw import SaladCreator
from io import BytesIO
from flask import send_file
import json

app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate)
app.jinja_env.globals.update(tojson=json.dumps)

Protein_Names = [
    Name for Name in Dots.Protein_YCoords
    ]
Dressings_Names = [
    Dressing for Dressing in Dots.DOT_Locations['Dressing']
    ]
Sprinkles_Names = [
    Sprinkles for Sprinkles in Dots.DOT_Locations['Sprinkles']
    ]

Poke_Protein_Names = [
    Name for Name in Poke_Dots.Protein_YCoords
    ]

Poke_Dressings_Names = [
    Dressing for Dressing in Poke_Dots.DOT_Locations['Dressing']
    ]
Poke_Sprinkles_Names = [
    Sprinkles for Sprinkles in Poke_Dots.DOT_Locations['Sprinkles']
    ]



# The basket stored in memory
basket = [
 # default salad in basket.
Salad(
        Name = "Crunch Box",
        Size = "Large" ,
        Proteins = [
            Protein(Name = "Chicken" , Size = "1/2") ,
            Protein(Name = "Halloumi" , Size = "1/2") ,
            Protein(Name = "Avocado" , Size = "2") ,
            ] ,
        Dressings = [ "Lemon Pesto" ] ,
        Sprinkles = [ "Crispy Onion" ],
        Gluten_Free = False,
        )

    ]


def get_basket_order_size():
    total_orders = 0
    for item in basket:
        total_orders += item.Quantity
    return total_orders , len(basket)

@app.route("/clear_basket", methods=["POST"])
def clear_basket():
    basket.clear()
    return redirect(url_for('index'))


@app.route("/delete", methods=["POST"])
def delete_salad():
    salad_id = int(request.form['salad_id'])
    if 0 <= salad_id < len(basket):
        del basket[salad_id]
    return redirect(url_for('index'))

@app.route("/order_all", methods=["POST"])
def order_all():
    pages = []

    for salad_id, salad in enumerate(basket):
        print(f"Create order for {salad}")

        pdfInstance = SaladCreator(Salad=salad)

        pdfInstance.run()

        # Repeat the image based on the quantity of the salad
        pages.extend([pdfInstance.image] * salad.Quantity)

    # Save images to PDF in-memory
    buffered = BytesIO()
    pages[0].save(buffered, "PDF", save_all=True, append_images=pages[1:])

    # Go to the start of the buffer for reading
    buffered.seek(0)

    # Send the PDF as a response
    return send_file(buffered, mimetype='application/pdf', as_attachment=False, download_name='salad_order.pdf')


@app.route("/order", methods=["POST"])
def order():
    # Extract the salad ID from the form
    salad_id = int(request.form['salad_id'])

    # Get the salad from the basket using the ID
    salad = basket[salad_id]
    print(f"Create order for {salad}")

    pdfInstance = SaladCreator(Salad = salad)

    pdfInstance.run()



    #pdfInstance.image.save("out.png")

    pages = [ pdfInstance.image ] * salad.Quantity

    # Save images to PDF in-memory
    buffered = BytesIO()
    pages[ 0 ].save(buffered , "PDF" , save_all = True , append_images = pages[ 1: ])

    # Go to the start of the buffer for reading
    buffered.seek(0)

    # Send the PDF as a response
    return send_file(buffered , mimetype = 'application/pdf' , as_attachment = False , download_name = 'salad_order.pdf')


@app.route("/add_to_basket", methods=["POST"])
def add_to_basket():
    print(request.form)
    Gluten_Free = False
    if request.form.get('Gluten_Free' , False): Gluten_Free = True
    if request.form.get('Gluten_Free_poke' , False): Gluten_Free = True

    Name = request.form.get('box_type')
    size = request.form[ 'size' ]
    proteins_data = { name: request.form.get('protein_size_' + name) for name in request.form.getlist('protein') }
    dressing = request.form.getlist('dressing')
    sprinkle = request.form.getlist('sprinkle')
    Quantity = int(request.form.get("quantity"))
    proteins = [ Protein(Name = name , Size = size) for name , size in proteins_data.items() ]

    salad = Salad(Name = Name , Size = size , Proteins = proteins ,
                  Dressings = dressing , Sprinkles = sprinkle ,
                  Quantity = Quantity , Gluten_Free = Gluten_Free
                  )
    basket.append(salad)
    return jsonify({"success": True, "message": "Item added to basket"})


def get_display_basket():
    display_basket = [ ]

    for salad in basket:
        basketed_salad = {
            "Name": salad.Name ,
            "Gluten_Free": 'Yes' if salad.Gluten_Free else 'No' ,
            'Size': salad.Size ,
            'Proteins': f"{salad.Proteins[ 0 ].Size} {salad.Proteins[ 0 ].Name}" if len(salad.Proteins) == 1 else ", ".join(
                [ f"{p.Size} {p.Name}" for p in salad.Proteins ]) ,

            'Dressings': salad.Dressings[ 0 ] if len(salad.Dressings) == 1 else ", ".join(salad.Dressings) ,
            'Sprinkles': salad.Sprinkles[ 0 ] if len(salad.Sprinkles) == 1 else ", ".join(salad.Sprinkles) ,
            "Quantity": salad.Quantity
            }
        display_basket.append(basketed_salad)
    return display_basket

@app.route("/get_basket")
def get_basket():
    total , basket_size = get_basket_order_size()
    return jsonify({"Basket": get_display_basket() , "total_orders": total, "basket_size": basket_size})


@app.route("/" , methods = [ "GET" ])
def index ():
    # Process the basket to generate display-ready data
    display_basket = get_display_basket()
    total , basket_size = get_basket_order_size()

    return render_template('index.html' ,
                           sizes = Mapping[ 'Size' ] ,
                           proteins = Protein_Names ,
                           protein_sizes = protein_sizes ,
                           dressings = Dressings_Names ,
                           sprinkles = Sprinkles_Names ,
                           basket = display_basket ,
                           basket_range = range(len(basket)),
                           salad_names = Salad_Display_Names.keys(),

                           #poke_bowl options:
                            poke_proteins = Poke_Protein_Names,
                            poke_dressings = Poke_Dressings_Names,
                            poke_sprinkles = Poke_Sprinkles_Names,

                           basket_size = basket_size,
                           basket_total = total
                           )


if __name__ == "__main__":
    LOCAL = False
    try:
        app.run(debug = False , port = 5055 , host = "66.85.157.72")
    except:
        app.run(debug = False , port = 5055 , host = "127.0.0.1")
