import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
def main(param_dict):
    authenticator = IAMAuthenticator(param_dict["IAM_API_KEY"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(param_dict["COUCH_URL"])
    if 'dealerId' in param_dict:
        response = service.post_find(db='reviews', selector={'dealership' : {'$eq' : int(param_dict['dealerId'])}},).get_result()
        try:
            result= {
                'headers': {'Content-Type' : 'application/json'},
                'body' : {'data':response}
            }
            return result
        except:
            return {
                'statusCode' : 404,
                'message': 'Something went wrong'
            }
    else:
        response = service.post_document(db='reviews', document=param_dict["review"]).get_result()
        try:
            result= {
            'headers': {'Content-Type':'application/json'},
            'body': {'data':response}
            }
            return result
        except:
            return {
            'statusCode': 404,
            'message': 'Something went wrong'
            }
