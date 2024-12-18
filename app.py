import pandas

csv_file = pandas.read_csv('import.csv')

# -------------------------------
#  Constants
percentages = {
  'labs': 0.15,
  'parcials': 0.3,
  'projects': 0.1,
  'final': 0.35,
  'attendance': 0.05,
  'portfolio': 0.05,
}

general_headers = [
  'First Name',
  'Last Name',
  'Email Address',
]

lab_headers = [
  'Laboratorio #1 - Crear cuenta de github',
  'Laboratorio #2 - Problemas básicos con Javascript',
  'Laboratorio #3 - Problemas de aplicación usando JS ',
  'Laboratorio #4 - Formulario sin usar evento submit',
  'Laboratorio #5 - Formulario sin usar evento submit agregando clases',
  'Laboratorio #6 - Flexbox',
  'Laboratorio #7 - Implementar aplicación para votación',
  'Laboratorio #8 - Grid',
  'Laboratorio #9 - Implementar aplicación basada en consumo de PokeApi',
]

parcial_headers = [
  'Parcial #1 - Tema #1',
  'Parcial #2 - Implementación de solución usando HTML/CSS/JS',
  'Parcial #3 - Implementar aplicación basada en consumo de PokeApi',
]

project_headers = [
  'Presentación #1 - Documento escrito',
  'Presentación #1 - Presentación oral',
]

attendance_headers = [
  'Asistencia',
]

portfolio_headers = [
  'Portafolio',
]

final_headers = [
  'Semestral',
]
# -------------------------------

# -------------------------------
#  Special operations
csv_file['Parcial #1 - Tema #1'] = csv_file['Parcial #1 - Tema #1'] * 2 # Double the grade of parcial #1, because the points are based on 50.
csv_file['Parcial #1 - Tema #1'] = csv_file['Parcial #1 - Tema #1'].fillna(csv_file['Semestral']) # If a parcial #1 is empty, get the grade from the semestral
csv_file['Asistencia'] = 100 # Set attendance to 100%
# -------------------------------


# Calculate data
general_data = csv_file[general_headers]

# Function to normalize and weight scores
def normalize_and_weight(data, headers, percentage):
    return ((data[headers].sum(axis=1) / len(headers)) * percentage).clip(upper=100 * percentage)

# Add headers to data
lab_data = normalize_and_weight(csv_file, lab_headers, percentages['labs'])
lab_data = lab_data.rename('Total Labs')

parcial_data = normalize_and_weight(csv_file, parcial_headers, percentages['parcials'])
parcial_data = parcial_data.rename('Total Parciales')

project_data = normalize_and_weight(csv_file, project_headers, percentages['projects'])
project_data = project_data.rename('Total Proyectos')

attendance_data = normalize_and_weight(csv_file, attendance_headers, percentages['attendance'])
attendance_data = attendance_data.rename('Total Asistencia')

portfolio_data = normalize_and_weight(csv_file, portfolio_headers, percentages['portfolio'])
portfolio_data = portfolio_data.rename('Total Portafolio')

final_data = normalize_and_weight(csv_file, final_headers, percentages['final'])
final_data = final_data.rename('Total Final')

# Calculate final grade
final_grade = lab_data + parcial_data + project_data + attendance_data + portfolio_data + final_data
final_grade = final_grade.rename('Nota Final')

# Ensure final grade doesn't exceed 100
final_grade = final_grade.clip(upper=100)

# Calculate letter grade
final_grade_letter = final_grade.apply(lambda x: 'A' if x >= 90 else 'B' if x >= 80 else 'C' if x >= 70 else 'D' if x >= 60 else 'F')
final_grade_letter = final_grade_letter.rename('Nota Final en Letra')
# -------------------------------

# Merge data
merged_data = pandas.concat([general_data, lab_data, parcial_data, project_data, attendance_data, portfolio_data, final_data, final_grade, final_grade_letter], axis=1)

# Order by last name
merged_data = merged_data.sort_values(by='Last Name')

# Export to CSV
merged_data.to_csv('export.csv', index=False)

# Export top3
merged_data_copy = merged_data.copy()
# Sort by final grade
merged_data_copy = merged_data_copy.sort_values(by='Nota Final', ascending=False)
top3 = merged_data_copy.head(3)
top3.to_csv('top3.csv', index=False)

# Export only final grade with name and last name
final_grade_only = merged_data[['First Name', 'Last Name', 'Nota Final', 'Nota Final en Letra']]
final_grade_only.to_csv('final_grade_only.csv', index=False)
