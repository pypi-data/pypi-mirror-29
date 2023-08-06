import subprocess
from pyriver.services import stream_service


def execute(args):
    # TODO: this needs to be able to use any server
    # TODO: do not force deletion/recreation of deployment and service
    stream = stream_service.get_river_json()
    name = stream["metadata"]["name"].replace(" ", "-").lower()
    user = stream["metadata"].get("user")
    repository = stream["metadata"].get("repository", "localhost:5000")
    imagename = "%s/%s/%s" % (repository, user, name)
    subprocess.call(["docker", "push", imagename])
    subprocess.call(["kubectl", "delete", "deployment", name])
    subprocess.call(["kubectl", "run", name, "--image=%s" % imagename, "--port=9876"])
    subprocess.call(["kubectl", "delete", "service", name])
    subprocess.call(["kubectl", "expose", "deployment", name, "--type=LoadBalancer"])
