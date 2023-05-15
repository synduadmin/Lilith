'''# studio/api_views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AssetSerializer
from .models import Asset

@api_view(['POST'])
def asset_request_api(request):
    if request.method == 'POST':
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            # Save the Asset instance
            asset = serializer.save()

            # Fetch and store the asset as done in the process_asset view
            # You might need to refactor the asset fetching and storing logic into a separate function
            # so that it can be reused here and in the process_asset view

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''