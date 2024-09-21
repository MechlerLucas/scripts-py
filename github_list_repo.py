import csv
from github import Github
from datetime import datetime, timedelta

# Authentication is defined via github.Auth
from github import Auth

# using an access token
auth = Auth.Token("")

# Public Web Github
g = Github(auth=auth)

# Name of the CSV
archive_name_csv = ""

# Abre o arquivo CSV em modo de escrita e escreve os dados
with open(archive_name_csv, mode="w", newline="") as archive_csv:
    escritor_csv = csv.writer(archive_csv)

    escritor_csv.writerow(["Owner;Repository"])

    for repo in g.get_user().get_repos():
        
        escritor_csv.writerow([repo.owner.login,repo.name])