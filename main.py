from fastapi import FastAPI,Form,UploadFile, File
from typing import Annotated
import os
import shutil
import json
from shipping import *
from datetime import datetime

app = FastAPI()

context = Context(NoDiscountStrategy(),LocalShippingStrategy())

@app.get("/files/{file_name}")
async def contenido_archivo(name: str):

    os.makedirs("output_files", exist_ok=True)
    current_dir = os.getcwd()
    folder_path = os.path.join(current_dir, "output_files",name)

    # Verificar si el archivo existe
    if not os.path.exists(folder_path):
        return {"error": f"El archivo '{name}' no existe."}

    # Leer el contenido
    with open(folder_path, "r", encoding="utf-8") as f:
        content = f.read()

    return {
        "file name": name,
        "content": content
    }

@app.post("/calculate-shipping")
async def process_file(file: UploadFile = File(...)):

    os.makedirs("output_files", exist_ok=True)
    


    contents = await file.read()
    data = json.loads(contents.decode("utf-8"))

    if data['destination'] == 'international':
        context._shipping_strategy=InternationalShippingStrategy()
    elif data['destination'] == 'national':
        context._shipping_strategy=NationalShippingStrategy()
    else:
        context._shipping_strategy=LocalShippingStrategy()

    if data['coupon'] == 'PRIME_USER':
        context._discount_strategy=PrimeUserStrategy()
    elif data['coupon'] == 'NEW_USER':
        context._discount_strategy=NewUserStrategy()
    else:
        context._discount_strategy=NoDiscountStrategy()


    final_dic=context.calculate_shipping(data['items'])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Construir nombre de archivo con timestamp  y el path para guardarlo
    current_dir = os.getcwd()
    filename = f"Output_{timestamp}.json"
    output_path = os.path.join(current_dir, "output_files",filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_dic, f, ensure_ascii=False, indent=4)

    return {"Output":f"El output file se creo bajo el nombre {filename}"}

