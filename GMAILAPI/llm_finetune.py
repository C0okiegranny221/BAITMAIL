import boto3
import json
import time

def submit_scams_finetuning_job(
    base_model_id: str,
    s3_train_uri: str,
    s3_valid_uri: str,
    output_s3_uri: str,
    role_arn: str,
    job_name: str,
    custom_model_name: str,
    hyperparameters: dict = None
):
    """
    Submits a Bedrock model customization job (fine-tuning) for scam classification.

    Args:
      base_model_id: ID of the base model (foundation model) you want to customize.
      s3_train_uri: S3 URI for your training JSONL file (e.g. "s3://bucket/train.jsonl").
      s3_valid_uri: S3 URI for your validation JSONL file (optional).
      output_s3_uri: S3 URI where the fine-tuned model artifacts should be stored.
      role_arn: IAM Role ARN that Bedrock can assume (with permissions to read training data, write output, etc.)
      job_name: A unique name/ID for this fine-tuning job.
      custom_model_name: A name you choose for the custom model.
      hyperparameters: (optional) dict of hyperparameters like epochs, batchSize, learningRate.

    Returns:
      The Job ARN or identifier for the submitted job.
    """

    bedrock = boto3.client("bedrock")

    # Build the payload for creating a customization (fine-tuning) job
    params = {
        "jobName": job_name,
        "customModelName": custom_model_name,
        "roleArn": role_arn,
        "baseModelIdentifier": base_model_id,
        "customizationType": "FINE_TUNING",
        "trainingDataConfig": {
            "s3Uri": s3_train_uri
        },
        "outputDataConfig": {
            "s3Uri": output_s3_uri
        },
    }

    if s3_valid_uri:
        params["validationDataConfig"] = {
            "validators": [
                {
                    "s3Uri": s3_valid_uri
                }
            ]
        }

    if hyperparameters:
        params["hyperParameters"] = {k: str(v) for k, v in hyperparameters.items()}

    print("Submitting model customization job with params:")
    print(json.dumps(params, indent=2))

    resp = bedrock.create_model_customization_job(**params)
    job_arn = resp.get("jobArn")
    print("Submitted job ARN:", job_arn)
    return job_arn

def wait_for_job_completion(job_arn, poll_interval=60):
    """
    Polls the job until it finishes (status: SUCCEEDED or FAILED).
    """
    bedrock = boto3.client("bedrock")

    while True:
        resp = bedrock.get_model_customization_job(jobIdentifier=job_arn)
        status = resp.get("status")
        print("Job status:", status)
        if status in ("SUCCEEDED", "FAILED"):
            return resp
        time.sleep(poll_interval)

def invoke_custom_model(custom_model_id: str, prompt: str):
    """
    Calls your custom model (after it's deployed) with a prompt and returns output.
    """
    client = boto3.client("bedrock-runtime")
    body = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 256,
            "temperature": 0.0,
            "topP": 0.9
        }
    }
    resp = client.invoke_model(modelId=custom_model_id, body=json.dumps(body))
    result = json.loads(resp["body"].read())
    return result

if __name__ == "__main__":
    # Example values — replace with your real values
    BASE = "cohere.command-light-text-v14:7:4k"  # example base model
    TRAIN = "s3://my-bucket/scam_finetune/train_emails.jsonl"
    VALID = "s3://my-bucket/scam_finetune/valid_emails.jsonl"
    OUTPUT = "s3://my-bucket/scam_finetune/output/"
    ROLE_ARN = "arn:aws:iam::123456789012:role/BedrockFineTuningRole"
    JOB = "scam-email-finetuning-job"
    CUSTOM = "scam-detector-model"
    HYPERS = {"epochCount": 3, "batchSize": 8, "learningRate": 0.00001}

    job_arn = submit_scams_finetuning_job(
        base_model_id=BASE,
        s3_train_uri=TRAIN,
        s3_valid_uri=VALID,
        output_s3_uri=OUTPUT,
        role_arn=ROLE_ARN,
        job_name=JOB,
        custom_model_name=CUSTOM,
        hyperparameters=HYPERS
    )

    # Wait till job completes
    job_info = wait_for_job_completion(job_arn)
    print("Job result:", json.dumps(job_info, indent=2))

    # Once custom model ARN is known (from job_info or output), invoke it
    custom_model_id = "arn-of-your-deployed-custom-model"
    prompt = "Classify this email as SCAM or NOT_SCAM:\n\nEmail: You have won $1000, click here!"
    output = invoke_custom_model(custom_model_id, prompt)
    print("Model output:", output)
