import pandas
import os

file_name = "import.csv"

if not os.path.exists(file_name):
    raise FileNotFoundError("File not found: " + file_name)

# Flag to indicate if this is a mid-semester calculation (50% of final grade)
IS_MID_SEMESTER = True

csv_file = pandas.read_csv(file_name)

# -------------------------------
#  Constants
percentages = {
    "labs": 0.15,
    "parcials": 0.3,
    "projects": 0.1,
    "final": 0.35,
    "attendance": 0.05,
    "portfolio": 0.05,
}

general_headers = [
    "First Name",
    "Last Name",
    "Email Address",
]

lab_headers = [
    "Laboratorio #1 - Crear cuenta de github",
    "Laboratorio #2 - Problemas básicos con Javascript",
    "Laboratorio #3 - Problemas de aplicación usando JS ",
    "Laboratorio #4 - Problemas de aplicación usando JS y HTML",
]

parcial_headers = [
    "Parcial #1 - Temas de presentaciones",
    "Parcial #2 - Bookshelf",
]

project_headers = [
    "Presentación #1 - Documento escrito",
    "Presentación #1 - Presentación oral",
]

attendance_headers = [
    "Prueba diagnóstica",
]

portfolio_headers = [
    "Portafolio",
]

final_headers = [
    "Semestral",
]
# -------------------------------

# -------------------------------
#  Special operations
csv_file["Parcial #1 - Temas de presentaciones"] = (
    csv_file["Parcial #1 - Temas de presentaciones"] * 2
)  # Double the grade of parcial #1, because the points are based on 50.

# If Semestral exists, use it as fallback for empty Parcial #1 grades
if "Semestral" in csv_file.columns:
    csv_file["Parcial #1 - Temas de presentaciones"] = csv_file[
        "Parcial #1 - Temas de presentaciones"
    ].fillna(csv_file["Semestral"])

csv_file["Prueba diagnóstica"] = 100  # Set attendance to 100%
# -------------------------------


# Calculate data
general_data = csv_file[general_headers]


# Function to normalize and weight scores
def normalize_and_weight(data, headers, percentage):
    return ((data[headers].sum(axis=1) / len(headers)) * percentage).clip(
        upper=100 * percentage
    )


# Add headers to data
lab_data = normalize_and_weight(csv_file, lab_headers, percentages["labs"])
lab_data = lab_data.rename("Total Labs")

parcial_data = normalize_and_weight(csv_file, parcial_headers, percentages["parcials"])
parcial_data = parcial_data.rename("Total Parciales")

project_data = normalize_and_weight(csv_file, project_headers, percentages["projects"])
project_data = project_data.rename("Total Proyectos")

attendance_data = normalize_and_weight(
    csv_file, attendance_headers, percentages["attendance"]
)
attendance_data = attendance_data.rename("Total Asistencia")

# Handle portfolio data
if IS_MID_SEMESTER:
    # In mid-semester, always give 100% for portfolio
    portfolio_data = pandas.Series(
        100 * percentages["portfolio"], index=csv_file.index, name="Total Portafolio"
    )
else:
    # In final calculation, use actual portfolio data if it exists
    if "Portafolio" in csv_file.columns:
        portfolio_data = normalize_and_weight(
            csv_file, portfolio_headers, percentages["portfolio"]
        )
        portfolio_data = portfolio_data.rename("Total Portafolio")
    else:
        portfolio_data = pandas.Series(
            100 * percentages["portfolio"],
            index=csv_file.index,
            name="Total Portafolio",
        )

# Handle final data
if IS_MID_SEMESTER:
    # In mid-semester, always give 100% for semestral
    final_data = pandas.Series(
        100 * percentages["final"], index=csv_file.index, name="Total Final"
    )
else:
    # In final calculation, use actual semestral data if it exists
    if "Semestral" in csv_file.columns:
        final_data = normalize_and_weight(csv_file, final_headers, percentages["final"])
        final_data = final_data.rename("Total Final")
    else:
        final_data = pandas.Series(
            100 * percentages["final"], index=csv_file.index, name="Total Final"
        )

# Calculate final grade
final_grade = (
    lab_data
    + parcial_data
    + project_data
    + attendance_data
    + portfolio_data
    + final_data
)
final_grade = final_grade.rename("Nota Final")

# Ensure final grade doesn't exceed 100
final_grade = final_grade.clip(upper=100)

# If this is mid-semester, adjust the grade to represent 50% of the final grade
if IS_MID_SEMESTER:
    final_grade = final_grade * 0.5
    final_grade = final_grade.rename("Nota Final (50%)")

# Calculate letter grade based on the appropriate scale
if IS_MID_SEMESTER:
    # For mid-semester, adjust the letter grade thresholds
    final_grade_letter = final_grade.apply(
        lambda x: (
            "A"
            if x >= 45  # 90% of 50
            else (
                "B"
                if x >= 40  # 80% of 50
                else (
                    "C"
                    if x >= 35  # 70% of 50
                    else "D" if x >= 30 else "F"  # 60% of 50
                )
            )
        )
    )
else:
    # For final grade, use normal thresholds
    final_grade_letter = final_grade.apply(
        lambda x: (
            "A"
            if x >= 90
            else "B" if x >= 80 else "C" if x >= 70 else "D" if x >= 60 else "F"
        )
    )
final_grade_letter = final_grade_letter.rename("Nota Final en Letra")
# -------------------------------

# Merge data
merged_data = pandas.concat(
    [
        general_data,
        lab_data,
        parcial_data,
        project_data,
        attendance_data,
        portfolio_data,
        final_data,
        final_grade,
        final_grade_letter,
    ],
    axis=1,
)

# Order by last name
merged_data = merged_data.sort_values(by="Last Name")

# Export to CSV
merged_data.to_csv("export.csv", index=False)

# Export top3
merged_data_copy = merged_data.copy()
# Sort by final grade
grade_column = "Nota Final (50%)" if IS_MID_SEMESTER else "Nota Final"
merged_data_copy = merged_data_copy.sort_values(by=grade_column, ascending=False)
top3 = merged_data_copy.head(3)
top3.to_csv("top3.csv", index=False)

# Export only final grade with name and last name
final_grade_only = merged_data[
    ["First Name", "Last Name", grade_column, "Nota Final en Letra"]
]
final_grade_only.to_csv("final_grade_only.csv", index=False)
