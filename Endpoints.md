# Endpoints

## POST - /api/runs

**Post a new run.**

Request Body:
```json
{
    "username": "username",
    "start_time": "start_time"
}
```
Response Body:
```json
{
    "username": "username",
    "start_time": "start_time",
    "run_id": "run_id"
}
```
_________________________________________________________________
## PATCH - /api/runs

**Update a run with it's required information.**

Request Body:
```json
{
    "username": "username",
    "run_id": "run_id",
    "finish_time": "finish_time",
    "average_speed": "average_speed",
    "total_distance": "total_distance",
    "coordinates": "coordinates"
}
```
`coordinates` is an object with key of run which is a stringified array of location objects as below:
```json
"[{
    longitude: -2.2397547,
    latitude: 53.4860582
}, ...]"
```
_________________________________________________________________
## GET - /api/runs

**Get all runs for a users subscribers as an array of runs.**

Query Parameter: `?username=<insert username>`
_________________________________________________________________
## GET - /api/users/:username/runs

**Get all runs for a specific user as an array of runs.**

```json
{
  "runs": [
    {
      "username": "username",
      "run_id": "run_id",
      "start_time": "start time"
    }, ...
    ]
}
```
_________________________________________________________________
## GET - /api/users

**Get all users returns an array of users**

```json
{
"users": [
    {
      "cumulative_distance": "cumulative_distance",
      "rewards_earned": "number of rewards earned",
      "username": "username",
      "followers": [],
      "subscriptions": []
    }, ...
    ]
}
```
_________________________________________________________________
## POST - /api/users

**Adds a new user to the database.**

Request Body:
```json
{
    "username": "username"
}
```
Response Body:
```json
{
    "username": "username",
    "cumulative_distance": 0,
    "rewards_earned": 0,
    "followers": [],
    "subscriptions": [],
}
```
_________________________________________________________________
## PATCH - /api/users/:username

**Adds the distance for a completed run to the user's cumulative distance key.**

Request Body:
```json
{
    "distance": "distance"
}
```
`distance` is a number.

Response Body:
```json
{
    "username": "username",
    "cumulative_distance": <new distance added here>,
    "rewards_earned": 0,
    "followers": [],
    "subscriptions": [],
}
```

_________________________________________________________________
## GET - /api/users/:username

**Returns the requested user**

Response Body:
```
{
  "user": {
    "cumulative_distance": 0.0,
    "rewards_earned": 2.0,
    "username": "username",
    "followers": [],
    "subscriptions": []
  }
}
```
_________________________________________________________________
## PATCH - /api/users/:username/followers

**Adds a follower to the user's followers array.**

Request Body:
```json
{
    "username": <username of follower>
}
```
_________________________________________________________________
## PATCH - /api/users/:username/subscriptions

**Adds a subscription to the user's subscriptions array.**

Request Body:
```json
{
    "username": <username of subscription>
}
```

_________________________________________________________________
## POST - /api/rewards

**Adds a new reward to the database.**

Request Body:
```json
{
    "challenge": "<running distance to achieve>",
    "reward": "<reward to be earned>"
}
```
`challenge` is a number.

_________________________________________________________________
## PATCH - /api/rewards

**Updates the reward's winner and whether it has been achieved.**

Request Body:
```json
{
    "reward_id": "reward_id",
    "winner": "<username of the user that achieved fthe challenge>"
}
```
_________________________________________________________________
## GET - /api/rewards

**Returns all the rewards that have yet to be achieved. If queried as below the response will contain all rewards that have been achieved.**

Query Parameter: `?completed=yes`

Response Body:
```
 {
    "completed": true/false,
    "reward_id": "reward_id",
    "challenge": "challenge distance,
    "winner": "winner,
    "reward": "reward"
}
```
_________________________________________________________________
## PATCH - /api/rewards/:username

**Updates the total number of rewards achieved for a specific user.**

No request body required.
