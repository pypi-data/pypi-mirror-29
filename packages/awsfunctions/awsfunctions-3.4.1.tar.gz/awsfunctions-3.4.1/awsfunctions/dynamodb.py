from typing import Dict, Optional

import boto3


class DynamoDBTable:
    def __init__(self, table_name: str) -> None:
        self.resource = boto3.resource('dynamodb')
        self.table = self.resource.Table(table_name)

    def put_item(self, item: Dict) -> bool:
        """
        Puts an item into the table
        :param item: Must contain the complete key as defined in schema
        :return: True if the item was successfully added, False otherwise
        """
        response = self.table.put_item(Item=item)

        return response.get('ResponseMetadata', {}).get('HTTPStatusCode',
                                                        -1) == 200

    def get_item(self, key: Dict) -> Optional[Dict]:
        """
        Gets an item from the table by Key
        :param key: Must contain the complete key as defined in table schema
        :return: Item dictionary if the item was successfully retrieved, empty dictionary otherwise
        """
        response = self.table.get_item(Key=key)

        return response.get('Item', None)
