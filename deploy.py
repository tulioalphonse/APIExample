import sys
import argparse
import subprocess
import random
import string
import shlex


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--namespace", dest="namespace", required=True)
    namespace = vars(parser.parse_args())['namespace']

    password = ''.join(random.choice(string.ascii_lowercase) for i in range(10))

    print("Building APIExample image on minikube")
    subprocess.call(shlex.split("./build_on_minikube.sh"))

    print("Creating ns={}".format(namespace))
    subprocess.call(shlex.split("kubectl create ns {}".format(namespace)))

    print("Deploying secret for mysql")
    subprocess.call(shlex.split("kubectl create secret generic mysql-credentials "
                                "--from-literal=root-password='{}' "
                                "-n {}".format(password, namespace)))

    print("Deploying mysql")
    subprocess.call(shlex.split("kubectl apply -f k8s/mysql.yaml "
                                "-n{}".format(namespace)))

    print("Generating config file to deploy APIExample")
    subprocess.call(shlex.split("python src/resources/configCreator.py "
                                "--outputPath \"/tmp/conf/\" "
                                "--host \"mysql.{}\" "
                                "--user \"root\" "
                                "--password \"{}\" "
                                "--db \"APIExample\"".format(namespace, password)))

    password = None

    print("Deploying ConfigMap")
    subprocess.call(shlex.split("kubectl create configmap api-config "
                                "--from-file=/tmp/conf/config.toml "
                                "-n{}".format(namespace)))

    print("Deploying APIExample")
    subprocess.call(shlex.split("kubectl apply -f k8s/apiexample.yaml "
                                "-n{}".format(namespace)))

    print("\n\n------------------------DONE------------------------\n\n")
    print("Please execute:\nkubectl port-forward svc/apiexample 5000 -n{}".format(namespace))
    print("After that just send requests to localhost:5000")
    print("\n\n----------------------------------------------------\n\n")


if __name__ == "__main__":
    main(sys.argv[1:])


