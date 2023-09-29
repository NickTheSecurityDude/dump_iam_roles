# dump_iam_roles

Dumps IAM roles in json format for easy searching with jq.

Example:
```
python3 dump_roles.py > role_dump.json 

# Searching - Note below queries don't take into account NotAction/NotResource, conditions, etc

# all roles with admin access
cat role_dump.json| jq -r '.roles[] | select(.policies[][].Action[]=="*") |  .roleName' |sort -n | uniq

# role names with s3 access (does not include admin access)
cat role_dump.json| jq -r '.roles[] | select(.policies[][].Action[]| contains("s3")) |  .roleName' |sort -n | uniq

# roles which can delete s3 objects
cat role_dump.json| jq -r '.roles[] | select(.policies[][].Action[]| contains("s3:Del")) | .roleName'

# roles with s3 access, shows full permission (does not include admin access)
for i in `cat role_dump.json| jq -r '.roles[] | select(.policies[][].Action[]| contains("s3")) |  .roleName' |sort -n | uniq`;do echo $i;cat role_dump.json| jq -r --arg ROLE "$i" '.roles[] | select(.roleName==$ROLE)' ;done

# full permission for specific role
cat role_dump.json| jq -r  '.roles[] | select(.roleName=="test-role")'

# s3 permissions for a specific role
cat role_dump.json| jq -r  '.roles[] | select(.roleName=="test-role") | .policies[][] | .Action[] | select(. | contains("s3"))'
```
