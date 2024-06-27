import json
import boto3
import os

# Bedrockクライアントの設定
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-west-2'  # 適切なリージョンに変更してください
)

def lambda_handler(event, context):
    # 入力テキストの取得
    # sqs。
    input_text = event.get('input_text', '')
    print(input_text)
    if not input_text:
        return {
            'statusCode': 400,
            'body': json.dumps('入力テキストが必要です。')
        }
    
    # Claude 3 Haikuへのリクエストボディの作成
    # 
    input_text = "会話しましょう"
    output_sentence = send_llm(input_text)
    try:
        # print(111111111)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'generated_text': output_sentence
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'エラーが発生しました: {str(e)}')
        }

def send_llm(sentence):
    request_body = {
         "anthropic_version": "bedrock-2023-05-31",
        "messages":[
            {
                "role":"user",
                "content":[{
                    "type":"text",
                    "text":sentence
                }]
            }
        ],
        "max_tokens": 500,
    }
    # Bedrockを使用してClaude 3 Haikuにリクエストを送信
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-haiku-20240307-v1:0',  # Claude 3 HaikuのモデルID
        body=json.dumps(request_body)
    )
    # レスポンスの解析
    response_body = json.loads(response['body'].read())
    generated_text = response_body["content"][0]["text"]
    return generated_text


# client = boto3.client('lambda')
# def send_data(data):
#     response = client.invoke(
#         FunctionName='children',#Lambdaで記載している関数名を記載
#         InvocationType='Event',
#         Payload=json.dumps({'data':data})
#     )