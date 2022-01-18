from flask import Flask, request
import couchdb

# api setup
app = Flask(__name__)

# database access
#define couchDB
couch_conn_string = None


if "COUCH_DB_CONN_STRING" in os.environ.keys():
    couch_conn_string = os.environ["COUCH_DB_CONN_STRING"]
else:
    raise Exception("COUCH_DB_CONN_STRING environment variable does not exist")

couch = couchdb.Server(couch_conn_string)
db = couch['raygun_errors']

@app.route("/api/raygun_webhook", methods=['POST'])
def addToDatabase():
    req = request.json

    for id in db:
        if id == request.json["application"]["name"]:
            doc = db[request.json["application"]["name"]]
            doc["reports"].append(req)
            db.save(doc)
            return "Doc updated"
        else:
            doc = {"_id": request.json["application"]["name"], "reports": [req]}
            db.save(doc)
            return "Doc created"



@app.route("/<application_name>")
def showRaygunErrorTable(application_name):
    
    for id in db:
        if id == application_name:
            doc = db[application_name]
            reports = doc["reports"]

            tableRows = ""
            for report in reports:
                tableRows = f"<tr><td>{report['error']['message']}</td><td><a href={report['error']['url']}>Link to Raygun</a></td><td>{report['error']['firstOccurredOn']}</td><td>{report['error']['lastOccurredOn']}</td><td>{report['error']['totalOccurrences']}</td></tr>"

            html = f"""<!DOCTYPE html>
                    <html>
                    <style>
                    table, th, td {{
                    border:1px solid black;
                    }}
                    </style>
                    <body>

                    <h2>Raygun issues</h2>

                    <table style="width:100%">
                    <tr>
                        <th>Message</th>
                        <th>Error URL</th>
                        <th>First Occurred On</th>
                        <th>Last Occurred On</th>
                        <th>Total Occurrences</th>
                    </tr>
                    {tableRows}
                    </table>

                    <p>Visit <a href={"https://app.raygun.com/"}>Raygun</a> for more information</p>

                    </body>
                    </html>
                """
            return (
                html
            )
        else:
                html = f"""<!DOCTYPE html>
                <html>
                <style>
                table, th, td {{
                border:1px solid black;
                }}
                </style>
                <body>

                <h2>Raygun issues</h2>

                <p>Visit <a href={"https://app.raygun.com/"}>Raygun</a> for more information</p>

                </body>
                </html>
            """
        return (
            html
        )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
