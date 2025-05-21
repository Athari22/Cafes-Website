from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, select
from random import choice



app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)



class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random", methods=["GET"])
def get_random_cafe():
    """Fetch a random cafe from the database and return it as JSON."""
    cafes = Cafe.query.all()
    if cafes:
        random_cafe = choice(cafes)
        return jsonify(cafe=random_cafe.as_dict())  # wrapped in "cafe": {} for clarity
    else:
        return jsonify(error="No cafes available in the database"), 404

@app.route("/all")
def get_all_cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.as_dict() for cafe in all_cafes])



@app.route('/search', methods=['GET'])
def search_cafes_by_location():
    """Search for cafes based on the location parameter."""
    location = request.args.get('loc', None)  # Get the 'loc' query parameter
    if location is None:
        return jsonify({"error": "Missing 'loc' parameter"}), 400  # Bad request if 'loc' is missing

    # Use `ilike` for case-insensitive search based on the location
    stmt = select(Cafe).where(Cafe.location.ilike(f"%{location}%"))  # Case-insensitive search
    cafes = db.session.execute(stmt).scalars().all()

    if cafes:
        return jsonify(cafes=[cafe.as_dict() for cafe in cafes])  # Return all matching cafes as JSON
    else:
        return jsonify({"message": f"No cafes found in location: {location}"}), 404  # No cafes found

@app.route("/add", methods=["POST"])
def post_new_cafe():
    data = request.get_json()

    new_cafe = Cafe(
        name=data.get("name"),
        map_url=data.get("map_url"),
        img_url=data.get("img_url"),
        location=data.get("loc"),
        has_sockets=bool(int(data.get("sockets"))),
        has_toilet=bool(int(data.get("toilet"))),
        has_wifi=bool(int(data.get("wifi"))),
        can_take_calls=bool(int(data.get("calls"))),
        seats=data.get("seats"),
        coffee_price=data.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."}), 201


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_coffee_price(cafe_id):
    new_price = request.args.get("new_price")  # نحصل على السعر الجديد من الـ URL params

    if not new_price:
        return jsonify(error="Missing 'new_price' parameter"), 400

    cafe_to_update = db.session.get(Cafe, cafe_id)

    if cafe_to_update:
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": f"Coffee price updated to {new_price} for cafe id {cafe_id}"}), 200
    else:
        return jsonify(error="Cafe not found"), 404

@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")

    if api_key != "TopSecretAPIKey":
        return jsonify(error="Not authorized to delete. Invalid API Key."), 403

    cafe_to_delete = db.session.get(Cafe, cafe_id)
    if cafe_to_delete:
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(response={"success": f"Cafe with id {cafe_id} has been deleted."}), 200
    else:
        return jsonify(error="Cafe not found."), 404


if __name__ == '__main__':
    app.run(debug=True)
