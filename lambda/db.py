'''
{
	"familyId": 0,
    "initialSettings": {
        "familyAges": [
            35,
            32,
            7
        ]
    }
}


'''


import boto3

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')

    #getItemメソッドの呼び出し(主キー検索)
    response = table.get_item(
        #パラメーターとして主キー情報(辞書型)を渡す
        #Keyという変数名?は固定(違う名前だとエラーになる)
        Key={
            'familyId': 0
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



