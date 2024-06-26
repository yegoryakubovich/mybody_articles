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


from starlette.responses import RedirectResponse

from app.utils.router import Router
from .get import router as router_get
from .update import router as router_update

router = Router(
    prefix='',
    routes_included=[
        router_get,
        router_update,
    ],
)


@router.get('/', include_in_schema=False)
async def route():
    return RedirectResponse('/docs')
