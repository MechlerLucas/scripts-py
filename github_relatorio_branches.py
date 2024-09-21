import csv
from github import Github
from datetime import datetime, timedelta

# Authentication is defined via github.Auth
from github import Auth

# using an access token
auth = Auth.Token("")

# Public Web Github
g = Github(auth=auth)

# Calculates current date and inactivity threshold (60 days ago)
current_date = datetime.now()
inactivity_limit_date = current_date - timedelta(days=60)

# CSV file name
csv_file_name = "report_stale_merged_branches.csv"

# Opens the CSV file in write mode and writes the data
with open(csv_file_name, mode="w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(["Owner;Repository;Branch;Last Commit Author;Last Commit Date;Inactive Days"])

    for repo in g.get_user().get_repos():

        if repo.owner.login == "asaplog":
            main_branch = repo.get_branch("master")
            count = 0

            branches_list = list(repo.get_branches())

            # Lists branches that are stale, already merged, and have been inactive for more than 60 days, excluding master and rc
            for branch in branches_list:
                if (branch.name != "master") and (branch.name != "rc") and (branch.name != "develop"):

                    # Gets the list of commits associated with the branch
                    commits = repo.get_commits(sha=branch.commit.sha)
                    last_commit = commits[0]
                    last_commit_author = last_commit.commit.author.name

                    last_commit = repo.get_commit(sha=branch.commit.sha)
                    last_commit_date = last_commit.commit.author.date
                    
                    is_stale = last_commit_date < main_branch.commit.commit.author.date
                    is_merged = branch.commit.sha == repo.get_branch(branch.name).commit.sha
                    
                    if is_merged and last_commit_date < inactivity_limit_date:
                        csv_writer.writerow([repo.owner.login, repo.name, main_branch.name, last_commit_author, last_commit_date, (current_date - last_commit_date).days])                        
                        count += 1
                    
                    elif is_stale and last_commit_date < inactivity_limit_date:
                        csv_writer.writerow([repo.owner.login, repo.name, main_branch.name, last_commit_author, last_commit_date, (current_date - last_commit_date).days])                        
                        count += 1
            
            csv_writer.writerow([repo.name, f"Filtered branches: {count}"])

