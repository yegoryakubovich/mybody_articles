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


async def generate_image_tag(
        tag: str,
):
    link = tag[tag.find('(')+1:tag.find(')')]
    description = tag[tag.find('[')+1:tag.find(']')]
    content = f"""<p style="text-align: center; margin: 0">
    <img alt="{description}" src="{link}" onerror="this.onerror=null;this.src='/assets/images/not_found.png';">"""
    if description:
        content += f"""<p style="
    text-align: center;
     font-style: italic
      font-size: 14px;
       color: var(--text-secondary);
        margin: 0 0">{description}</p>"""
    content += """</p>"""
    return content
