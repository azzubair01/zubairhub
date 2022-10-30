### 1) Uploading code to GCP
gcloud builds submit --tag gcr.io/airasia-adedashboard-stg/ade-reporting-app  --project=airasia-adedashboard-stg

### 2) Deployment & running code on GCP
gcloud run deploy --image gcr.io/airasia-adedashboard-stg/ade-reporting-app  --platform managed  --project=airasia-adedashboard-stg --allow-unauthenticated