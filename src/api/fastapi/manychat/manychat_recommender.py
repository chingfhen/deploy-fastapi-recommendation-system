

from fastapi import APIRouter

manychat_router = APIRouter()


@manychat_router.get("/manychat/recommend")
async def manychat_recommend():
    return {
        "version": "v2",
        "content": {
            "messages": [
            {
                "type": "image",
                "url": "https://storage.googleapis.com/seller123/693560",
                "buttons": [{
                    "type": "url",
                    "caption": "External link",
                    "url": "https://shopee.sg/arietes.acc",
                    "webview_size": "full"
                }]
            }
            ],
            "actions": [],
            "quick_replies": []
        }
    }
