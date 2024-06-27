'''
{
    "familyId": 0,
    "initialSettings": {
        "familyAges": [
            35,
            32,
            7
        ],
        "cookingSkill": 5,
        "allergies": [
            "soy"
        ]
    },
    "preferences": {
        "ingredients": {
            "carrot": 10,
            "onion": 8,
            "potato": 7
        },
        "dishes": {
            "curry": 10,
            "hamburger": 9,
            "salad": 6
        }
    }
}
{
    num_day:5,
    family_id:0
    }


'''
import boto3
import json

def lambda_handler(event, context):

    # print(num_data, type(num_data))
    # print(num_data)
    family_id = event['family_id']
    item = get_data(family_id=family_id)
    print(item)
    sentence = "会話しましょう"
    # sentence = generate_prompt(item, event)
    output_sentence = send_llm(sentence)
    return {
        'statusCode': 200,
        'body': json.dumps({
            'generated_text': output_sentence
        })
    }

def generate_prompt(item, event):
    # family_id = event['family_id']
    num_day = event['num_day']
    family_lst = item['initialSettings']['familyAges']
    allergies = item['initialSettings']['allergies']
    ingredients = item['preferences']['ingredients']
    dishes = item['preferences']['dishes']
    
    prompt = "あなたは経験豊富な栄養士兼料理専門家です。以下の条件に従って、5日分の朝昼晩の献立を作成してください。\n"
    family_info_sentence = ""
    for i, age in enumerate(family_lst):
        adult = "大人" if age >= 20 else "子供"
        family_info_sentence += f"-{age}歳 ({adult})\n"
    
    ingredients_sentence = ""
    for ingredient, amount in ingredients.items():
        ingredients_sentence += f"-{ingredient} {amount}g\n"
    
    
    
    
    
    
    
def get_data(family_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')

    #getItemメソッドの呼び出し(主キー検索)
    response = table.get_item(
        #パラメーターとして主キー情報(辞書型)を渡す
        #Keyという変数名?は固定(違う名前だとエラーになる)
        Key={
            'familyId': family_id
        }
    )
    #responseの正体は、Itemなどのキーが定義された辞書型オブジェクト
    # print(response)

    #結果の取得
    item = response['Item']

    #辞書型オブジェクトとして取得できる(テーブルのカラムが定義されている)
    #キーに一致するものがない場合、エラーとなる
    print("返す値")
    print(item)

    return item

def send_llm(sentence):
    bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-west-2'  # 適切なリージョンに変更してください
)

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
    print(f"response: {response}")
    # レスポンスの解析
    response_body = json.loads(response['body'].read())
    print(f"response_body: {response_body}")
    generated_text = response_body["content"][0]["text"]
    return generated_text