from bottle import run, route
import os

@route("/")
def index():
    page =   f'''
                <h1>Ping Web App</h1>
                <p>Pings host/multiple hosts</p>
                <p>Usage: <i>http://127.0.0.1:8080/youtube.com,google.com,192.168.1.1</i></p>
            '''
    return page

# Web app that pings a host or multiple hosts
@route("/<host>")
def index(host):
    host_list = host.split(",")
    body = ""

    for value in host_list:
        value = value.strip()
        try:
            response = os.popen(f"ping -c 1 {value}").read()
        except:
            response = "Couldn't connect"
        if response == "":
            response = "Host couldn't resolve"
        body += f"<h2>{value}</h2><pre>{response}</pre>"

    header = '<meta http-equiv="refresh" content="5">'
    return f"{header}{body}"

run(host="127.0.0.1", port=8080)