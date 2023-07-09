import os
import re
from typing import List
from urllib.parse import unquote
from onThisDay.settings import MEDIA_ROOT, MEDIA_URL


# back here when you learn Celery
def delete_file(src: str) -> None:
    '''
    Delete a file based on its path. If there is no match it will do nothing
    
    Args:
        src(str): the path of the file 
            Ex: /media/uploads/froala_editor/images/default.png
    '''

    full_path = src.replace(MEDIA_URL, MEDIA_ROOT)
    file_path = os.path.abspath(full_path)
    is_exist = os.access(file_path, os.F_OK)
    if is_exist:
        os.remove(file_path)
    else:       # in case of url_encoded src, for non-alphanumeric characters
        file_path = unquote(file_path)
        is_exist = os.access(file_path, os.F_OK)
        if is_exist:
            os.remove(file_path)
      

def generate_imgs_paths(html: str) -> List[str]:

    pattern = r'<img.+?src\s*=\s*(?:"|\').+?(/media/.+?)(?:"|\')'
    matches = re.findall(pattern, html)

    return matches
