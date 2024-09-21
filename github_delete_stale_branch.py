# File name: github_delete_stale_branch.py
# Autor: Lucas Mechler Fernandes
# Date of creation: 31/07/2023

# Description:
# Code made to delete merged or stale branches with a time period entered by the user

import csv
from github import Github
from datetime import datetime, timedelta
import subprocess
import time

# Authentication is defined via github.Auth
from github import Auth

# Using an access token
auth = Auth.Token("")

# Public Web Github
g = Github(auth=auth)

# Put the owner of the branch here
owner = ""

# Put the name of the repository you want to clean
repository = [""]

# Here put the list of branches you want to avoid being deleted
avoid_branches = ["master","develop","rc"]

# Fill in the number of days of inactivity
inactivity_days = 60

def main():

    subprocess.call('clear', shell=True)

    lista_teste = []

    # Calculates current date and inactivity threshold
    current_date = datetime.now()
    inactivity_limit_date = current_date - timedelta(days=inactivity_days)

    print(f"\nDate limit of inactivity: {inactivity_limit_date.date()}\n")

    # Loop to gather repositories
    for repo in g.get_user().get_repos():
        #If to filter the owner and repository
        if repo.owner.login == owner and repo.name in repository:
            print(f"Repository: {repo.name}\n")
            if not repo.archived:
                count_marked = 0
                
                branches_list = list(repo.get_branches())
                count_all = len(branches_list)
                branches_marked_deletion = []
                main_branch = repo.get_branch("master")

                print("-" *30)
                print("Branches on repository\n")

                # Loop to run through the branches
                for branch in branches_list:
                    # If to filter the branches em discart the avoid_list branches
                    if branch.name not in avoid_branches:

                        commits = repo.get_commits(sha=branch.commit.sha)
                        last_commit = commits[0]

                        last_commit = repo.get_commit(sha=branch.commit.sha)
                        last_commit_date = last_commit.commit.author.date
                        
                        is_stale = last_commit_date < main_branch.commit.commit.author.date
                        is_merged = branch.commit.sha == repo.get_branch(branch.name).commit.sha

                        #Filter to make the list of marked branches                        
                        if is_merged and last_commit_date < inactivity_limit_date:
                            print("MARKED FOR DELETION")
                            print(f"Branch: {branch.name}")
                            print(f"Last activity: {last_commit_date}")
                            print(f"Merged branch with {(current_date - last_commit_date).days} days of inactivity\n")
                            branches_marked_deletion.append(branch)
                            count_marked += 1
                        
                        elif is_stale and last_commit_date < inactivity_limit_date:
                            print("MARKED FOR DELETION")
                            print(f"Branch: {branch.name}")
                            print(f"Last activity: {last_commit_date}")
                            print(f"Stale branch with {(current_date - last_commit_date).days} days of inactivity\n")
                            branches_marked_deletion.append(branch)
                            count_marked += 1
                        else:
                            print("PRESERVED")
                            print(f"Branch: {branch.name}")
                            print(f"Last activity: {last_commit_date}")
                            print(f"{(current_date - last_commit_date).days} days of inactivity\n")

                    else:
                        print("PRESERVED - On avoid list")
                        print(f"Branch: {branch.name}\n")
                    
                    time.sleep(3) # Sleep for 3 seconds

                print("-" *30)
                print("\n")

                print("*" *30)

                if count_marked > 0:

                    # Loop to run through the marked branches
                    for branch in branches_marked_deletion:
                        commits = repo.get_commits(sha=branch.commit.sha)
                        last_commit = commits[0]

                        last_commit = repo.get_commit(sha=branch.commit.sha)
                        last_commit_date = last_commit.commit.author.date

                        print("MARKED FOR DELETION")
                        print(f"Branch: {branch.name}")
                        print(f"Last activity: {last_commit_date}")
                        print(f"Merged branch with {(current_date - last_commit_date).days} days of inactivity\n")
                    
                    print(f"{count_marked} of {count_all} branches marked for deletion on {repo.name}")

                    print("*" *30)

                    # Get the user confirmation for deletion
                    choice = input(f"Sure you want to delete these marked branches on {repo.name}? (Y/N): ")

                    if choice.lower() == 'y':
                        # Deletion of marked branches
                        for branch in branches_marked_deletion:
                            delete_branch(branch.name, repo)
                    else:
                        print(f"Nothin on'{repo.name}' deleted.")

                    print(f"\nDeleted {count_marked} branches\n\n")
                
                else:
                    print(f"No stale branches found on {repo.name}")

                print("@"*50)
                print("\n")

            else:
                print(f"{repo.name} is archived\n")
            print("~"*50)
            print("\n")
# end main
            
# Deletion function
def delete_branch(branch, repo):
    
    ref = repo.get_git_ref(f"heads/{branch}")
    ref.delete()

    print(f"Deleted: {branch}")

    time.sleep(3) # Sleep for 3 seconds


if __name__ == "__main__":
    main()
