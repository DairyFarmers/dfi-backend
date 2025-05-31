from reports.models.report import Report
from django.utils.timezone import now
from users.models import UserActivityLog
from orders.models import Order
from inventories.models import InventoryItem
from django.db.models import Sum, Count
from django.core.files.base import ContentFile
import pandas as pd
import io
from reports.utils.pdf_generator import PDFGenerator
from reports.repositories.report_repository import ReportRepository
from exceptions import DatabaseException

class ReportService:
    @staticmethod
    def generate_report(user, report_type, date_from, date_to, format='pdf', filters=None):
        """Generate report based on type and parameters"""
        report_generators = {
            'sales': ReportService._generate_sales_report,
            'inventory': ReportService._generate_inventory_report,
            'orders': ReportService._generate_orders_report,
            'user_activity': ReportService._generate_user_activity_report,
        }
        
        if report_type not in report_generators:
            raise ValueError(f"Invalid report type: {report_type}")

        # Generate report data
        data = report_generators[report_type](date_from, date_to, filters)
        
        # Create report record
        report = Report.objects.create(
            report_type=report_type,
            format=format,
            generated_by=user,
            date_from=date_from,
            date_to=date_to,
            filters=filters or {}
        )

        # Generate file based on format
        file_content = ReportService._generate_file(data, format)
        filename = f"{report_type}_report_{now().strftime('%Y%m%d_%H%M%S')}.{format}"
        report.file.save(filename, ContentFile(file_content), save=True)

        return report

    @staticmethod
    def delete_report(report_id: str, user) -> bool:
        try:
            repository = ReportRepository()
            return repository.delete_report(report_id, user.id)
        except DatabaseException as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Failed to delete report: {str(e)}")
            
    @staticmethod
    def _generate_sales_report(date_from, date_to, filters=None):
        queryset = Order.objects.filter(
            created_at__range=[date_from, date_to]
        )

        if filters:
            queryset = queryset.filter(**filters)

        data = {
            'summary': {
                'total_sales': queryset.aggregate(total=Sum('total_amount'))['total'] or 0,
                'total_orders': queryset.count(),
                'average_order_value': queryset.aggregate(
                    avg=Sum('total_amount')/Count('id')
                )['avg'] or 0
            },
            'orders': list(queryset.values(
                'id', 
                'order_number', 
                'customer_email',  # Changed from customer__email
                'total_amount', 
                'status', 
                'created_at'
            ))
        }
        return data

    @staticmethod
    def _generate_inventory_report(date_from, date_to, filters=None):
        queryset = InventoryItem.objects.filter(
            updated_at__range=[date_from, date_to]
        )

        if filters:
            queryset = queryset.filter(**filters)

        data = {
            'summary': {
                'total_items': queryset.count(),
                'low_stock_items': queryset.filter(quantity__lte=10).count(),
                'total_value': queryset.aggregate(
                    total=Sum('quantity') * Sum('price')
                )['total'] or 0
            },
            'items': list(queryset.values(
            'id', 
            'name', 
            'quantity', 
            'price',
            'dairy_type',
            'storage_condition',
            'expiry_date',
            'reorder_point',
            'updated_at'
        ))
        }
        return data

    @staticmethod
    def _generate_user_activity_report(date_from, date_to, filters=None):
        queryset = UserActivityLog.objects.filter(
            timestamp__range=[date_from, date_to]
        )

        if filters:
            queryset = queryset.filter(**filters)

        data = {
            'summary': {
                'total_activities': queryset.count(),
                'unique_users': queryset.values('user').distinct().count()
            },
            'activities': list(queryset.values(
                'user__email', 'action', 'timestamp',
                'ip_address', 'details'
            ))
        }
        return data

    @staticmethod
    def _generate_file(data, format):
        """Generate file in specified format"""
        if format == 'pdf':
            return ReportService._generate_pdf(data)
        elif format == 'excel':
            return ReportService._generate_excel(data)
        elif format == 'csv':
            return ReportService._generate_csv(data)
        else:
            raise ValueError(f"Unsupported format: {format}")

    @staticmethod
    def _generate_orders_report(date_from, date_to, filters=None):
        queryset = Order.objects.filter(
            created_at__range=[date_from, date_to]
        )

        if filters:
            queryset = queryset.filter(**filters)

        data = {
            'summary': {
                'total_orders': queryset.count(),
                'total_value': queryset.aggregate(total=Sum('total_amount'))['total'] or 0,
                'pending_orders': queryset.filter(status='pending').count(),
                'completed_orders': queryset.filter(status='completed').count()
            },
            'orders': list(queryset.values(
                'id', 
                'order_number',
                'customer_email',  # Changed from customer__email
                'customer_name',
                'total_amount',
                'status',
                'created_at',
                'expected_delivery_date',  # Changed from delivery_date
                'payment_status'
            ).order_by('-created_at'))
        }
        return data

    @staticmethod
    def _generate_pdf(data):
        return PDFGenerator.generate_pdf(data)

    @staticmethod
    def _generate_excel(data):
        output = io.BytesIO()
        
        # Create Excel writer
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Write summary
            pd.DataFrame([data['summary']]).to_excel(writer, sheet_name='Summary', index=False)
            
            # Write details
            detail_key = next(k for k in data.keys() if k != 'summary')
            pd.DataFrame(data[detail_key]).to_excel(writer, sheet_name='Details', index=False)

        return output.getvalue()

    @staticmethod
    def _generate_csv(data):
        output = io.StringIO()
        
        # Get the detail data (orders, items, or activities)
        detail_key = next(k for k in data.keys() if k != 'summary')
        
        # Convert to DataFrame and save as CSV
        df = pd.DataFrame(data[detail_key])
        df.to_csv(output, index=False)
        
        return output.getvalue().encode('utf-8')