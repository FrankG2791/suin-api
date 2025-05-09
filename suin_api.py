from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/documentos", methods=["GET"])
def consultar_documento():
    tipo = request.args.get("tipo")  # Leyes, Decretos, etc.
    id_suin = request.args.get("id")  # El ID interno del documento

    if not tipo or not id_suin:
        return jsonify({"error": "Parámetros 'tipo' e 'id' son obligatorios"}), 400

    # Construye la URL a SUIN
    suin_url = f"https://www.suin-juriscol.gov.co/viewDocument.asp?ruta={tipo}/{id_suin}"
    suin_response = requests.get(suin_url)

    if suin_response.status_code != 200:
        return jsonify({"error": "Documento no encontrado en SUIN"}), 404

    soup = BeautifulSoup(suin_response.content, "html.parser")

    # Extracción básica del contenido legal
    content_div = soup.find("div", class_="Texto")  # Suele ser esta clase
    texto = content_div.get_text(separator="\n") if content_div else soup.get_text()

    return jsonify({
        "tipo": tipo,
        "id_suin": id_suin,
        "url": suin_url,
        "texto": texto.strip()
    })

if __name__ == "__main__":
    app.run(debug=True)