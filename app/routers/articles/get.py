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

from typing import Optional

from fastapi import Depends
from mybody_api_client import MyBodyApiClient
from pydantic import BaseModel, Field
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_302_FOUND
from mybody_api_client.utils.exceptions import ApiException, NotEnoughPermissions, ArticleSessionRequired

from app.utils import ErrorResponse, Router, md_to_html, generate_get_css, create_url
from config import settings

router = Router(prefix='/get')


class ArticleGetSchema(BaseModel):
    id: int = Field()
    token: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None)
    bg_color: Optional[str] = Field(default=settings.bg_color_default)
    font_color: Optional[str] = Field(default=settings.font_color_default)
    is_admin: Optional[bool] = Field(default=False)


@router.get()
async def route(schema: ArticleGetSchema = Depends()):
    try:
        id_ = schema.id
        token = schema.token
        language = schema.language
        bg_color = schema.bg_color
        font_color = schema.font_color
        is_admin = schema.is_admin

        mybody_api_client = MyBodyApiClient(token=token, url=settings.api_url)

        article = await mybody_api_client.client.articles.get(
            id_=id_,
        )

        # Checking a token, has a role in case of a flag is_admin
        if token:
            account = await mybody_api_client.client.accounts.get()
            permissions = account['permissions']
            if is_admin:
                if 'articles' not in permissions:
                    raise NotEnoughPermissions
        else:
            if not article['can_guest']:
                raise ArticleSessionRequired
            if is_admin:
                raise NotEnoughPermissions

        article = await mybody_api_client.client.articles.get_additional(
            id_=id_,
            language=language or None,
        )

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
    except ApiException as e:
        return ErrorResponse(code=e.code, message=e.message)
