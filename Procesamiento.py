import pandas as pd
from datetime import datetime

# ---------------------------
# 1. Diagnosticar datos
# ---------------------------
dfNotas = pd.read_csv('data/notas.csv')
dfUsuarios = pd.read_csv('data/usuarios.csv')

print(dfNotas.info())
print(dfUsuarios.info())

# ---------------------------
# 2. Cargar primeros datos
# ---------------------------
print(dfUsuarios.head(20))
print(dfNotas.head(20))

# ---------------------------
# 3.1 limpieza de datos en Notas
# ---------------------------

# Nota → numérico (float), inválidos a NaN
dfNotas['nota'] = pd.to_numeric(dfNotas['nota'], errors='coerce')

# Rellenar notas nulas con promedio general
promedio_general = dfNotas['nota'].mean()
dfNotas['nota'].fillna(promedio_general, inplace=True)

# Materia → string limpio
dfNotas['materia'] = dfNotas['materia'].astype(str).str.strip().str.lower()
dfNotas['materia'].fillna('desconocida', inplace=True)

# estudiante_id → numérico
dfNotas['estudiante_id'] = pd.to_numeric(dfNotas['estudiante_id'], errors='coerce')
dfNotas['estudiante_id'].fillna(-1, inplace=True)  # si falta, poner -1 o lo que definas
dfNotas['estudiante_id'] = dfNotas['estudiante_id'].astype(int)

# Fecha → limpiar espacios y convertir a datetime
dfNotas['fecha'] = dfNotas['fecha'].astype(str).str.strip()
dfNotas['fecha'] = pd.to_datetime(dfNotas['fecha'], errors='coerce')
dfNotas['fecha'].fillna(pd.Timestamp.today().normalize(), inplace=True)

print("--- Notas Limpias ---")
dfNotas.info()

# ---------------------------
# 3.2 limpieza de datos en Usuarios
# ---------------------------

# Edad → numérico
dfUsuarios['edad'] = pd.to_numeric(dfUsuarios['edad'], errors='coerce')
dfUsuarios['edad'].fillna(dfUsuarios['edad'].mean(), inplace=True)
dfUsuarios['edad'] = dfUsuarios['edad'].astype(int)

# Nombre → string limpio
dfUsuarios['nombre'] = dfUsuarios['nombre'].astype(str).str.strip().str.lower()
dfUsuarios['nombre'].fillna('desconocido', inplace=True)

# ID → numérico
dfUsuarios['id'] = pd.to_numeric(dfUsuarios['id'], errors='coerce')
dfUsuarios['id'].fillna(dfUsuarios['id'].max() + 1, inplace=True)
dfUsuarios['id'] = dfUsuarios['id'].astype(int)

# Género → string limpio
dfUsuarios['genero'] = dfUsuarios['genero'].astype(str).str.strip().str.lower()
dfUsuarios['genero'].fillna('desconocido', inplace=True)

print("--- Usuarios Limpios ---")
dfUsuarios.info()

# ---------------------------
# 4. Guardar datos limpios
# ---------------------------
dfNotas.to_csv('data/notas_limpias.csv', index=False)
dfUsuarios.to_csv('data/usuarios_limpios.csv', index=False)


# ---------------------------
# 5.1 Filtrado con [] (utilizar para filtrar filas)
# ---------------------------

# Notas mayores o iguales a 3 (aprobados)
aprobados = dfNotas[dfNotas['nota'] >= 3]

# Ejemplo en matematicas aprobados
aprobados_mate = dfNotas[(dfNotas['nota'] >= 3) & (dfNotas['materia'] == 'matemáticas')]
dfNotas.loc[(dfNotas['materia'] == 'matemáticas') & (dfNotas['nota'] > 4), ['estudiante_id', 'nota']]
# Ejemplo en matematicas reprobados
reprobados_mate = dfNotas[(dfNotas['materia'] == 'matemáticas') & (dfNotas['nota'] < 3)]
print(reprobados_mate.head())

#Ejemplo en todas las materias mostrando los primeros 20 registros
aprobados = dfNotas[dfNotas['nota'] >= 3]
print(aprobados.head(20))

# Notas aplicadas en un año especifico 20 primeros registros
notas_2023 = dfNotas[dfNotas['fecha'].dt.year == 2023]
print(notas_2023.head(20))

# Estudiantes con notas perfectas
NotasPerfectas = dfNotas[dfNotas['nota'] == 5]
print(NotasPerfectas)

#Filtrar estudiantes de genero femenino
femeninos = dfUsuarios[dfUsuarios['genero'] == 'femenino']
print(femeninos.head())


# ---------------------------
# 5.2 Filtrado con .loc (es mas potente, filtra filas y columnas)
# ---------------------------

# Todos los estudiantes aprobados
aprobados = dfNotas.loc[dfNotas['nota'] >= 3, ['estudiante_id', 'nota']]
print(aprobados.head())

# Notas reprobadas en lengua con los primeros 5 registros
dfNotas.loc[(dfNotas['materia'] == 'lengua') & (dfNotas['nota'] < 3)].head()

# Reprobados en matematicas, filtrando nombre y fecha 
reprobados_mate = dfNotas.loc[
    (dfNotas['materia'] == 'matemáticas') & (dfNotas['nota'] < 3),
    ['estudiante_id', 'fecha']
]
print(reprobados_mate.head())

# Notas perfectas , imprime el id del estudiante,  materia y fecha
notas_perfectas = dfNotas.loc[dfNotas['nota'] == 5, [ 'estudiante_id', 'materia', 'fecha']]
print(notas_perfectas)

# Usuarios femeninos con id
femeninos = dfUsuarios.loc[dfUsuarios['genero'] == 'femenino', ['id', 'nombre']]
print(femeninos.head())

# Filtrar usuarios sin genero
sin_genero = dfUsuarios.loc[dfUsuarios['genero'] == 'desconocido', ['id', 'nombre']]
print(sin_genero.head())


# ---------------------------
# 6.1 Concatenación .concat()
# ---------------------------

# Unir la cabeza y la cola del listado Usuarios como si fueran dos listas diferentes
usuarios_parte1 = dfUsuarios.head(50)   # primeros 50
usuarios_parte2 = dfUsuarios.tail(50)   # últimos 50
# Concatenamos verticalmente
usuarios_todos = pd.concat([usuarios_parte1, usuarios_parte2], axis=0)
print(usuarios_todos.shape)

#Crear una nueva columna con la edad en meses
edad_meses = dfUsuarios['edad'] * 12
dfEdadExtra = pd.DataFrame(edad_meses, columns=['edad_meses'])
# Concatenamos al lado (el axis=1 coloca columnas de forma horizontal)
usuarios_expandido = pd.concat([dfUsuarios, dfEdadExtra], axis=1)
print(usuarios_expandido.head())

# ---------------------------
# 6.2 Fusión .merge()
# ---------------------------

# Relación de estudiantes con notas
notas_con_usuarios = pd.merge(
    dfNotas, dfUsuarios,
    left_on='estudiante_id',  # columna en dfNotas
    right_on='id',            # columna en dfUsuarios
    how='inner'               # tipo de unión
)

print(notas_con_usuarios.head())

# Calculo de nota promedio por estudiante
promedio_estudiantes = dfNotas.groupby('estudiante_id')['nota'].mean().reset_index()

# Unimos con dfUsuarios para ver nombres
promedio_con_nombres = pd.merge(
    promedio_estudiantes, dfUsuarios,
    left_on='estudiante_id',
    right_on='id',
    how='inner'
)

print(promedio_con_nombres[['nombre', 'nota']].head())





