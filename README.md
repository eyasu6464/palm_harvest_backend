## Palm Harvest Backend

Techstack: Django


#### List of Api
| Method | URL | Description |
| ------ | --- | ----------- |
| POST | `api/token` | Used to login and get access and refresh tokens |
| POST | `api/registeruser` | Used to register Managers and Harvesters |
| POST | `api/registerbranch` | Used to register Branches |
| POST | `api/uploadimage` | used to upload images by Harvesters |
| GET | `api/users` | get all users info |
| GET | `api/branches` | get all branches |
| GET | `api/userinformation` | get current user information |
| GET | `api/getbranch/id` | get specific branch by id |
| GET | `api/activateaccount/id/` | activate user account by id |
| GET | `api/deactivateaccount/id/` | deactivate user account by id |
| PUT | `updatebranch/id/` | update branch informaiton |
| DELETE | `deletebranch/id/` | delete branch |

##### All API need Bearer Token except register 

#### POST API Descriptions
1. `api/token`
   ```JSON
   {
    "username":"username here",
    "password":"password here"
   }
  
   ```
   Response: access and refresh tokens

   ```JSON
   {
    "refresh": "REFRESH KEY TOKEN",
    "access": "Access KEY TOKEN"
   }
   ```

3. `api/registeruser`
   ```JSON
   {
    "first_name":"First name",
    "last_name":"Last name",
    "email":"Email",
    "password":"Password",
    "user_type":"Type",
    "address":"Address",
    "branch_id":"ID"
   }
   ```
   Response: Approval Message
4. `api/registerbranch`

   ```JSON
   {
    "branchname":"Branch name here",
    "city":"city name",
    "address_longitude":"Longitude value",
    "address_latitude":"Latitude value"
   }
   ```
   Response: Approval Message

5. `api/uploadimage`
   ```JSON
   form data with key name image
   ```
   Response: Approval Message

#### GET API Descriptions
1. `api/users`
   Response: Array of users
   ```JSON
   [
    {
        "palmuser": {
            "id": id,
            "username": "username",
            "email": "email",
            "first_name": "First Name",
            "last_name": "Last Name",
            "is_active": "Boolean"
        },
        "branch":  branch ID,
        "user_type": "USER_TYPE",
        "address": "Address of User"
    }
   ]
   ```


2. `api/branches`
   Response: Array of Branches
   ```JSON
   [
    {
        "branchid": branch ID,
        "branchname": "Branch Name",
        "city": "Branch Ciry",
        "address_longitude": "Longitude Address",
        "address_latitude": "Latitude Address"
    }
   ]
   ```

3. `api/userinformation`
   Response: Current user information
   ```JSON
   {
        "palmuser": {
            "id": id,
            "username": "username",
            "email": "email",
            "first_name": "First Name",
            "last_name": "Last Name"
        },
        "branch":  branch ID,
        "user_type": "USER_TYPE",
        "address": "Address of User"
    }
   ```
5. `api/getbranch/id`
   Response: Branch Information with Specific ID
   ```JSON
   {
        "branchid": branch ID,
        "branchname": "Branch Name",
        "city": "Branch Ciry",
        "address_longitude": "Longitude Address",
        "address_latitude": "Latitude Address"
    }
   ```
6. `api/activateaccount/id/`
   Response: Approval Messsage
7. `api/activateaccount/id/`
   Response: Approval Messsage

#### PUT API Descriptions

1. `updatebranch/id/`

   ```JSON
   {
    "branchname":"Branch name here",
    "city":"city name",
    "address_longitude":"Longitude value",
    "address_latitude":"Latitude value"
   }
   ```
   Response: Approval Message

#### dELETE API Descriptions

1. `deletebranch/id/`
   Response: Approval Message