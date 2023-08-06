# Myotest client API

## Setup

  - Python > 3.4
  - pip install -r requirement.txt

## Install dev version in your notebook

This will install a python package named "revo-client" in your current environment

##### Local version

  - ```pip install -e {PATH TO YOUR REPO}```

##### Repository version

  - ```pip install revo-client```



## Create Client

By default a connect will connect to the production server

```python
from myotest import Client

# Connect to production server with your api token
client = Client("my-api-token")

# Connect to staging server
client = Client("my-api-token", server="staging")

# Connect to another server
client = Client("my-api-token", server="https://my-server")

# Create a client for another user ( you must be the user's coach to be able to get his information )
client = Client("my-api-token", user_id="other-user-uuid")

```

## Root queries

```python

# Fetch last workout that contains tags
workout = client.get_last_workout_with_tags(["vam_high", "ranges"])

# Fetch workout with id
workout = client.get_workout_with_id("workout-uuid")

# Fetch current profile
profile = client.get_profile()

```

## Objects

### Object :: Workout

#### Attributes
  - id (ID)
  - title (string)
  - start (datetime)
  - end (datetime)
  - type (string) workout type
  - target_duration (timedelta) workout requested duration
  - effective_duration (timedelta)
  - slots (list of Object::Slot)
  - datasets (list of Object::Dataset)
  
#### workout.get_dataset(name)
  Return the dataset matching name, if the name is complete (i.e. "mil-1") the dataset is returned.
  If the name is partial (i.e. "mil") the first dataset is returned (lower index)
  
#### workout.get_slots()
  Return all workout slots in execution order
  
#### workout.get_slot_with_tags(tags)
  Return the first slot (Object :: Slot) containing all tags, if any
  
  ```workout.get_slot_with_tags(["vm_high])```
  
 
### Object :: Dataset

#### Attributes
  - id (ID)
  - name (string)
  - dataframe (Pandas dataframe)
  - describe (dict) Full dataset describe
  - avro_schema (dict)
  - workout (Object::workout)

### Object :: Slot

#### Attributes
  - id (ID)
  - tags (list of string)
  - type (string)
  - value (Object::SlotValue)
  - text (string)
  - result (Object::SlotResult)
  - end_time (datetime)
  - start_time (datetime)
  - power_type (string)
  - analysis (list of dict)
  - workout (Object::workout)

### Object :: SlotResult

#### Attributes
  - power (dict) Describe of power **("max","min","std","mean","count","median")**
  - speed (dict) Describe of speed **("max","min","std","mean","count","median")**
  - gps_power (dict) Describe of gps_power **("max","min","std","mean","count","median")**
  - gps_speed (dict) Describe of gps_speed **("max","min","std","mean","count","median")**
  - distance (float) distance in meters
  - gps_distance (float) distance in meters
  - regularity_90 (float) regularity 90% of the time
  - step_count_ratio (float) step vs run ratio
  - regularity_median (float) median on regularity

**gps_speed** and **gps_power** are only available if the mil contains those information, if 
the user created a workout without gps, those values are null

### Object :: SlotValue

#### Attributes
  - value (float) distance=meters, duration=seconds, repetition=count
  - type (distance | duration | repetition )

### Object :: Profile

#### Attributes
  - id (ID)
  - full_name (string)
  - gender (male|female)
  - weight (float) in kilogram
  - height (float) in meter
  - leg_length (float) in meter
  - waist (float) in meter
  - vma (float)
  - pma (float)
  - birth_date (date)
  - age (float) in years
    
  
### Object :: AvroSchema

#### Attributes
  - name (string)
  - type (string) record type
  - fields (Array of dict)
  
  
## Script Example

```python
from myotest import Client

client = Client("my-api-token")
workout = client.get_last_workout_with_tags(["vma_high"]) 
slot = workout.get_slot_with_tags(["vma_high"])
profile = client.get_profile()

print(
    "Hello I'm {} and I am {} years old, my last" 
    "vma workout had a regularity of {}".format(
        profile.full_name, 
        profile.age, 
        slot.result.regularity_median))
```