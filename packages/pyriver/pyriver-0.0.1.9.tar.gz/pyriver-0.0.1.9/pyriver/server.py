from pyriver.api import create_app


app = create_app()


def run_server():
    app.debug = True
    app.run(host="0.0.0.0", port=9876)


if __name__ == "__main__":
    run_server()
