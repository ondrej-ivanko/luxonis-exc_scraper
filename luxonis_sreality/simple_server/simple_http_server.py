import os
import sys
import socketserver
from http.server import SimpleHTTPRequestHandler
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.absolute().__str__())

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from luxonis_sreality.db_engine import engine


PORT = 8000


class SimpleAparmentHandler(SimpleHTTPRequestHandler):
    def _set_response(self, code=200):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def close_sess(self, db_session):
        db_session.close()
        engine.dispose()

    def create_content(self):
        Session = sessionmaker(bind=engine)
        db_session = Session()
        data = db_session.execute(text("select title, img_url from apartments_sale"))

        try:
            rows_to_html = ""
            for row in data:
                rows_to_html += f"""
                    <tr>
                      <td>{row[0]}</td>
                      <td>  |  </td>
                      <td>{row[1]}</td>
                    </tr>"""
            html = f"""<!DOCTYPE html>
            <html>
              <meta charset="UTF-8">
              <head>
                <title>Apartments for Sale</title>
              </head>

              <body>
                 <table>
                    <tr>
                      <th>Title</th>
                      <th>  |  </th>
                      <th>Image Url</th>
                    </tr>
                        {rows_to_html}
                  </table>
              </body>
            </html>"""
            with open("index.html", "w") as f:
                f.write(html)

        except Exception as e:
            sys.stderr.write(str(e))
            raise
        finally:
            self.close_sess(db_session)

    def do_GET(self):
        self.create_content()
        super().do_GET()


def run():
    with socketserver.TCPServer(
        (os.getenv("HOST", "127.0.0.1"), PORT),
        RequestHandlerClass=SimpleAparmentHandler,
    ) as httpd:
        print("serving at port", PORT)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("stoping server...")
        finally:
            httpd.shutdown()


if __name__ == "__main__":
    run()
