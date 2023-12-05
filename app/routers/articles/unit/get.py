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


from mybody_api_client import MyBodyApiClient
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_302_FOUND

from app.utils import ErrorResponse, Router, md_to_html, generate_get_css, create_url
from config import BG_COLOR_DEFAULT, FONT_COLOR_DEFAULT

router = Router(prefix='/get')


@router.get()
async def route(
        id_: int,
        token: str = None,
        language: str = None,
        bg_color: str = BG_COLOR_DEFAULT,
        font_color: str = FONT_COLOR_DEFAULT,
        is_admin: bool = False,
):
    mybody_api_client = MyBodyApiClient(token=token)

    # Checking a token, has a role in case of a flag is_admin
    if token:
        account = await mybody_api_client.account.get()
        if account.state == 'error':
            return ErrorResponse(message=account.message)
        if is_admin:
            if 'articles' not in account.roles:
                return ErrorResponse(message='Insufficient permissions to view this article')
    elif is_admin:
        return ErrorResponse(message='Insufficient permissions to view this article')

    article = await mybody_api_client.article.get(
        id_=id_,
        language=language or None,
    )

    if article.state == 'error':
        return ErrorResponse(message=article.message)
    if article.language != language:
        language = article.language
        redirect_url = await create_url(
            id_=id_,
            type_='get',
            token=token,
            language=language,
            is_admin=is_admin,
            bg_color=bg_color,
            font_color=font_color,
        )
        return RedirectResponse(url=redirect_url, status_code=HTTP_302_FOUND)

    # Generate response
    body = await md_to_html(md=article.md)
    styles = await generate_get_css(bg_color=bg_color, font_color=font_color)
    url = await create_url(
        id_=id_,
        type_='update',
        token=token,
        language=language,
        is_admin=True,
        bg_color=bg_color,
        font_color=font_color,
    )

    with open(f'assets/html/get.html', encoding='utf-8', mode='r') as base_html:
        content = base_html.read().format(
            styles=styles,
            title=article.name,
            md=body,
            button_display='block' if is_admin else 'none',
            url=url,
        )
    return HTMLResponse(content=content)
