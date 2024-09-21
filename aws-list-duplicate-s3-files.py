# File name: aws-list-duplicate-s3-files.py
# Autor: Lucas Mechler Fernandes
# Date of creation: 31/07/2023

# Description:
# Code made to list the duplicate files inside a especified S3

import boto3
import csv

# Put the profile name of the AWS
profile_name_input = ""

# Put here the folders that you want to verify
folders = []

# Name of the bucket to be verify
bucket = ""

def save_to_csv(result, csv_writer):
    for key, versions in result.items():
        for version in versions:
            csv_writer.writerow({
                'Folder': folder,
                'Archive': key,
                'Version': version['VersionId'],
                'Date': version['LastModified']
            })

def list_files_with_multiple_versions(folder):
    objects = list_all_objects(bucket, folder)
    file_versions = {}
    for obj in objects:
        key = obj['Key']
        versions = s3.list_object_versions(Bucket=bucket, Prefix=key)['Versions']
        if len(versions) > 1:
            file_versions[key] = versions
    print(f"{len(objects)} foram verificados")
    return file_versions

def list_all_objects(bucket_name, prefix):
    objects = []
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    while True:
        contents = response.get('Contents')
        if contents:
            objects.extend(contents)
        token = response.get('NextContinuationToken')
        if not token:
            break
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, ContinuationToken=str(token))
    return objects

# Main
session = boto3.session.Session(profile_name=profile_name_input)
s3 = session.client('s3')
csv_filename = 'output.csv'

with open(csv_filename, 'w', newline='') as csvfile:
    
    fieldnames = ['Folder', 'Archive', 'Version', 'Date']
    
    csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    csv_writer.writeheader()
    for folder in folders:
        print(f"\n-------\nInside Folder {folder}\n")
        result = list_files_with_multiple_versions(folder)
        if result:
            
            save_to_csv(result, csv_writer)
            
            for key, versions in result.items():
                print(f'Archive: {key}')
                for version in versions:
                    print(f'  Version: {version["VersionId"]}, Date: {version["LastModified"]}')
                print('---')
        else:
            print("Não há versões duplicadas")

print(f'Dados foram salvos em {csv_filename}')
