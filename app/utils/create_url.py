#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from urllib.parse import urlencode


async def create_url(
        id_: int,
        type_: str = 'get',
        token: str = None,
        language: str = None,
        is_admin: bool = None,
        bg_color: str = None,
        font_color: str = None,
):
    params = {}
    for name, value in zip(
            ['language', 'token', 'is_admin', 'bg_color', 'font_color'],
            [language, token, is_admin, bg_color, font_color],
    ):
        if value:
            params[name] = value

    url = f'/{id_}/{type_}?' + urlencode(params)
    return url
