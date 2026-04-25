import boto3
import json

def lambda_handler(event, context):
    # Configuración de recursos
    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.client('s3')
    
    table = dynamodb.Table('Estados_tabla_3') 
    bucket_name = 'ebani-act-devops'     
    
    # 1. Obtener datos de DynamoDB
    response = table.scan()
    items = response.get('Items', [])
    
    if not items:
        return {'statusCode': 404, 'body': 'No se encontraron datos'}

    # 2. Lógica para filtrar mayor y menor temperatura
    # Convertimos a int/float porque en DynamoDB suelen venir como strings o Decimal
    max_item = max(items, key=lambda x: float(x['Temperatura']))
    min_item = min(items, key=lambda x: float(x['Temperatura']))
    
    resultado = {
        "caluroso": {
            "estado": max_item['Estado'],
            "temperatura": str(max_item['Temperatura']),
            "humedad": str(max_item['Humedad'])
        },
        "frio": {
            "estado": min_item['Estado'],
            "temperatura": str(min_item['Temperatura']),
            "humedad": str(min_item['Humedad'])
        }
    }
    
    # 3. Subir el resultado filtrado a S3 como JSON
    s3.put_object(
        Bucket=bucket_name,
        Key='datos_filtrados.json',
        Body=json.dumps(resultado),
        ContentType='application/json'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Procesamiento completado con éxito')
    }