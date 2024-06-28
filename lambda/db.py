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
    event = json.loads(event['body'])
    family_id = event['family_id']
    print(f"family_id: {family_id}")
    item = get_data(family_id=family_id)
    print(item)
    sentence = "会話しましょう"
    sentence = generate_prompt(item, event)
    output_sentence = send_llm(sentence)
    print("-"*10)
    print(f"{type(output_sentence)=}")
    print(output_sentence)
    print("ここまでがoutputsentence")
    output_sentence = json.loads(output_sentence)
    print("ssssssssssssss")
    print(output_sentence)
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
    
    family_info_sentence = ""
    for i, age in enumerate(family_lst):
        adult = "大人" if age >= 20 else "子供"
        family_info_sentence += f"-{age}歳 ({adult})\n"
    
    ingredients_sentence = ""
    for ingredient, score in ingredients.items():
        ingredients_sentence += f"-{ingredient} ({score})\n"
    dish_sentence = ""
    for dish, score in dishes.items():
        dish_sentence += f"-{dish} ({score})\n"
    allergies_sentence = ""
    for allergy in allergies:
        allergies_sentence += f"-{allergy} (完全除去)\n"
        
    
    prompt = "あなたは経験豊富な栄養士兼料理専門家です。以下の条件に従って、5日分の朝昼晩の献立を作成してください。\n"
    prompt += f"家族構成\n{family_info_sentence}\n\n"
    prompt += f"好み：()内は嗜好度を表す0-10のスケール（10が最も好き、0が最も嫌い）\n"
    prompt += f"食材\n{ingredients_sentence}\n"
    prompt += f"料理\n{dish_sentence}\n\n"
    prompt += f"アレルギー\n{allergies_sentence}\n\n"
    prompt += """献立作成の条件：
1. 栄養バランスを考慮し、各食事で主食、主菜、副菜を含める
2. 年齢に応じた適切なカロリーと栄養素を提供
3. 嗜好度を考慮し、高スコアの食べ物を優先的に取り入れる（週に2-3回）
4. 低スコアの食べ物は避けるか、代替案や工夫を提案する
5. アレルギー食材は完全に除去し、制限のある食材は指定量以下に抑える
6. 平日の朝食と夕食は30分以内、昼食は15分以内で調理可能な献立にする
7. 食材の無駄を減らすため、週を通して食材を効率的に使用する
8. 季節性を考慮し、旬の食材を積極的に取り入れる
9. 週に1回は新しい料理や食材を試す「チャレンジデー」を設ける
10. 子供の成長に必要な栄養素を意識的に取り入れる

予算：
- 1日あたりの食費：3000円以内
- 週間食費：15000円以内

各食事について以下の情報を提供してください：
- 料理名
- 概算費用（1人あたり）
- 概算カロリー（1人あたり）

追加指示：
1. 各日の終わりに、その日の総コスト、総カロリー、総炭水化物量を記載してください。
2. 週間の総コストを最後に記載してください。
3. 特定の料理に対して、アレルギー対応や低糖質版の代替案がある場合は、コメントとして追加してください。
4. 栄養バランスや嗜好度を考慮しつつ、できるだけ多様な料理を提案してください。
5. 献立に使用する主な食材リストを週の最後に追加してください。

出力形式：
以下のJSON形式で出力してください。下記のjson形式以外で絶対に出力しないでください。それ以外の形式で出力したらペナルティを与えます。

{
  "day1": {
    "breakfast": {
      "meal": "料理名",
      "cost(yen)": "○○○",
      "calories(kcal)": "○○○"
    },
    "lunch": { ... },
    "dinner": { ... },
    "dailyTotal": {
      "cost": "○○○○",
      "calories(kcal)": "○○○○",
    }
  },
  "day2": { ... },
  ...

}
    """
    return prompt
    
    
    
    
    
    
    
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
    print(f"response: {response}")

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
        "max_tokens":10000,
    }
    # Bedrockを使用してClaude 3 Haikuにリクエストを送信
    response = bedrock.invoke_model(
        # modelId='anthropic.claude-3-haiku-20240307-v1:0',  # Claude 3 HaikuのモデルID
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',  # Claude 3 HaikuのモデルID
        body=json.dumps(request_body)
    )
    print(77777)
    print(f"response: {response}")
    print(9999)
    # レスポンスの解析
    response_body = json.loads(response['body'].read())
    print(f"response_body: {response_body}")
    generated_text = response_body["content"][0]["text"]
    return generated_text