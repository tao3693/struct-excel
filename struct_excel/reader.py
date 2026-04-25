from openpyxl.worksheet.worksheet import Worksheet

from models import RawRow


def read_raw_row(ws: Worksheet) -> list[RawRow]:
    headers = {cell.value: idx for idx, cell in enumerate(ws[1])}
    rows = []

    for row in ws.iter_rows(min_row=2, values_only=True):
        rows.append(
            RawRow(
                reg_date=row[headers["Reg Date"]],
                student_full_name=str(row[headers["Full Name"]]),
                student_email=str(row[headers["Email"]]),
                student_company=str(row[headers["Company"]]),
                student_job_title=str(row[headers["Job Title"]]),
                country=str(row[headers["Country"]]),
                exception=str(row[headers["Exception"]]),
                phone=str(row[headers["Phone"]]),
                course=str(row[headers["Course"]]),
                gender=str(row[headers["Gender"]]),
                sector=str(row[headers["Sector"]]),
                supervisor_name=str(row[headers["Supervisor's Name"]]),
                supervisor_email=str(row[headers["Supervisor's Email"]]),
                it_background=str(row[headers["IT/Cybersecurity bckgrd (Yes/No)"]]),
                experience=str(row[headers["IT/Cybersecurity work exp (yrs)"]]),
                completed=str(row[headers["Completed"]]),
                payment_status=str(row[headers["Payment Status"]]),
            )
        )

    return rows
