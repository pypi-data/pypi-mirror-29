## README

1. `python`
2. `from crackle_api_helpers.api_wrapper import APIWrapper`
3. `wrapper = APIWrapper()`

## Example usage

`config = host_api_ps4()`  
`a = APIWrapper('ps4', config)`  
`a.find_media_with_min_duration()`  

## Available API methods:

Auth:
- register_config()
- register_quick()
- login(email, password)
- logout(user_id)
- deactivate(user_id)

Video:
- find_media()
- find_media_without_adverts()
- find_media_with_preroll()
- find_media_without_preroll()
- find_media_with_two_midrolls()
- find_media_with_rating(rating)
- find_media_with_min_duration(min_duration_mins)
