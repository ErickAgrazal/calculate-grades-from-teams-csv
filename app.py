import pandas

csv_file = pandas.read_csv('import.csv')

# Personal information
csv_file['Nombre'] = csv_file['First Name']
csv_file['Apellidos'] = csv_file['Last Name']
csv_file['Correo'] = csv_file['Email Address']

# Use the semestral grade as the Lab #10 grade if it's missing or is 0
csv_file['Laboratorio #10 - Agregar backend al código del parcial #2'] = csv_file.apply(
  lambda row:
    row['Laboratorio #10 - Agregar backend al código del parcial #2']
    if row['Laboratorio #10 - Agregar backend al código del parcial #2'] > 0
    else row['Semestral'],
  axis=1
)

# Use the semestral grade as the partial #2 grade if it's missing or is 0
csv_file['Parcial #1 - Temas de presentaciones'] = csv_file.apply(
  lambda row:
    row['Parcial #1 - Temas de presentaciones']
    if row['Parcial #1 - Temas de presentaciones'] > 0
    else row['Semestral'] * 0.28,
  axis=1
)

# Lab grades
csv_file['Laboratorios'] = (csv_file[
  [
    'Laboratorio #1 - Crear cuenta de github',
    'Laboratorio #2 - Problemas básicos con Javascript',
    'Laboratorio #3 - Problemas de aplicación usando JS ',
    'Laboratorio #4 - Problemas de aplicación usando JS y HTML',
    'Laboratorio #5 - Implementar aplicación para captura de notas',
    'Laboratorio #6 - Login simulator',
    'Laboratorio #7 - Desarrollo de endpoint que retorne fibonacci',
    'Laboratorio #8 - Desarrollo de endpoint que retorne fibonacci',
    'Laboratorio #9 - Integrar front con endpoint que retorna fibonacci',
    'Laboratorio #10 - Agregar backend al código del parcial #2',
  ]
].sum(axis=1) / 10) * 0.25

# Partial grades
csv_file['original_parcial_1'] = csv_file['Parcial #1 - Temas de presentaciones']
csv_file['Parcial #1 - Temas de presentaciones'] = csv_file['Parcial #1 - Temas de presentaciones'].apply(lambda x: x * 100/28)
csv_file['Parciales'] = (csv_file[
  [
    'Parcial #1 - Temas de presentaciones',
    'Parcial #2 - Income and Expenses system',
    'Presentación #1 - Documento escrito',
    'Presentación #1 - Presentación oral',
    'Semestral - Avance #1 - CasosDeUso/HistoriasDeUsuario/etc'
  ]
].sum(axis=1) / 4) * 0.30

# Final grade calculation
csv_file['Portafolio'] = csv_file['Portafolio'] * 0.05
csv_file['Semestral'] = csv_file['Semestral'] * 0.35
csv_file['Asistencia'] = 5
csv_file['Final'] = (
  csv_file['Semestral'] +
  csv_file['Asistencia'] +
  csv_file['Portafolio'] +
  csv_file['Laboratorios'] +
  csv_file['Parciales']
).round()
csv_file['Final en letra'] = csv_file['Final'].apply(lambda x: 'F' if x < 60 else 'D' if x < 70 else 'C' if x < 80 else 'B' if x < 90 else 'A')

# Export only the columns we need
csv_file = csv_file[
  [
    'Apellidos',
    'Nombre',
    'Final en letra',
    'Semestral',
    'Correo',
    'Final',
    'Laboratorio #1 - Crear cuenta de github',
    'Laboratorio #2 - Problemas básicos con Javascript',
    'Laboratorio #3 - Problemas de aplicación usando JS ',
    'Laboratorio #4 - Problemas de aplicación usando JS y HTML',
    'Laboratorio #5 - Implementar aplicación para captura de notas',
    'Laboratorio #6 - Login simulator',
    'Laboratorio #7 - Desarrollo de endpoint que retorne fibonacci',
    'Laboratorio #8 - Desarrollo de endpoint que retorne fibonacci',
    'Laboratorio #9 - Integrar front con endpoint que retorna fibonacci',
    'Laboratorio #10 - Agregar backend al código del parcial #2',
    'Parcial #1 - Temas de presentaciones',
    'Parcial #2 - Income and Expenses system',
    'Presentación #1 - Documento escrito',
    'Presentación #1 - Presentación oral',
    'Semestral - Avance #1 - CasosDeUso/HistoriasDeUsuario/etc',
    'Asistencia',
    'original_parcial_1',
  ]
]

csv_file = csv_file.sort_values(by=['Apellidos'], ascending=True)
csv_file.to_csv('export.csv', index=False)

# Export the top 5 students to a new file
csv_file = csv_file.sort_values(by=['Final'], ascending=False)
csv_file = csv_file.head(5)
csv_file.to_csv('top3.csv', index=False)
