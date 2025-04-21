from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, text, bindparam
connection_string = "mysql+pymysql://admin:123@192.168.50.124:3306/GS"
engine = create_engine(connection_string, echo=True)
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
@app.route("/")
def index():
    return "Hello world"
@app.route("/api/GS/all")
def get_GS():
    with engine.connect() as connection:
        raw_GS = connection.execute(text("SELECT * FROM GS"))
        GS = []
        for i in raw_GS.all():
            GS.append(i._asdict())
        return jsonify(GS)
    return Response(jsonify({"status": "500", "message": "Database is down!"}), status=500)


# Метод добавления конфигурации
@app.route("/api/GS/all", methods=["POST",])
def add_GS():
    if request.method == "POST":
        form = request.form
        with engine.connect() as connection:
            query = text("INSERT INTO GS (ManufacturerCPU, ModelCPU, ManufacturerGPU, ModelGPU, SizeRAM, HertzRam, Name) VALUES (:ManufacturerCPU, :ModelCPU, :ManufacturerGPU, :ModelGPU, :SizeRAM, :HertzRam, :Name) RETURNING *")
            query = query.bindparams(bindparam("ManufacturerCPU", form.get("ManufacturerCPU")))
            query = query.bindparams(bindparam("ModelCPU", form.get("ModelCPU")))
            query = query.bindparams(bindparam("ManufacturerGPU", form.get("ManufacturerGPU")))
            query = query.bindparams(bindparam("ModelGPU", form.get("ModelGPU")))
            query = query.bindparams(bindparam("SizeRAM", form.get("SizeRAM")))
            query = query.bindparams(bindparam("HertzRam", form.get("HertzRam")))
            query = query.bindparams(bindparam("Name", form.get("Name")))
            result = connection.execute(query)
            
            connection.commit()
            return jsonify(result.fetchone()._asdict())
        return jsonify({"message": "Error"})

# Метод, чтоб не вылазила ошибка при нажатие на редактирование.
@app.route("/api/GS/<id>", methods=["GET"])
def get_single_GS(id):
    with engine.connect() as connection:
        query = text("SELECT * FROM GS WHERE id = :id")
        result = connection.execute(query.bindparams(bindparam("id", id))).fetchone()
        if result:
            return jsonify(result._asdict())
        return jsonify({"message": "Not found"}), 404

# Метод редактирования
@app.route("/api/GS/<id>", methods=["PUT"])
def update_GS(id):
    form = request.form
    with engine.connect() as connection:
        update_query = text("""
            UPDATE GS 
            SET ManufacturerCPU=:ManufacturerCPU, ModelCPU=:ModelCPU, ManufacturerGPU=:ManufacturerGPU, ModelGPU=:ModelGPU, SizeRAM=:SizeRAM, HertzRAM=:HertzRAM, Name=:Name 
            WHERE id=:id
        """)
    
        connection.execute(update_query, {
            'ManufacturerCPU': form.get("ManufacturerCPU"),
            'ModelCPU': form.get("ModelCPU"),
            'ManufacturerGPU': form.get("ManufacturerGPU"),
            'ModelGPU': form.get("ModelGPU"),
            'SizeRAM': form.get("SizeRAM"),
            'HertzRAM': form.get("HertzRAM"),
            'Name': form.get("Name"),
            'id': id
        })

        select_query = text("SELECT * FROM GS WHERE id = :id")
        result = connection.execute(select_query, {'id': id})
        updated_row = result.fetchone()
        connection.commit()
        if updated_row:
            return jsonify(updated_row._asdict())
        else:
            return jsonify({"message": "Record not found"}), 404

# Метод Удаления
@app.route("/api/GS/<id>", methods=["DELETE"])
def delete_GS(id: int):
    if request.method == "DELETE":
        with engine.connect() as connection:
            query = text("DELETE FROM GS WHERE id = :id")
            query = query.bindparams(bindparam("id", id))
            result = connection.execute(query)
            connection.commit()
        return jsonify(id)
    
def main():
    app.run("localhost", 8000, True)
if __name__ == "__main__":
    main()