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


from markdown import markdown

from app.utils import generate_image_tag
from app.utils.functions.generate_youtube_iframe import generate_youtube_iframe


async def md_to_html(
        md: str,
):
    print(md)
    md_str_list = md.split('\n')
    md_str = ''
    body_html = ''

    for i in range(len(md_str_list)):
        if '![youtube]' in md_str_list[i]:
            md_str_list[i] = await generate_youtube_iframe(md_str_list[i])
        elif '![' in md_str_list[i]:
            md_str_list[i] = await generate_image_tag(md_str_list[i])
        md_str += md_str_list[i] + '<br>'
    md_html_list = markdown(md_str).split('\n')
    for i in range(len(md_html_list)):
        if '<p><img' in md_html_list[i]:
            md_html_list[i] = md_html_list[i][:2] + ' style="text-align: center"' + md_html_list[i][2:]
        body_html += md_html_list[i]

    return body_html
