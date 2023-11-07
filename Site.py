from flask import Flask, render_template, request, redirect, url_for
from Salad import Salad,Protein,Mapping,protein_sizes, Dots
from SaladDraw import SaladCreator
from io import BytesIO
from flask import send_file


app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate)

Protein_Names = [
    Name for Name in Dots.Protein_YCoords
    ]
Dressings_Names = [
    Dressing for Dressing in Dots.DOT_Locations['Dressing']
    ]
Sprinkles_Names = [
    Sprinkles for Sprinkles in Dots.DOT_Locations['Sprinkles']
    ]


# The basket stored in memory
basket = [
 # default salad in basket.
Salad(
        Size = "Large" ,
        Proteins = [
            Protein(Name = "Chicken" , Size = "1/2") ,
            Protein(Name = "Halloumi" , Size = "1/2") ,
            Protein(Name = "Avocado" , Size = "2") ,
            ] ,
        Dressings = [ "Lemon Pesto" ] ,
        Sprinkles = [ "Crispy Onion" ]
        )

    ]

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


@app.route("/" , methods = [ "GET" , "POST" ])
def index ():
    if request.method == "POST":
        size = request.form[ 'size' ]
        proteins_data = { name: request.form.get('protein_size_' + name) for name in request.form.getlist('protein') }
        dressing = request.form.getlist('dressing')
        sprinkle = request.form.getlist('sprinkle')
        Quantity = int(request.form.get("quantity"))
        proteins = [ Protein(Name = name , Size = size) for name , size in proteins_data.items() ]

        salad = Salad(Size = size , Proteins = proteins , Dressings = dressing , Sprinkles = sprinkle, Quantity = Quantity)
        basket.append(salad)

        return redirect(url_for('index'))

    # Process the basket to generate display-ready data
    display_basket = [


        ]
    for salad in basket:
        basketed_salad = {
            'Size': salad.Size ,
            'Proteins': salad.Proteins ,
            'Dressings': salad.Dressings[0] if len(salad.Dressings) == 1 else ", ".join(salad.Dressings),
            'Sprinkles': salad.Sprinkles[ 0 ] if len(salad.Sprinkles) == 1 else ", ".join(salad.Sprinkles),
            "Quantity": salad.Quantity
            }
        display_basket.append(basketed_salad)

    return render_template('index.html' ,
                           sizes = Mapping[ 'Size' ] ,
                           proteins = Protein_Names ,
                           protein_sizes = protein_sizes ,
                           dressings = Dressings_Names ,
                           sprinkles = Sprinkles_Names ,
                           basket = display_basket ,
                           basket_range = range(len(basket)))


if __name__ == "__main__":
    LOCAL = False
    try:
        app.run(debug = False , port = 5055 , host = "108.170.31.44")
    except:
        app.run(debug = False , port = 5055 , host = "127.0.0.1")
