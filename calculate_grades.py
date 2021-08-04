import csv
import os

FILENAME = os.environ.get('FILENAME', 'export.csv')


def get_float(number):
    try:
        number = float(number)
    except:
        number = 0
    return number


with open(FILENAME, newline='') as csvfile:
    exported_file = csv.DictReader(csvfile)
    for row in exported_file:
        first_name = row['\ufeff"First Name"']
        last_name = row['Last Name']
        email = row['Email Address']
        semestral = get_float(row['Semestral']) * 0.35
        parciales = (
            get_float(row['Parcial #2 - Implementación de aplicación de TO-DO']),
            get_float(row['Presentación #1 - Documento escrito']),
            get_float(row['Presentación #1 - Presentación oral'])
        )
        laboratorios = (
            get_float(row['Laboratorio #8 - Continuación de ejemplos de ExpressJS (Docker)']),
            get_float(row['Laboratorio #7 - Continuación de ejemplos de ExpressJS (Frontend)']),
            get_float(row['Laboratorio #6 - Continuación de ejemplos de ExpressJS']),
            get_float(row['Laboratorio #5 - Problemas usando JS con HTML tablas']),
            get_float(row['Laboratorio #4 - Problemas de aplicación usando JS con HTML']),
            get_float(row['Laboratorio #3 - Problemas de aplicación usando JS ']),
            get_float(row['Laboratorio #2 - Problemas básicos con Javascript']),
            get_float(row['Laboratorio #1 - Crear cuenta de github']),
        )
        parciales = (sum(parciales) / len(parciales)) * 0.30
        print(f'parciales: {parciales}')
        laboratorios = (sum(laboratorios) / len(laboratorios)) * 0.30
        print(f'laboratorios: {laboratorios}')
        print(f'semestral: {semestral}')
        asistencia = 0.05
        grade = semestral + parciales + laboratorios + asistencia
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
        print(f'{first_name} {last_name}: {grade} ({grade_in_letter})')
        print()
