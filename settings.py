import os
from decouple import config

CLIPPINGS_FILE = config('CLIPPINGS_FILE', default="MyClippings.txt")
NOTION_TOKEN = config(
    'NOTION_TOKEN', default= "965704f5b164b1d090e093067a5c72ef09455eb562fcb5764e0e1e122fe0fc87cdeefdbfddc374f3e1beef9a60a4403eeafae664b1a79293f1910ebd28e4dfe9917bbabc816caa10e97f58358f6b")
NOTION_TABLE_ID = config(
    'NOTION_TABLE_ID', default="https://www.notion.so/d61023cf4f134f12926bc34d785f097a?v=278b5c16962c4d6bbad0bbeeb7794054")
