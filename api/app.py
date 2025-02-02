from fastapi import FastAPI, HTTPException
import sqlite3
import pandas as pd

app = FastAPI()

DATABASE = '../db/basedatos.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.post("/cargar_csv")
def cargar_csv():
    try:
        proyectos_df = pd.read_csv('../data/leyes_promulgadas.csv')
        leyes_df = pd.read_csv('../data/leyes_temas_principales_2023_to_2025.csv')

        conn = get_db()
        cursor = conn.cursor()

        proyectos_df.to_sql('leyes_chile', conn, if_exists='replace', index=False)

        leyes_df.to_sql('leyes_chile_temas_principales', conn, if_exists='replace', index=False)

        conn.commit()
        conn.close()

        return {"mensaje": "Datos cargados exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/consultar/{palabra_clave}")
def consultar_by_key_word(palabra_clave: str):
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM leyes_chile_temas_principales where materias like '%{palabra_clave}%'")
        leyes = cursor.fetchall()

        conn.close()

        return {
            "Result": [dict(row) for row in leyes]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/consultar/all/{id_ley}")
def consultar_by_key_word(id_ley: int):
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM leyes_chile where numero_ley =  {id_ley}")
        leyes = cursor.fetchall()

        conn.close()

        return {
            "Result": [dict(row) for row in leyes]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)