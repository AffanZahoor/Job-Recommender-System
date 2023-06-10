import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

companies = pd.read_csv("naukri_data_science_jobs_india.csv")
applicants = pd.read_csv("applicants.csv")

# data retrieval

required_skills = []
col5c = companies['Skills/Description']
for i in col5c:
    required_skills.append([i])

for i in range(0, len(companies)):
    required_skills[i] = required_skills[i][0].split(", ")
    required_skills[i] = [string.lower() for string in required_skills[i]]

#print(required_skills[100])

required_location = []
col4c = companies['Location']
for i in col4c:
    required_location.append([i])

for i in range(0, len(companies)):
    required_location[i] = required_location[i][0].split(", ")
    required_location[i] = [string.lower() for string in required_location[i]]

#print(required_location[100])

company_name = []
col3c = companies['Company']
for i in col3c:
    company_name.append([i])

for i in range(0, len(companies)):
    company_name[i] = [string.lower() for string in company_name[i]]
#print(company_name[100])

job_role = []
col2c = companies['Job_Role']
for i in col2c:
    job_role.append([i])

for i in range(0, len(companies)):
    job_role[i] = [string.lower() for string in job_role[i]]
#print(job_role[100])

comid = []
col1c = companies['id']
for i in col1c:
    comid.append(i)
#print(comid[100])

#print('\n')

skills = []
col5a = applicants['skills']
for i in col5a:
    skills.append([i])

for i in range(0, len(applicants)):
    skills[i] = skills[i][0].split(", ")
    skills[i] = [string.lower() for string in skills[i]]

#print(skills[1])

current_job = []
col4a = applicants['current_job_id']
for i in col4a:
    current_job.append(i)
#print(current_job[1])

desired_location = []
col3a = applicants['Desired location']
for i in col3a:
    desired_location.append([i])
for i in range(0, len(applicants)):
    desired_location[i] = [string.lower() for string in desired_location[i]]
#print(desired_location[1])

appname = []
col2a = applicants['applicants']
for i in col2a:
    appname.append([i])
for i in range(0, len(applicants)):
    appname[i] = [string.lower() for string in appname[i]]
#print(appname[1])

appid = []
col1a = applicants['id']
for i in col1a:
    appid.append(i)
#print(appid[1])

# recommender system

# collaborative item based
all_skillsreq = set(skillreq for skillsreq in required_skills for skillreq in skillsreq)
data = {}
for i, skillsreq in enumerate(required_skills):
    data[comid[i]] = {skillreq: int(skillreq in skillsreq) for skillreq in all_skillsreq}
df1 = pd.DataFrame.from_dict(data, orient='index')

#print(df1.head(10))

# calculate the item similarities
cos_sim = cosine_similarity(df1)

def get_similar_rows(row_id, df1, cos_sim,no_of_sim):
    row_index = row_id - 1
    row_similarities = cos_sim[row_index]
    most_similar_rows = np.argsort(row_similarities)[::-1][1:(no_of_sim+1)] + 1
    return most_similar_rows

# appidforsim = 25
# appjobforsim=current_job[appidforsim-1]
# similar_companies = get_similar_rows(appjobforsim, df1, cos_sim,40)

# print("similar companies for ", appname[appidforsim-1][0]," ID =",appidforsim, " city =",desired_location[appidforsim-1][0])
# print("\n")
#
# for i in similar_companies:
#     if desired_location[appidforsim-1][0] in required_location[i-1]:
#         print("ID =",i,"  Company Name = ", company_name[i-1][0], "  city =",required_location[i-1])

# for i in similar_companies:
#     print("ID =",i,"  Company Name = ", company_name[i-1][0], "  city =",required_location[i-1])



# collaborative user based
all_skillsapp = set(skillapp for skillsapp in skills for skillapp in skillsapp)
data2 = {}
for i, skillsapp in enumerate(skills):
    data2[appid[i]] = {skillapp: int(skillapp in skillsapp) for skillapp in all_skillsapp}
df2 = pd.DataFrame.from_dict(data2, orient='index')


# calculate the item similarities
cos_sim2 = cosine_similarity(df2)

appidforsim = 100
if(current_job[appidforsim-1]==0):
    similar_users = get_similar_rows(appidforsim, df2, cos_sim2,1)

    print("similar Users for ", appname[appidforsim-1][0]," ID =",appidforsim, " city =",desired_location[appidforsim-1][0])
    print("\n")

    # for i in similar_companies:
    #     if desired_location[appidforsim-1][0] in required_location[i-1]:
    #         print("ID =",i,"  Company Name = ", company_name[i-1][0], "  city =",required_location[i-1])

    for i in similar_users:
        print("ID =",i,"  Applicant Name = ", appname[i-1][0], "  Company Name = ", company_name[current_job[i-1]][0], "  city =",desired_location[i-1][0])

    #hybrid collaborative filtering

    appidforsim2 = similar_users[0]
    appjobforsim2=current_job[appidforsim-1]
    similar_companies = get_similar_rows(appjobforsim2, df1, cos_sim,100)

    print("Recommended companies for ", appname[appidforsim-1][0]," ID =",appidforsim, " city =",desired_location[appidforsim-1][0])
    print("\n")

    j=0
    limit=10
    print ("{:<8} {:<60} {:<50} {:<40}".format('ID','Job Role','Company Name','City'))
    for i in similar_companies:
        if desired_location[appidforsim-1][0] in required_location[i-1]:
            print("{:<8} {:<60} {:<50} {:<40}".format(i, job_role[i-1][0], company_name[i-1][0],col4c[i-1]))
            if j == limit:
                break
            j = j + 1

    for i in similar_companies:
        if desired_location[appidforsim - 1][0] in required_location[i - 1]:
            print("",end="")
        else:
            print("{:<8} {:<60} {:<50} {:<40}".format(i, job_role[i-1][0], company_name[i-1][0],col4c[i-1]))
            if j == limit:
                break
            j = j + 1
else:
    appjobforsim=current_job[appidforsim-1]
    similar_companies = get_similar_rows(appjobforsim, df1, cos_sim, 100)

    print("Recommended companies for ", appname[appidforsim - 1][0], " ID =", appidforsim, " city =",
          desired_location[appidforsim - 1][0])
    print("\n")

    j = 0
    limit = 10
    print("{:<8} {:<60} {:<50} {:<40}".format('ID', 'Job Role', 'Company Name', 'City'))
    for i in similar_companies:
        if desired_location[appidforsim - 1][0] in required_location[i - 1]:
            print("{:<8} {:<60} {:<50} {:<40}".format(i, job_role[i - 1][0], company_name[i - 1][0], col4c[i - 1]))
            if j == limit:
                break
            j = j + 1

    for i in similar_companies:
        if desired_location[appidforsim - 1][0] in required_location[i - 1]:
            print("", end="")
        else:
            print("{:<8} {:<60} {:<50} {:<40}".format(i, job_role[i - 1][0], company_name[i - 1][0], col4c[i - 1]))
            if j == limit:
                break
            j = j + 1