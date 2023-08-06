import subprocess
from pyriver.services import stream_service


def execute(args):
    schema = stream_service.get_river_json()
    name = schema["metadata"]["name"].replace(" ", "-").lower()
    repository = schema["metadata"].get("repository", "localhost:5000")
    user = schema["metadata"].get("user")
    imagename = "%s/%s/%s" % (repository, user, name)
    subprocess.call(["docker", "build", ".", "--file", ".river/Dockerfile", "--tag", imagename])
