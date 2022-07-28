import codecs

from app.model.line_ten import InvoiceLineTen
from app.services.s3_service import S3Service

from app.utils.utils import get_request_id, is_str_or_dict

file = S3Service()


def handler(event, context):
    data = []
    try:
        request_id = get_request_id(event, context)
        message = is_str_or_dict(event)
        body = is_str_or_dict(message['Records'][0]['body'])
        write_file = file.get_file_to_write(request_id, body)
        line_stream = codecs.getreader('ISO-8859-1')
        for line in line_stream(write_file.get()['Body']):
            if line.startswith('10', 0, 2):
                line_ten = InvoiceLineTen(line).__dict__()
                data.append(line)
            elif line.startswith('29', 0, 2):
                if line_ten['cpf_cnpj'] == body['cpf_cnpj']:
                    data.append('29' + body['qrcode']['emv'] + '\r\n')
                    data.append('30' + body['qrcode']['text'] + '\r\n')
                    data.append('31' + body['qrcode']['image'] + '\r\n')
                else:
                    data.append(line)
            else:
                data.append(line)

        file.save_file(request_id, body, data)
        print('FIM')
    except Exception as e:
        print(e)
        raise


if __name__ == '__main__':
    eeeee = {
        "Records": [
            {
                "messageId": "90d0f116-0035-45d8-83ab-e1e11466cf7a",
                "receiptHandle": "AQEB/OIM6mxql1NrKCFS/KLBofii1nKwsUbTetW0a7w==",
                "body": "{\n   \"file_name\":\"EcosyInstdePagamentoSA29042022.txt\",\n   \"bucket_name\":\"read-invoice\",\n   \"nome_cedente\":\"Banco EC S.A.\",\n   \"cnpj_cedente\":\"33264668000103\",\n   \"data_geracao\":\"29042022\",\n   \"data_vencimento\":\"29072022\",\n   \"nome_cliente\":\"FABILANIA SANDES\",\n   \"cpf_cnpj\":\"99959835243\",\n   \"conta\":\"682680\",\n   \"cep\":\"71505235\",\n   \"cidade\":\"Barueri\",\n   \"estado\":\"DF\",\n   \"endereco\":\"Av. Tambore\",\n   \"numero\":\"267\",\n   \"complemento\":\"Complemento\",\n   \"valor_fatura\":\"00000000204655\",\n   \"idtx\":\"QT332646680001032904202200000000001\",\n   \"loc\":{\n      \"url\":\"api-h.developer.btgpactual.com/v1/p/v2/bd2f1763b529490c97792f543fd1d01c\",\n      \"emv\":\"00020101021226930014br.gov.bcb.pix2571api-h.developer.btgpactual.com/v1/p/v2/bd2f1763b529490c97792f543fd1d01c5204010053039865802BR5923Joselito de Souza Silva6007Barueri61087150523562070503***630471FB\",\n      \"locType\":\"COB\",\n      \"id\":\"4078206097511746876\",\n      \"idTx\":\"RQT332646680001032904202200000000019999\",\n      \"loc\":\"bd2f1763-b529-490c-9779-2f543fd1d01c\"\n   },\n   \"qrcode\":{\n      \"emv\":\"00020101021226930014br.gov.bcb.pix2571api-h.developer.btgpactual.com/v1/p/v2/bd2f1763b529490c97792f543fd1d01c5204010053039865802BR5923Joselito de Souza Silva6007Barueri61087150523562070503***630471FB\",\n      \"text\":\"MDAwMjAxMDEwMjEyMjY5MzAwMTRici5nb3YuYmNiLnBpeDI1NzFhcGktaC5kZXZlbG9wZXIuYnRncGFjdHVhbC5jb20vdjEvcC92Mi9iZDJmMTc2M2I1Mjk0OTBjOTc3OTJmNTQzZmQxZDAxYzUyMDQwMTAwNTMwMzk4NjU4MDJCUjU5MjNKb3NlbGl0byBkZSBTb3V6YSBTaWx2YTYwMDdCYXJ1ZXJpNjEwODcxNTA1MjM1NjIwNzA1MDMqKio2MzA0NzFGQg==\",\n      \"image\":\"iVBORw0KGgoAAAANSUhEUgAAAPoAAAD6AQAAAACgl2eQAAADI0lEQVR4Xu2WUZIbIQxE4SJw/1vkKHARyHvCYztO1VY+Mvoy2c0w0K7qlbpbLvvn9at8nnysL+CsL+CsfwKMUuqeo/VR+uSl77n5ieMsgK+jjx670VcrrfIMVBpgVG9ag9VcfdTVF7/nOBFAmXiWFly5bnWmA6hOOZgKRJYP7lkAftBH9WRasArlGcdpANU5/15/qvrzdv5fgGvZr9LCQaEaLy/zJgBsEK0qiIUn5vWtUzC6lwUAwS2Pqmxgh2hDPlezEgBkBTznUifkmFUCPzVxHqBVeqVwd0TpCZDiaRrAFKU+K2pkgRYv9s/qJQHMb/QBoxUOEvXRrNsBe3nJOc7pmGZrXHZuswADPkNW3vEWAm4+rr8iARDn1QiPOcJdM0nHq1m3AyiIZqFhNUwElEC3Sg+SCYAtHZgiVK5DsxpoPkkmADjEvFLVPuiVwg0ldAkmA8AFZdpKtZgbAfE0D2BqGRdiYGepegTJU7T3AzwVQsP4xyyrhkhFvddfcT9gqRXHSWWu82aT+IjXaQBFy0yTJP2qVknlmu15gHnCQmLVnQBUa66nAbSNAVrCQHIujtpnsxIAfr/VrWHYuFW58828CQBd42WYt0p6HyslAjwoTlUZhnVQTp+STwNw3ZFqzNI9hNXp81XJ+wFzmZ68WR/5ybm+vmAkALbTTKownQ5VG7btXCJg2Cx6hXtJMP7zO0Z9M+/9AGxbQzTVNLd1bMjRZ6ESACES6zT0rVRb5HomAHLowyhTKrExPY6GkwCG+Qpu0CTLnCyPGEsDLDPUK07Y0KVgG4mSBTipxfxgiuBabLv9zvFqVgaAylgjFUuLmtNth4nzALCM6LBdVRft8HK0KwvAGY5Ru1EjukTZCFZblgVYsmr69ohHoXi/30R7NyBcA6OYqs6zCBTTZOcB9ikWHAfuQasWK3yUBpCO3VGvksU1gOe7cW4H2BVF6w7p4p/lJzzPA9gqjhzuENYyTTNH6RIBU5XYqh1bemWU5AJoD/PdEImaxXAfFi8L8MDQox7yaWYp+3fB3AzgyPy6+mSo8uqHdhrgx/UFnPUFnPUfAL8BCYZ/x1j8g+0AAAAASUVORK5CYII=\",\n      \"payloadURL\":\"api-h.developer.btgpactual.com/v1/p/v2/bd2f1763b529490c97792f543fd1d01c\",\n      \"idDocument\":\"6f398083-0014-49b3-9a13-9a0d1f3ca952\",\n      \"idTx\":\"RQT33264668000103290420220000000001\"\n   }\n}",
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1656852238363",
                    "SequenceNumber": "18870898246730480640",
                    "MessageGroupId": "QT332646680001032904202200000000001",
                    "SenderId": "AIDAYT3YFZIESZ6X7UGX6",
                    "MessageDeduplicationId": "QT332646680001032904202200000000001",
                    "ApproximateFirstReceiveTimestamp": "1656852238363"
                },
                "messageAttributes": {

                },
                "md5OfBody": "d0fb1e15ae0c85ea1ebb41f2d03177d2",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:sa-east-1:592420653577:write-invoice.fifo",
                "awsRegion": "sa-east-1"
            }
        ]
    }
    handler(eeeee, None)
