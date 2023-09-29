import boto3,json,os

# main routine
if __name__ == "__main__":

  iam_client = boto3.client('iam')

  #print("Checking all roles")

  # Dict for results
  all_roles={"roles":[]}

  # Paginator
  p=iam_client.get_paginator('list_roles')
  paginator=p.paginate()  

  # Loop through pages
  for page in paginator:
    roles=page['Roles']

    # Loop through roles
    for role in roles:
      role_name=role['RoleName']
      if "ServiceRole" not in role_name and "AWSReservedSSO" not in role_name and "aws-controltower" not in role_name and "AWSControlTower" not in role_name:
        role_results={"roleName":role_name,"policies":[]}

        #Get inline policies
        policies = iam_client.list_role_policies(
          RoleName=role_name
        )['PolicyNames']

        for policy_name in policies:
          response = iam_client.get_role_policy(
            RoleName=role_name,
            PolicyName=policy_name
          )
          statement=response['PolicyDocument']['Statement']

          # Make sure actions are in a list
          for sid in statement:
            action=sid['Action']
            if not isinstance(action,list):
              sid['Action']=[sid['Action']]

          role_results['policies'].append(statement)

        #Get managed policies
        policies = iam_client.list_attached_role_policies(
          RoleName=role_name
        )['AttachedPolicies']

        for policy in policies:
          policy_arn=policy['PolicyArn']

          # Get policy version
          policy_version=response = iam_client.get_policy(
            PolicyArn=policy_arn
          )['Policy']['DefaultVersionId']

          # Get policy document's statements
          response = iam_client.get_policy_version(
            PolicyArn=policy_arn,
            VersionId=policy_version
          )

          statement=response['PolicyVersion']['Document']['Statement']

          # Make sure actions are in a list
          for sid in statement:
            action=sid['Action']
            if not isinstance(action,list):
              sid['Action']=[sid['Action']]

          role_results['policies'].append(statement)

        all_roles['roles'].append(role_results)

  print(json.dumps(all_roles))


