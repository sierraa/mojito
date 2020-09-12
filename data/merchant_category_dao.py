import boto3

class MerchantCategoryDao:
    
    def __init__(self, access_key_id, secret_access_key, table_name="merchant_category"):
        self.dynamodb = boto3.resource('dynamodb', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
        self.table = self.dynamodb.Table(table_name)

    def put_item(self, name, category, website):
        is_recurring = self.is_recurring(name)
        self.table.put_item(Item={
            "name": name,
            "category": category,
            "recurring": is_recurring
        })

    def get_item(self, name):
        response = self.table.get_item(Key={
            "name": name
        })
        return response["Item"]

    def update_category(self, name, category):
        self.table.update_item(Key={
            "name": name
            },
            UpdateExpression='SET category = :val',
            ExpressionAttributeValues={
                'val': category
            })

    def is_recurring(name):
        # TODO: this should probably live in a database
        # TODO: definitely need more names 
        return name in ["Spotify", "Netflix", "Hulu", "Winc"]
