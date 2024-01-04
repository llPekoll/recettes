from bs4 import BeautifulSoup
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class RemoveDataTestMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if settings.DEBUG:
            return response

        if "text/html" in response["Content-Type"]:
            soup = BeautifulSoup(response.content, "html.parser")
            for tag in soup.find_all(attrs={"data-test": True}):
                del tag["data-test"]
            response.content = str(soup)
        return response
