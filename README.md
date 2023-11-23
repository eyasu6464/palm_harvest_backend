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

#### API Descriptions
1. `api/token`
   ```JSON
   {
    "username":"username here",
    "password":"password here"
   }
  
   ```

2. `api/registeruser`
   ```JSON

   ```
3. `api/registerbranch`

   ```JSON
   {
    "branchname":"Branch name here",
    "city":"city name",
    "address_longitude":"Longitude value",
    "address_latitude":"Latitude value"
   }
   ```

4. `api/uploadimage`
   ```JSON
   form data with key name image

   ```
