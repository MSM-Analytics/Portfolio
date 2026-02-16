import csv
from io import StringIO
from typing import List, Dict
from fastapi.responses import StreamingResponse


def export_csv(
    filename: str,
    headers: List[str],
    rows: List[Dict]
):
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=headers)

    writer.writeheader()
    for row in rows:
        writer.writerow(row)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
