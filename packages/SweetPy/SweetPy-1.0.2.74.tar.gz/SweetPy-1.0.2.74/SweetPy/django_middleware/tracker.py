from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseServerError
from ..tracker import Tracker
from ..extend.response_plus import create_data,APIResponseHTTPCode
from ..func_plus import FuncHelper


class request_tracker(MiddlewareMixin):

    def process_request(self, request):
        tracker = Tracker(request)
        request.tracker = tracker
        return None

    def process_response(self, request, response):
        if hasattr(request,'tracker'):
            request.tracker.end()
        return response

    def process_exception(self, request, exception):
        if hasattr(request,'tracker'):
            request.tracker.set_excetion(exception)
        print(exception)
        data = create_data(APIResponseHTTPCode.FAIL)
        data['message'] = str(exception)
        data = FuncHelper.dict_to_json(data)
        return HttpResponseServerError(data)

    # def process_view(request, view_func, view_args, view_kwargs)
    #     process_template_response(request, response)