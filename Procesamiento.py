
import pandas as pd
from datetime import datetime

# ---------------------------
# Funciones simples de limpieza
# ---------------------------

def limpiar_id(valor):
    """Convierte el id en número. Si falla, devuelve None."""
    try:
        return int(str(valor).strip())
    except:
        return None

def limpiar_materia(valor):
    """Convierte la materia en minúsculas y quita espacios."""
    if pd.isna(valor):
        return "desconocida"
    texto = str(valor).lower().strip()
    # reemplazar caracteres raros
    texto = texto.replace("@", "a").replace("0", "o").replace("3", "e")
    return texto if texto != "" else "desconocida"

def limpiar_nota(valor):
    """Convierte la nota a número entre 0 y 5."""
    try:
        texto = str(valor).strip().lower()
        if texto == "" or texto == "nan":
            return None
        if "excel" in texto:
            return 5.0
        if "aprob" in texto:
            return 3.0
        if "mal" in texto:
            return 1.0
        texto = texto.replace(",", ".")
        numero = float(texto)
        if numero < 0:
            return None
        if numero > 5:
            return 5.0
        return numero
    except:
        return None

def limpiar_fecha(valor):
    """Convierte la fecha a un formato válido. Si falla, pone hoy."""
    try:
        return pd.to_datetime(valor, errors="coerce")
    except:
        return pd.Timestamp.today()

# ---------------------------
# Programa principal
# ---------------------------

def main():
    # Archivos
    usuarios_path = "data/usuarios.csv"
    notas_path = "data/notas.csv"

    # ---- Usuarios ----
    dfu = pd.read_csv(usuarios_path)

    # limpiar ids
    dfu["id"] = dfu["id"].apply(limpiar_id)

    # nombres
    dfu["nombre"] = dfu["nombre"].astype(str).str.strip().str.lower()

    # genero
    if "genero" not in dfu.columns:
        dfu["genero"] = "na"
    dfu["genero"] = dfu["genero"].fillna("na").str.strip().str.lower()

    # edad
    dfu["edad"] = pd.to_numeric(dfu["edad"], errors="coerce")
    dfu["edad"] = dfu["edad"].fillna(dfu["edad"].mean()).astype(int)

    # guardar limpio
    dfu.to_csv("data/usuarios_limpios.csv", index=False)

    # ---- Notas ----
    dfn = pd.read_csv(notas_path)

    dfn["estudiante_id"] = dfn["estudiante_id"].apply(limpiar_id)
    dfn["materia"] = dfn["materia"].apply(limpiar_materia)
    dfn["nota"] = dfn["nota"].apply(limpiar)