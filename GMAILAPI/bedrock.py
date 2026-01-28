import boto3
import json
from dotenv import load_dotenv

load_dotenv()
bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")
model_id ="amazon.nova-pro-v1:0"
def analyze_email_with_bedrock(email_body):
    prompt = "tell me if the email is scam or not. email: " + email_body +"give me a crisp consise answer if the email is a scam write 'qwerty' as the first word "
    
    kwargs = {
        "modelId": model_id,
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "inferenceConfig": {
            "max_new_tokens": 1000
            },
            "messages": [
            {
                "role": "user",
                "content": [
                {
                    "text": prompt
                }
                ]
            }
            ]
        })
    }
    response = bedrock.invoke_model(**kwargs)
    # Parse the response
    response_body = json.loads(response["body"].read())
    #print(response_body['output']['message']['content'][0]['text'])
    return response_body['output']['message']['content'][0]['text']
#analyze_email_with_bedrock("this is a scam email")
def analyze_email_with_bedrock_scam_back(email_body):
    
    prompt = "you are interested in the offer write a email acting as if interested in the offer :" +"give me a extremely interested response."+"Don't give me any warnings or other information except the response."+"donot include parameters like rcepient name your name your contact info or your profile website just generate the proper response. "+"Talk about the empire you can make and how we can take over the world "+email_body
    
    kwargs = {
        "modelId": model_id,
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "inferenceConfig": {
            "max_new_tokens": 1000
            },
            "messages": [
            {
                "role": "user",
                "content": [
                {
                    "text": prompt
                }
                ]
            }
            ]
        })
    }
    response = bedrock.invoke_model(**kwargs)
    # Parse the response
    response_body = json.loads(response["body"].read())
    #print(response_body['output']['message']['content'][0]['text'])
    return response_body['output']['message']['content'][0]['text']