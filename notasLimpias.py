import pandas as pd

# ---------------------------
# 1. Cargar los datos crudos
# ---------------------------
dfNotas = pd.read_csv("data/notas.csv")
dfUsuarios = pd.read_csv("data/usuarios.csv")

print("\n--- Archivos crudos cargados ---")
print("Notas:", dfNotas.shape, "registros")
print("Usuarios:", dfUsuarios.shape, "registros")

# ---------------------------
# 2. Limpieza de Notas
# ---------------------------

# Quitar duplicados
dfNotas = dfNotas.drop_duplicates()

# Eliminar filas sin 'nota'
dfNotas = dfNotas.dropna(subset=['nota'])

# Reemplazar valores inválidos en notas
dfNotas['nota'] = dfNotas['nota'].replace("Desconocido", None)

# Convertir notas a numéricas (forzar errores a NaN)
dfNotas['nota'] = pd.to_numeric(dfNotas['nota'], errors="coerce")

# Eliminar filas con nota vacía después de conversión
dfNotas = dfNotas.dropna(subset=['nota'])

# Asegurar rango válido (ejemplo: 0 a 5)
dfNotas = dfNotas[(dfNotas['nota'] >= 0) & (dfNotas['nota'] <= 5)]

# ---------------------------
# 3. Limpieza de Usuarios
# ---------------------------

# Quitar duplicados
dfUsuarios = dfUsuarios.drop_duplicates()

# Eliminar filas con campos críticos nulos (ej: nombre, id)
dfUsuarios = dfUsuarios.dropna(subset=['id', 'nombre'])

# ---------------------------
# 4. Guardar datos limpios
# ---------------------------
dfNotas.to_csv("data/notas_limpias.csv", index=False)
dfUsuarios.to_csv("data/usuarios_limpios.csv", index=False)

print("\n--- Archivos limpios generados correctamente ---")
print("Notas limpias:", dfNotas.shape, "registros")
print("Usuarios limpios:", dfUsuarios.shape, "registros")
