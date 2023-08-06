Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
Description-Content-Type: UNKNOWN
Description: ﻿smsapi-python
        =============
        
        Client for SMSAPI.
        
        ## COMPATIBILITY:
        Compatible with Python 2.7+, 3.+.
        
        ## REQUIREMENTS:
        requests
        
        ## INSTALLATION:
        If You have pip installed:
        
            sudo pip install smsapi-client
        
        else You can install manually:
        
            git clone https://github.com/smsapi/smsapi-python-client.git
        
            cd smsapi-python
        
            python setup.py install
        
        ## Client instance:
        
        If You are smsapi.pl customer You should import
        ```python
            from smsapi.client import SmsApiPlClient
        ```
        
        else You need to use client for smsapi.com
        ```python
            from smsapi.client import SmsApiComClient
        ```
        
        ## Credentials
        
        - Access Token
        ```python
            client = SmsApiPlClient(access_token='your-access-token')
        ```
        
        ## Examples
        
        - Send SMS
        ```python
            from smsapi.client import SmsApiPlClient
            
            client = SmsApiPlClient(access_token='your access token')
            
            r = client.sms.send(to='phone number', message='text message')
            
            print(r.id, r.points, r.status, r.error)
        ```
        
        - **You can find more examples in "examples" directory in project files.**
        
        
        ## Error handling
        
        ```python
            from smsapi.exception import SmsApiException
        
            try:
                contact = client.sms.send(to='123123')
            except SmsApiException as e:
                print(e.message, e.code)
        ```
        
        ## LICENSE
        [Apache 2.0 License](https://github.com/smsapi/smsapi-python-client/blob/master/LICENSE)
Platform: UNKNOWN
Classifier: Development Status :: 3 - Alpha
Classifier: Intended Audience :: Developers
Classifier: License :: Apache 2.0
Classifier: Topic :: Software Development :: Libraries :: Python ModulesProgramming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3.2
Classifier: Programming Language :: Python :: 3.3
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
Classifier: Programming Language :: Python :: 3.6
