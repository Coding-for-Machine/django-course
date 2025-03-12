from ninja import Router
from . import course_api, modules_api, lesson_api, problems_api, quiz_api, queation_api
admin_router = Router()

admin_router.add_router("course/", course_api.course_api_router)
admin_router.add_router("module/", modules_api.api_module_router)

admin_router.add_router("lesson/", lesson_api.lesson_router_api)
admin_router.add_router("problem/", problems_api.problems_router_api)
admin_router.add_router("quiz/", quiz_api.quize_router)
admin_router.add_router("question/", queation_api.question_router)
# admin_router.add_router("lesson/", lesson_api)


