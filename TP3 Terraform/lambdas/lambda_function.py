import json
import boto3
import csv
import io

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Obtener los detalles del archivo desde el evento S3
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    # Descargar el archivo desde S3
    csv_file = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    csv_content = csv_file['Body'].read().decode('utf-8').splitlines()

    # Leer el archivo CSV
    reader = csv.DictReader(csv_content)

    # Conectar a DynamoDB
    table_name = 'optipc-csv-data-nic'
    table = dynamodb.Table(table_name)

    # Insertar cada fila del CSV en la tabla DynamoDB
    for row in reader:
        table.put_item(
            Item={
                'partType': row['partType'],
                'name': row['name'],
                'image': row['image'],
                'url': row['url'],
                'sizeType': row['sizeType'],
                'storageType': row['storageType'],
                'brand': row['brand'],
                'socket': row['socket'],
                'speed': row['speed'],
                'coreCount': int(row['coreCount']),
                'threadCount': int(row['threadCount']),
                'power': int(row['power']),
                'VRAM': int(row['VRAM']),
                'resolution': row['resolution'],
                'size': int(row['size']),
                'space': int(row['space']),
                'productId': row['productId'],
                'precio': int(row['precio'])
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('CSV loaded into DynamoDB successfully!')
    }