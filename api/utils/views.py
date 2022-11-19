from rest_framework.views import APIView
from rest_framework.response import Response


class PostView(APIView):
    serializer_class = None
    send_request_to_serializer = False
    object_permissions = None
    filter_data_to_response = None
    message_to_response = None
    instance = None
    status = 200
    saving = False
    no_content = False

    def post(self, request):
        if self.send_request_to_serializer:
            if not self.instance:
                serializer = self.serializer_class(data=request.data, context={"request": request})
            else:
                serializer = self.serializer_class(
                    data=request.data, instance=self.instance, context={"request": request})
        else:
            if not self.instance:
                serializer = self.serializer_class(data=request.data)
            else:
                serializer = self.serializer_class(data=request.data, instance=self.instance)

        serializer.is_valid(raise_exception=True)

        if self.message_to_response:
            return Response(data={"message": self.message_to_response}, status=self.status)
        elif self.filter_data_to_response:
            return Response(data=serializer.validated_data.get(self.filter_data_to_response), status=self.status)
        elif self.no_content:
            return Response(status=self.status)
        return Response(data=serializer.validated_data, status=self.status)
