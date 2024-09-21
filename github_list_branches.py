import csv
from github import Github
from datetime import datetime, timedelta

# Authentication is defined via github.Auth
from github import Auth

# Put the access token
auth = Auth.Token("")

# Public Web Github
g = Github(auth=auth)

# Put the name of the owner
owner = ""

# Name of the CSV
nome_arquivo_csv = ""

# Abre o arquivo CSV em modo de escrita e escreve os dados
with open(nome_arquivo_csv, mode="w", newline="") as arquivo_csv:
    escritor_csv = csv.writer(arquivo_csv)

    escritor_csv.writerow(["Repository;Branches in total"])

    for repo in g.get_user().get_repos():

        if repo.owner.login == owner:
            main_branch = repo.get_branch("master")

            branches_list = list(repo.get_branches())
            branches_cout = len(branches_list)
            
            escritor_csv.writerow([repo.name,branches_cout])
