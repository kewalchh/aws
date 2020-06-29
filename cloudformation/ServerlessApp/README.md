Project: Deploy Serverless REST API on AWS using CloudFormation (Infrastructure as Code)
AWS Services: API Gateway, Lambda Function, DynamoDB

Steps for the deployment:

1. Checkout the Serverless App dir
2. Create S3 bucket and upload the Lambda functions 

s3bucket=<Your unique S3 bucket name>
aws s3 mb s3://${s3bucket}

zip -j -D GetProductCatalogApiFunction.zip GetProductCatalogApiFunction/lambda_function.py && aws s3 cp GetProductCatalogApiFunction.zip s3://${s3bucket}
zip -j -D PostProductCatalogApiFunction.zip PostProductCatalogApiFunction/lambda_function.py && aws s3 cp PostProductCatalogApiFunction.zip s3://${s3bucket}

3. Create CloudFormation Stack

aws cloudformation validate-template --template-body file://ServerLessRestApi.yml

aws cloudformation create-stack --stack-name product-catalog-rest-api --template-body file://ServerLessRestApi.yml --parameters ParameterKey=S3BucketLambdaCode,ParameterValue=${s3bucket} --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM" 

aws cloudformation wait stack-create-complete --stack-name product-catalog-rest-api

4. List all objects:

aws cloudformation list-stack-resources --stack-name product-catalog-rest-api
aws cloudformation describe-stack-resources --stack-name product-catalog-rest-api

5. Load sample data to sample data to DynamoDB

aws dynamodb batch-write-item --request-items file://ProductCatalog.json

6. Test the api using curl command

GET:
curl -v https://{uri}/Dev/product?productId=102

POST:
curl -d '{"Id":104, "Title":"Book 104 Title", "Price":200, "ProductCategory":"Book"}' -H 'Content-Type: application/json' https://{uri}/Dev/product