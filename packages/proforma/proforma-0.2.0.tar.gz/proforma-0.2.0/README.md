# Proforma

This is a simple library to help me setup AWS infrastructure.

Don't use this.  Go use Terraform or Cloud Formation.

## Usage

Let's say our infrastructure consists of an S3 bucket
and an IAM role with an inline policy that allows access to that bucket.

```python
import json

from proforma import CompositeComponent
from proforma.aws import Bucket, IAMRole, RoleInlinePolicy

class MyBucket(Bucket):
    def __init__(self, **options):
        super().__init__(name='my-bucket', **options)

class MyBucketAccessRole(IAMRole):
    def __init__(self, **options):
        super().__init__(name='my-bucket-role', **options)
            
class MyRoleInlinePolicy(RoleInlinePolicy):
    def __init__(self, **options):
        super().__init__(role_name='my-bucket-role',
                         name='my-bucket-policy',
                         policy_document=json.dumps(
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::my-bucket"
                ]
            }),
            **options
        )
        
class MyDeployment(CompositeComponent):
    SUBCOMPONENTS = {
        'bucket': MyBucket,
        'role': MyBucketAccessRole,
        'role-policy': MyRoleInlinePolicy
    }    

# You can now setup, check and teardown this infrastructure as follows:

MyDeployment().setup()
MyDeployment().check()
MyDeployment().teardown()
```
