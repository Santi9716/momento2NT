import pandas as pd

# ---------------------------
# 1. Cargar los datos limpios
# ---------------------------
dfNotas = pd.read_csv("data/notas_limpias.csv")
dfUsuarios = pd.read_csv("data/usuarios_limpios.csv")

print("\n--- Archivos cargados correctamente ---")
print("Notas:", dfNotas.shape, "registros")
print("Usuarios:", dfUsuarios.shape, "registros")

# ---------------------------
# 2. Análisis de las preguntas
# ---------------------------

# 1. Frecuencia → ¿Cuál es la materia con más registros positivos de calificaciones?
materia_mas_registros = (
    dfNotas[dfNotas['nota'] >= 3]   # Solo notas aprobadas
    .groupby('materia')['nota']
    .count()
    .sort_values(ascending=False)
)
print("\n1. Materia con más registros positivos de calificaciones:")
print(materia_mas_registros.head(1))

# 2. Agregación → ¿Cuál es la nota promedio por cada materia?
promedio_por_materia = dfNotas.groupby('materia')['nota'].mean().sort_values(ascending=False)
print("\n2. Nota promedio por materia:")
print(promedio_por_materia)

# 3. Filtrado y Conteo → ¿Cuántos estudiantes aprobaron?
aprobados = (
    dfNotas.groupby('estudiante_id')['nota']
    .mean()
    .reset_index()
)
num_aprobados = (aprobados['nota'] >= 3).sum()
print("\n3. Número de estudiantes que aprobaron:", num_aprobados)

# 4. Top Rendimiento → ¿Cuál es el estudiante con la nota más alta en todas las materias?
mejor_nota = dfNotas['nota'].max()
mejor_estudiante = dfNotas.loc[dfNotas['nota'] == mejor_nota, 'estudiante_id'].unique()
print("\n4. Estudiante(s) con la nota más alta:", mejor_estudiante, "con nota", mejor_nota)

# 5. Asistencia de datos faltantes → ¿Cuántas notas están vacías?
faltantes = dfNotas['nota'].isna().sum() + (dfNotas['nota'] == 'Desconocido').sum()
print("\n5. Número de notas faltantes/inválidas:", faltantes)

# ---------------------------
# 3. Fin del análisis
# ---------------------------
print("\n--- Análisis completado ---")

