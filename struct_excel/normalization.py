import logging
import re
from openpyxl.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet
import pycountry
import phonenumbers

logger = logging.getLogger(__name__)

_ALIASES: dict[str, str] = {
    "uk": "GB",
    "u.k.": "GB",
    "england": "GB",
    "scotland": "GB",
    "usa": "US",
    "u.s.": "US",
    "america": "US",
}


def _get_row_data(ws: Worksheet, row: int) -> list:
    return [ws.cell(row=row, column=col).value for col in range(1, ws.max_column + 1)]


def _add_error_row(
    ws: Worksheet, err_ws: Worksheet, row: int, rows_to_delete: list
) -> None:
    err_ws.append(_get_row_data(ws, row))
    rows_to_delete.append(row)


def normalize_sheet(ws: Worksheet, err_ws: Worksheet) -> None:
    ws = _trim_cells(ws)
    err_ws.append([cell.value for cell in ws[1]])

    try:
        _normalize_country_and_phone_col(ws, err_ws)
    except Exception:
        pass


def _trim_cells(ws: Worksheet) -> Worksheet:
    for row in ws:
        for cell in row:
            if cell.value != None and isinstance(cell.value, str):
                cell.value = cell.value.strip()

    return ws


def _normalize_country_and_phone_col(ws: Worksheet, err_ws: Worksheet) -> None:
    headers = {cell.value: cell.column for cell in ws[1]}

    country_col = headers.get("Country")
    if not country_col:
        raise ValueError("Country column not found")

    phone_col = headers.get("Phone")
    if not phone_col:
        raise ValueError("Phone column not found")

    rows_to_delete = []

    for row in range(2, ws.max_row + 1):
        country_cell = ws.cell(row=row, column=country_col)
        phone_cell = ws.cell(row=row, column=phone_col)
        normalized_country = ""

        if not isinstance(country_cell, Cell) or not isinstance(phone_cell, Cell):
            continue

        if not isinstance(country_cell.value, str):
            _add_error_row(ws, err_ws, row, rows_to_delete)
            continue
        try:
            normalized_country = _normalize_country(country_cell.value)
            country_cell.value = normalized_country
        except ValueError as e:
            _add_error_row(ws, err_ws, row, rows_to_delete)
            logger.error(f"row: {row} exception: {e}")
            continue

        if not isinstance(phone_cell.value, str):
            _add_error_row(ws, err_ws, row, rows_to_delete)
            continue

        try:
            phone_cell.value = _normalize_phone(phone_cell.value, normalized_country)
        except ValueError as e:
            _add_error_row(ws, err_ws, row, rows_to_delete)
            logger.error(f"row: {row} exception: {e}")

    for row in reversed(rows_to_delete):
        ws.delete_rows(row)


def _normalize_country(country: str) -> str:
    if not country or not country.strip():
        raise ValueError(f"invalid country: {country}")

    country = country.strip()
    country = re.sub(r"\s+", " ", country)

    country = _ALIASES.get(country.lower(), country)

    try:
        res = pycountry.countries.lookup(country)
        return res.alpha_2
    except LookupError as e:
        raise ValueError(f"normalize country={country} failed") from e


def _normalize_phone(number: str, country: str) -> str:
    if not number or not country:
        raise ValueError(
            f"number and country cannot be empty, number={number}, country={country}"
        )

    try:
        parsed = phonenumbers.parse(number, country)
        if not phonenumbers.is_possible_number(parsed):
            raise ValueError(
                f"number={number} country={country} is not a possible number"
            )

        res = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        return res
    except phonenumbers.NumberParseException as e:
        raise ValueError(f"parse number={number} country={country} failed") from e
