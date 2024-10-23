import json

def lambda_handler(event, context):
    try:
        # Extraemos los datos recibidos desde la EC2
        body = json.loads(event['body'])
        optimized_components = body.get('priority-components', [])
        
        # Devolvemos los datos optimizados al frontend
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({
                'message': 'Datos recibidos exitosamente desde la EC2',
                'optimized_components': optimized_components
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'message': 'Error al recibir los datos', 'error': str(e)})
        }