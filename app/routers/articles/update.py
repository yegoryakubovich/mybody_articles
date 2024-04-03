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


from typing import Annotated

from fastapi import Form
from mybody_api_client import MyBodyApiClient
from mybody_api_client.utils.exceptions import ApiException
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_302_FOUND

from app.utils import Router, ErrorResponse, create_url, generate_update_css
from config import BG_COLOR_DEFAULT, FONT_COLOR_DEFAULT, API_URL

router = Router(prefix='/update')


@router.get()
async def route(
        id_: int,
        token: str,
        language: str = None,
        bg_color: str = BG_COLOR_DEFAULT,
        font_color: str = FONT_COLOR_DEFAULT,
):
    try:
        mybody_api_client = MyBodyApiClient(token=token, url=API_URL)
        response = await mybody_api_client.client.articles.get_additional(
            id_=id_,
            language=language,
        )
        name, md = response.name, response.md
        url = await create_url(
            id_=id_,
            type_='update',
            token=token,
            language=language,
            is_admin=True,
            bg_color=bg_color,
            font_color=font_color,
        )
        styles = await generate_update_css(bg_color=bg_color, font_color=font_color)

        with open(f'assets/html/update.html', encoding='utf-8', mode='r') as base_html:
            content = base_html.read().format(
                title=name,
                name=name,
                md=md,
                url=url,
                styles=styles,
            )

        return HTMLResponse(content=content)
    except ApiException as e:
        return ErrorResponse(code=e.code, message=e.message)


@router.post()
async def route(
        name: Annotated[str, Form()],
        md: Annotated[str, Form()],
        id_: int,
        token: str,
        language: str = None,
        bg_color: str = BG_COLOR_DEFAULT,
        font_color: str = FONT_COLOR_DEFAULT,
):
    try:
        mybody_api_client = MyBodyApiClient(token=token, url=API_URL)

        article = await mybody_api_client.client.articles.get_additional(
            id_=id_,
            language=language or None,
        )

        if article.language != language:
            language = article.language

        await mybody_api_client.admin.articles.update_md(
            id_=id_,
            md=md,
            language=language or None,
        )
        url = await create_url(
            id_=id_,
            type_='get',
            token=token,
            language=language,
            is_admin=True,
            bg_color=bg_color,
            font_color=font_color,
        )
        return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
    except ApiException as e:
        return ErrorResponse(code=e.code, message=e.message)
