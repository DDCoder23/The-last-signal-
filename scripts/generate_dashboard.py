import sqlite3
import os
import html
import json


DB_PATH = "database/python_reports.db"
OUTPUT = "dashboard/index.html"


def get_data():

    if not os.path.exists(DB_PATH):
        return []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

    runs.id,
    runs.run_number,
    runs.date,
    runs.branch,

    quality_metrics.pylint,
    quality_metrics.coverage,
    quality_metrics.complexity,

    tests.failed,

    security.high,
    security.medium,
    security.low

FROM runs

LEFT JOIN quality_metrics
ON runs.id = quality_metrics.run_id

LEFT JOIN tests
ON runs.id = tests.run_id

LEFT JOIN security
ON runs.id = security.run_id

ORDER BY runs.id ASC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows



def generate_dashboard(data):

    os.makedirs(
        "dashboard",
        exist_ok=True
    )

    runs = []
    coverage = []
    pylint_values = []
    table_rows = []


    for row in data:

        (
    id,
    run,
    date,
    branch,
    pylint,
    cov,
    complexity,
    failed,
    high,
    medium,
    low
) = row

        runs.append(str(run))





        coverage.append(
            cov if cov else 0
        )

        pylint_values.append(
            score if score else 0
        )


        table_rows.append(
            f"""
            <tr>
                <td>{run}</td>
                <td>{html.escape(date)}</td>
                <td>{html.escape(branch)}</td>
                <td>{cov or 0}%</td>
                <td>{score or 0}/10</td>
            </tr>
            """
        )


    html_content = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>
The Last Signal - CI Dashboard
</title>


<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>


<style>

body {{
    font-family: Arial;
    margin: 40px;
    background:#111;
    color:white;
}}

.card {{

    background:#222;
    padding:20px;
    border-radius:10px;
    margin-bottom:20px;

}}


table {{

width:100%;
border-collapse:collapse;

}}

td,th {{

padding:10px;
border-bottom:1px solid #555;

}}

</style>


</head>


<body>


<h1>
🚀 The Last Signal - CI Dashboard
</h1>


<div class="card">

<h2>
Evolution couverture des tests
</h2>


<canvas id="coverage"></canvas>

</div>



<div class="card">

<h2>
Evolution Pylint
</h2>


<canvas id="pylint"></canvas>

</div>




<div class="card">

<h2>
Historique des builds
</h2>


<table>

<tr>
<th>Run</th>
<th>Date</th>
<th>Branche</th>
<th>Coverage</th>
<th>Pylint</th>
</tr>


{''.join(table_rows)}


</table>


</div>



<script>


new Chart(
document.getElementById('coverage'),
{{

type:'line',

data:{{
labels:{json.dumps(runs)},

datasets:[{{

label:'Coverage %',

data:{json.dumps(coverage)}

}}]

}}

}}



);



new Chart(

document.getElementById('pylint'),

{{

type:'line',

data:{{

labels:{json.dumps(runs)},

datasets:[{{

label:'Pylint /10',

data:{json.dumps(pylint)}

}}]

}}

}}

);



</script>


</body>

</html>
"""


    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            html_content
        )



if __name__ == "__main__":

    data = get_data()

    generate_dashboard(data)

    print(
        f"Dashboard généré : {OUTPUT}"
    )