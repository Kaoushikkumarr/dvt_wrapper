# # Below commands will be used for Deploying the code base to the Cloud Run Environment.
#
# 1. gcloud config set project <project_name>
# 2. gcloud builds submit --tag gcr.io/<project_name>/dvt-wrapper:latest .
# 3. gcloud run deploy dvt-wrapper --image gcr.io/<project_name>/dvt-wrapper:latest --platform managed --region us-east1
#     --allow-unauthenticated --service-account workload-sa@<project_name>
