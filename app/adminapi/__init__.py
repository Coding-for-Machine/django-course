from ninja import Router
from . import course_api, modules_api
admin_router = Router()

admin_router.add_router("course/", course_api.course_api_router)
admin_router.add_router("module/", modules_api.api_module_router)


