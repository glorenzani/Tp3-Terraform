import json
import requests
import os

def lambda_handler(event, context):
    try:
        # Extraemos los datos que vienen desde el API Gateway (frontend)
        body = json.loads(event['body'])
        budget = body['budget']
        components = body['priority-components']
        
        # La IP privada de la EC2 donde se ejecuta el modelo de optimización
        ec2_private_ip = os.environ['EC2_ENDPOINT']
        headers = {'Content-Type': 'application/json'}
        
        # Enviar los datos a la EC2 para su procesamiento
        payload = {
            'budget': budget,
            'priority-components': components
        }
        
        response = requests.post(ec2_private_ip, data=json.dumps(payload), headers=headers)
        
        if response.status_code == 200:
            # Obtenemos los datos optimizados de la EC2
            optimized_data = response.json()

            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                'body': json.dumps({
                    'message': 'Optimización exitosa',
                    'optimized_components': optimized_data
                })
            }
        else:
            return {
                'statusCode': response.status_code,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                'body': json.dumps({'message': 'Error al procesar en la EC2'})
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'message': 'Error en la Lambda', 'error': str(e)})
        }