## README

1. `python`
2. `from crackle_api_helpers.api_wrapper import APIWrapper`
3. `wrapper = APIWrapper()`

## Example usage

`config = host_api_ps4()`  
`a = APIWrapper(config)`  
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
        Find any media item  
        returns: ('media_id', 'short_name', 'media_duration')

- find_media_without_adverts()  
        Find a media item without any adverts  
        returns: ('media_id', 'short_name', 'media_duration')

- find_media_with_preroll()  
        Find a media item with a preroll  
        returns: ('media_id', 'short_name')
 
- find_media_without_preroll()  
        Find a media item without a preroll  
        returns: ('media_id', 'short_name')

- find_media_with_two_midrolls()  
        Find a media item with at least two midrolls  
        returns: ('media_id', 'short_name', [midroll timestamps (seconds)])
        
- find_media_with_rating(rating)  
        Find a media item with the given rating  
        rating: 'Not Rated', 'PG' 'PG-13', 'TV-14', 'R'  
        returns: ('media_id', 'short_name')  
        
- find_media_with_min_duration(min_duration_mins)  
        Find a media item with the minimum duration  
        min_duration: minimum duration in minutes  
        returns: ('media_id', 'short_name')  
