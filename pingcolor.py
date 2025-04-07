from bottle import run, route
import os
import re

latency_quality = {"good": 20, "usable": 30, "bad": 50}

@route("/")
def index():
    page =  '''
                <h1>Ping Web App</h1>
                <p>Pings host/multiple hosts</p>
                <p>Usage: <i>http://127.0.0.1:8080/youtube.com,google.com,192.168.1.1</i></p>
            '''
    return page

@route("/<host>")
def index(host):
    command = "ping -c 1"
    host_list = host.split(',')
    arg = " | grep time"
    body = ""

    for host in host_list:
        host = host.strip()
        try:
            # Run ping and filter output with grep
            response = os.popen(f'{command} {host} {arg}').read()
            print(f"Ping response for {host}:\n{response}")
        except Exception as e:
            response = "Problem connecting"
            color = "red"
        else:
            # setting background color to green/red to show connected or not
            color = "green" if "time" in response else "red"
            
            # Use regex to extract the latency value
            match = re.search(r'time=([\d\.]+)', response)
            if match:
                try:
                    latency = float(match.group(1))
                except ValueError:
                    latency = None
            else:
                latency = None
            
            if latency is not None:
                if latency < latency_quality['good']:
                    latency_color = "lightgreen"
                elif latency <= latency_quality['usable']:
                    latency_color = "yellow"
                elif latency <= latency_quality['bad']:
                    latency_color = "orange"
                else:
                    latency_color = "red"
            else:
                latency_color = "purple"
                
        if response == "":
            response = "Host could not resolve"

        body += f'''
                <h1 style="background-color:{color};">{host}</h1>
                <pre style="background-color:{latency_color}">{response}</pre>
                '''
    header = '<meta http-equiv="refresh" content="5">'
    page = f'''
            {header}
            {body}
            '''
    return page

run(host="127.0.0.1", port=8080)
