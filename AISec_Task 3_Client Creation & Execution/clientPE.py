#!/usr/bin/env python

import boto3
import numpy as np
import argparse
import ast
from sklearn.preprocessing import RobustScaler

def main():
 
    import json
    import ember
    
    from sklearn.preprocessing import RobustScaler
    rs = RobustScaler()
       
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--featureversion", type=int, default=2, help="EMBER feature version")
    parser.add_argument("binaries", metavar="BINARIES", type=str, nargs="+", help="PE files to classify")
    args = parser.parse_args()
    #opening the downloaded PE file
    testpe = open(args.binaries[0],'rb').read()
    #Feature extractor class of the ember project 
    extract = ember.PEFeatureExtractor() 
    data = extract.feature_vector(testpe) #vectorizing the extracted features
    scaled_data = rs.fit_transform([data])
    Xdata = np.reshape(scaled_data,(1, 2381))
    Xdata= Xdata.tolist()

    client = boto3.client('runtime.sagemaker',
				region_name='us-east-1',
                              	#enter ids from AWS CLI
				aws_access_key_id='XXXXXXXXXXXXXX', 
				aws_secret_access_key='XXXXXXXXXXXXX',
				aws_session_token='XXXXXXXXXXXXX')
    
response = client.invoke_endpoint(EndpointName='sagemaker-tensorflow-2020-04-28-17-18-22-025', Body=json.dumps(Xdata))
    response_body = response['Body']
    out = response_body.read()
    astr = out.decode("UTF-8")
    out = ast.literal_eval(astr)
    out = out['outputs']['score']['floatVal']

    if out[0] >0.5:
        print("Malicious")
    else:
        print("Benign")
		
if __name__ == "__main__":
	main()
