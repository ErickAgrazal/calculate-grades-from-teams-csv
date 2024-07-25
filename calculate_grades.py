import collections
import csv
import os

IMPORT_FILE = os.environ.get('IMPORT_FILENAME', 'import.csv')
EXPORT_FILE = os.environ.get('EXPORT_FILENAME', 'export.csv')


def get_float(number):
    try:
        number = float(number)
    except:
        number = 0
    return number


with open(IMPORT_FILE, newline='') as csvfile:
    counter = {}
    with open(EXPORT_FILE, 'w') as exportfile:
        writer = csv.writer(exportfile)
        writer.writerow(('nombre', 'correo', 'parciales', 'laboratorios', 'semestral', 'final', 'final en letra'))
        exported_file = csv.DictReader(csvfile)
        for row in exported_file:
            first_name = row['\ufeff"Nombre"']
            last_name = row['Apellidos']
            email = row['Dirección de correo']
            semestral_raw = row['Examen semestral - Construir CV ']
            semestral = get_float(semestral_raw) * 0.35
            parciales = (
                get_float(row['Parcial # 1']),
                get_float(row['Proyecto #1 - Implementar el HTML y CSS en base al Wireframe']),
                get_float(row['Presentación #1 - Trabajo escrito']),
                get_float(row['Presentación #1 - Presentación Oral'])
            )
            laboratorios = (
                get_float(row['Laboratorio #8 - Construir frontend para calculadora']),
                get_float(row['Laboratorio #7 - Crear endpoints para calculadora']),
                get_float(row['Laboratorio #6 - Aplicar Flexbox a formulario de estudiantes']),
                get_float(row['Laboratorio #5 - Generar cartas usando CSS (Flexbox)']),
                get_float(row['Laboratorio #4 - Aplicar CSS a un formularios básicos']),
                get_float(row['Laboratorio #3 - Crear documento HTML con formularios básicos']),
                get_float(row['Laboratorio #2 - Crear documento HTML con etiquetas de visualización']),
                get_float(row['Laboratorio #1 - Crear documento HTML con la información sobre la ']),
            )
            parciales = (sum(parciales) / len(parciales)) * 0.30
            laboratorios = (sum(laboratorios) / len(laboratorios)) * 0.30
            asistencia = 0.05
            grade = round(semestral + parciales + laboratorios + asistencia)
            if grade < 61:
                grade_in_letter = 'F'
            elif grade < 71:
                grade_in_letter = 'D'
            elif grade < 81:
                grade_in_letter = 'C'
            elif grade < 91:
                grade_in_letter = 'B'
            else:
                grade_in_letter = 'A'
            counter[grade_in_letter] = counter.get(grade_in_letter, 0) + 1
            print(f'{first_name} {last_name}: {grade} ({grade_in_letter})')
            writer.writerow((f'{first_name} {last_name}', email, parciales, laboratorios, semestral_raw, grade, grade_in_letter))
        writer.writerow(('-------------------', ))
        writer.writerow(('letra', 'cantidad'))
        ordered_dict = collections.OrderedDict(sorted(counter.items()))
        for letter, count in ordered_dict.items():
            writer.writerow((letter, count))
        print('Exported')
