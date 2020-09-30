import boto3
import uuid

class TransactionDao:
    
    def __init__(self, access_key_id, secret_access_key, table_name="transactions"):
        self.dynamodb = boto3.resource('dynamodb', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
        self.table = self.dynamodb.Table(table_name)
        self.merchant_dao = MerchantDao(access_key_id, secret_access_key)

    def put_item(self, transaction_date, amount, merchant, category, website, user):
        # This allows me to define custom categories 
        category = self.get_merchant_category_if_exists(merchant, category, website)
        self.table.put_item(Item={
            "uuid": uuid.uuid4(),
            "date": transaction_date,
            "amount": amount,
            "user": user,
            "merchant": merchant,
            "category": category
        })

    def get_merchant_category_if_exists(self, merchant, category, website):
        item = self.merchant_dao.get_item(merchant)
        if item is None:
            self.merchant_dao.put_item(merchant, category, website)
            return category
        else:
            return item.category

