#!/usr/bin/env python
"""
Very simple HTTP server in python (Updated for Python 3.7)

Usage:

    ./dummy-web-server.py -h
    ./dummy-web-server.py -l localhost -p 8000

Send a GET request:

    curl http://localhost:8000

Send a HEAD request:

    curl -I http://localhost:8000

Send a POST request:

    curl -d "foo=bar&bin=baz" http://localhost:8000

This code is available for use under the MIT license.

----

Copyright 2021 Brad Montgomery

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.    

"""
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3
import json
import base64
from datetime import datetime

DATABASE_NAME = 'database/project10a.db'


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        pass

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.

        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self.send_response(200)

        # connect to database
        con = sqlite3.connect(f'{DATABASE_NAME}')
        cur = con.cursor()

        # if path is empty
        if self.path == '/':
            self.send_header("Content-type", "text/json")
            self.end_headers()
            # get last 5 events
            cur.execute("""
                SELECT id, timestamp
                FROM past_events
                ORDER BY timestamp desc
                LIMIT 5;
                """)
            results = cur.fetchall()

            # close database connection
            con.commit()
            con.close()

            # convert result to json
            json_format = []
            for row in results:
                newrow = {
                    'id': row[0],
                    'timestamp': row[1]}
                json_format.append(newrow)
            json_ = json.dumps(json_format, indent=2)

            # send the result
            self.wfile.write(json_.encode('utf8'))

        # if the path is not empty
        else:
            self.send_header("Content-type", "image/jpg")
            self.end_headers()
            event_id = self.path.split('/')[1]
            # get photo using id
            cur.execute("""
                SELECT photo
                FROM past_events
                WHERE id = ?
                LIMIT 5;
                """, (event_id,))
            result = cur.fetchone()

            # close database connection
            con.commit()
            con.close()
            self.wfile.write(result[0])

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        print('post ' + self.path)
        # get post body
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        # insert post body into database
        con = sqlite3.connect(f'{DATABASE_NAME}')
        cur = con.cursor()
        cur.execute("""
            INSERT INTO past_events (timestamp, photo)
            VALUES (?, ?);
            """, (self.path.split('/')[1], post_data))

        # close database connection
        con.commit()
        con.close()

        self.wfile.write(self._html("POST!"))


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)

