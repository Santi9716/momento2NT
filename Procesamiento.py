
import pandas as pd
import re
from datetime import datetime

def clean_user_id(raw_id):
    if pd.isna(raw_id):
        return None
    s = str(raw_id).strip()
    m = re.search(r'\d+', s)
    return int(m.group()) if m else None

def infer_gender(name):
    if not name or str(name).strip()=='':
        return 'na'
    n = str(name).lower()
    # quick heuristic based on common spanish names endings
    if any(x in n for x in ['maria','ana','luisa','laura','maría']):
        return 'femenino'
    if any(x in n for x in ['juan','pedro','miguel','carlos']):
        return 'masculino'
    return 'na'

def parse_notas_raw(path):
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    header = lines[0].split(',')
    for ln in lines[1:]:
        parts = [p.strip() for p in ln.split(',')]
        if len(parts) < 5:
            # skip malformed
            continue
        # id, estudiante_id, materia, nota (may contain commas), fecha (last)
        id_ = parts[0]
        estudiante_id = parts[1]
        materia = parts[2]
        fecha = parts[-1]
        nota = ','.join(parts[3:-1]) if len(parts) > 5 else parts[3]
        rows.append({'id': id_, 'estudiante_id': estudiante_id, 'materia': materia, 'nota': nota, 'fecha': fecha})
    return pd.DataFrame(rows)

def normalize_materia(s):
    if pd.isna(s):
        return 'desconocida'
    s = str(s).lower()
    s = s.replace('@','a').replace('0','o').replace('3','e')
    s = re.sub(r'[^a-záéíóúñ ]','', s)
    s = s.strip()
    return s if s else 'desconocida'

def parse_nota_value(v):
    if pd.isna(v):
        return None
    s = str(v).strip().lower()
    if s in ['', 'nan']:
        return None
    # replace common words
    if 'excel' in s:
        return 5.0
    if 'aprob' in s:
        return 3.0
    if 'mal' in s or 'malo' in s:
        return 1.0
    # replace comma decimal
    s = s.replace(',', '.')
    # keep only digits and dot and minus
    s = re.sub(r'[^0-9\.\-]', '', s)
    try:
        val = float(s)
        # clamp 0-5
        if val < 0:
            val = None
        if val is not None and val > 5:
            # if >5 maybe it's malformed, set to 5
            val = 5.0
        return val
    except:
        return None

def parse_date(s):
    if pd.isna(s):
        return pd.NaT
    s = str(s).strip()
    s = s.replace('"','').replace("'",'')
    if s.lower() in ['fecha','nan','']:
        return pd.NaT
    # try common formats
    for fmt in ['%Y/%m/%d', '%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%Y/%d/%m', '%d %m %Y', '%Y.%m.%d']:
        try:
            return pd.to_datetime(s, format=fmt)
        except:
            pass
    # last resort, let pandas try
    try:
        return pd.to_datetime(s, errors='coerce')
    except:
        return pd.NaT

def main():
    base = __import__('pathlib').Path(__file__).resolve().parents[0]
    data_dir = base / 'data'
    usuarios_path = data_dir / 'usuarios.csv'
    notas_path = data_dir / 'notas.csv'

    # --- load and normalize usuarios
    dfu = pd.read_csv(usuarios_path, dtype=str)
    # ensure columns
    if 'edad' not in dfu.columns:
        dfu['edad'] = None
    if 'genero' not in dfu.columns:
        dfu['genero'] = None

    # clean id: extract numeric
    dfu['id_raw'] = dfu['id'].astype(str)
    dfu['id_num'] = dfu['id_raw'].apply(clean_user_id)
    # assign new ids for missing
    max_id = int(dfu['id_num'].dropna().max()) if dfu['id_num'].dropna().size>0 else 0
    next_id = max_id + 1
    for idx in dfu.index:
        if dfu.at[idx,'id_num'] is None:
            dfu.at[idx,'id_num'] = next_id
            next_id += 1
    dfu['id'] = dfu['id_num'].astype(int)
    dfu.drop(columns=['id_raw','id_num'], inplace=True)

    # normalize nombre and genero
    dfu['nombre'] = dfu['nombre'].astype(str).str.strip()
    dfu['genero'] = dfu['genero'].fillna('').astype(str).str.strip().replace({'m':'masculino','f':'femenino','na':'na','':None})
    # infer if still missing
    dfu['genero'] = dfu.apply(lambda r: infer_gender(r['nombre']) if not r['genero'] else r['genero'], axis=1)
    dfu['genero'] = dfu['genero'].fillna('na')

    # edad numeric
    dfu['edad'] = pd.to_numeric(dfu.get('edad', None), errors='coerce')
    dfu['edad'] = dfu['edad'].fillna( dfu['edad'].mean() ).astype(int)

    # --- load and normalize notas with custom parser
    dfn = parse_notas_raw(str(notas_path))
    # clean estudiante_id
    dfn['estudiante_id'] = dfn['estudiante_id'].apply(lambda x: int(re.search(r'\d+', str(x)).group()) if re.search(r'\d+', str(x)) else None)
    # normalize materia
    dfn['materia'] = dfn['materia'].apply(normalize_materia)
    # parse nota numeric
    dfn['nota'] = dfn['nota'].apply(parse_nota_value)
    # fill missing notas with global mean (after parsing)
    mean_nota = dfn['nota'].dropna().mean()
    if pd.isna(mean_nota):
        mean_nota = 3.0
    dfn['nota'] = dfn['nota'].fillna(mean_nota)
    # parse fecha
    dfn['fecha'] = dfn['fecha'].apply(parse_date)
    dfn['fecha'] = pd.to_datetime(dfn['fecha'], errors='coerce').fillna(pd.Timestamp.today().normalize())

    # save cleaned files
    dfn.to_csv(data_dir / 'notas_limpias.csv', index=False)
    dfu.to_csv(data_dir / 'usuarios_limpios.csv', index=False)

    # merge
    notas_con_usuarios = pd.merge(dfn, dfu, left_on='estudiante_id', right_on='id', how='inner')
    print('Merged records:', len(notas_con_usuarios))
    # Save merged
    notas_con_usuarios.to_csv(data_dir / 'notas_con_usuarios.csv', index=False)

    # compute averages
    promedio_estudiantes = notas_con_usuarios.groupby(['estudiante_id','nombre'])['nota'].mean().reset_index().sort_values('nota',ascending=False)
    promedio_estudiantes.to_csv(data_dir / 'promedio_estudiantes.csv', index=False)
    print('Promedios saved, sample:')
    print(promedio_estudiantes.head(10).to_string(index=False))

if __name__ == "__main__":
    main()
