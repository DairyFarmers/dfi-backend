from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from reports.models.report import Report
from reports.serializers.report_serializer import ReportSerializer
from django.core.paginator import Paginator
from utils import setup_logger

logger = setup_logger(__name__)

class ReportListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ReportSerializer(many=True)})
    def get(self, request):
        try:
            logger.info(f"{request.user} is retrieving their reports")
            reports = Report.objects.filter(
                generated_by=request.user
            ).select_related('generated_by')

            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('size', 10)
            paginator = Paginator(reports, page_size)
            current_page = paginator.get_page(page)
            serializer = ReportSerializer(
                current_page.object_list, 
                many=True,
                context={'request': request}
            )
            return Response({
                'status': True,
                'message': 'Reports retrieved successfully',
                'data': {
                    'results': serializer.data,
                    'count': paginator.count,
                    'num_pages': paginator.num_pages,
                    'next': current_page.number + 1 if current_page.has_next() else None,
                    'previous': current_page.number - 1 if current_page.has_previous() else None
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving reports: {e}")
            return Response(
                {"error": "Failed to retrieve reports"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
