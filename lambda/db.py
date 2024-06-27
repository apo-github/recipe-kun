import json
import boto3
# 使用するDynamoDBテーブルを取得します
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EscapeGameDB')
# ハンドラを定義します
def lambda_handler(event, context):
# DynamoDBのパーティションキーを指定する値をeventから受け取ります
    ID = event['ID']
# イベントから受け取った値をもとにDynamoDBテーブルの項目を指定し、取得します
    response = table.get_item(
        Key={
            'ID':ID
        }
    )
    item = response['Item']
    print(item['Situation'])
    name = 'name'
# DynamoDBテーブルからから取得した項目をウェブページに返します
    return {
        'statusCode': 200,
        'body': item
    }    
}