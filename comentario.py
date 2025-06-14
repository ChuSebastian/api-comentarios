import boto3
import uuid
import os

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    nombre_tabla = os.environ["TABLE_NAME"]
    # Proceso
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
            'texto': texto
        }
    }

    # Grabar en S3 (Ingesta Push)
    s3 = boto3.client('s3')
    file_key = f'{tenant_id}/{uuidv1}.json'
    s3.put_object(
        Bucket=bucket_ingesta,
        Key=file_key,
        Body=json.dumps(comentario),
        ContentType='application.json'
    )

    # Grabar en DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    response = table.put_item(Item=comentario)

    # Salida (json)
    print(comentario)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'response': response
    }
