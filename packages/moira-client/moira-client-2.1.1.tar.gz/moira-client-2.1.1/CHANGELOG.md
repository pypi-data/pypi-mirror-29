# 2.1.1
- Allow passing warn_value and error_value for trigger as None when expression is used
- Fixed case with subscription's schedule with no days selected

# 2.0
- Added custom headers support
- Added trigger creation by custom id
- Removed tags extra data addition feature
- Changed ttl type from string to int
- Optimized fetch_by_id for large production solutions

# 0.4
- Added fetch_assigned_triggers_by_tags method for Tag entity
- Fixed trigger existence check. Check equals by casting to sets
- Fixed trigger delete logic

# 0.3.3
- Fixed contact creation. Explore only current user's contacts

# 0.3.2
- Added basic authorization

# 0.3.1
- Trigger update on save
- Subscription is_exist method added
- Contact idempotent creation

# 0.3
- Store id in Trigger after save of existent trigger
- Add get_id Contact method

# 0.2
- TriggerManager is_exist function added
- TriggerManager get_non_existent function added

# 0.1.1
- Trigger exist check added

# 0.1
- base functionality (support for models: contact, event, notification, pattern, subscription, tag, trigger)
