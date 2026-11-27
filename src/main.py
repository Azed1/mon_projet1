import subprocess


def addition(a, b):
    return a + b


def lister(dossier):
    subprocess.run(["ls", dossier])
