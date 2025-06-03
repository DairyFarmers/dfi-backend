from celery import shared_task
from django.utils import timezone
from .models import Notification
from orders.models import Order
from datetime import timedelta
from django.db.models import Q
from inventories.models import InventoryItem
from notifications.services import NotificationService
from django.contrib.auth import get_user_model
from notifications.services import EmailService
from utils import setup_logger

logger = setup_logger(__name__)

@shared_task
def send_welcome_notification(user_id):
    """Send welcome notification and email to new user"""
    try:
        User = get_user_model()
        user = User.objects.get(id=user_id)
        
        # Create notification
        notification_service = NotificationService()
        notification = notification_service.create_notification(
            notification_type='welcome',
            notification_title='Welcome to Dairy Farmers System',
            message=(
                f'Welcome {user.first_name} {user.last_name}! '
                'We\'re glad to have you on board. '
                'Feel free to explore our system and reach out if you need any help.'
            ),
            user_id=user.id,
            priority='medium',
        )
        
        # Send welcome email
        if notification:
            service = EmailService()
            email_sent = service.send_email(
                recp_email=user.email,
                recp_name=f"{user.first_name} {user.last_name}".strip(),
                subject='Welcome to Dairy Farmers!',
                title=notification.notification_title,
                message=notification.message,
            )
            
            if email_sent:
                logger.info(f"Welcome email sent to {user.email}")
                notification.sent_email = True
                notification.save(update_fields=['sent_email'])
            else:
                logger.error(f"Failed to send welcome email to {user.email}")
                
        logger.info(f"Welcome notification created for user {user.id}")
        return True
    except Exception as e:
        logger.error(f"Error sending welcome notification: {str(e)}")
        return False

@shared_task
def send_order_notification(order_id):
    """Send order notification to relevant users"""
    try:
        order = Order.objects.select_related('supplier')\
            .get(id=order_id)
        
        notification_service = NotificationService()
        
        # Notify inventory managers
        inventory_managers = get_user_model().objects.filter(
            role__name='inventory_manager'
        )
        
        for manager in inventory_managers:
            notification = notification_service.create_notification(
                notification_type='order',
                notification_title=f'New Order: {order.order_number}',
                message=(
                    f'New order ({order.order_number}) requires attention.\n'
                    f'Customer: {order.customer_name}\n'
                    f'Email: {order.customer_email}\n'
                    f'Total Amount: ${order.total_amount}\n'
                    f'Expected Delivery: {order.expected_delivery_date}\n'
                    f'Priority: {order.priority}\n'
                    f'Status: {order.status}'
                ),
                user_id=manager.id,
                priority='high',
                related_object_id=str(order.id),
                related_object_type='order'
            )
            
            if notification:
                email_service = EmailService()
                email_sent = email_service.send_email(
                    recp_email=manager.email,
                    recp_name=f"{manager.first_name} {manager.last_name}".strip(),
                    subject='New Order Notification',
                    title=notification.notification_title,
                    message=notification.message,
                )
                
                if email_sent:
                    logger.info(f"Notification email sent to {manager.email}")
                else:
                    logger.error(f"Failed to send notification email to {manager.email}")
        
        # Notify supplier if B2B order
        if order.supplier:
            notification = notification_service.create_notification(
                notification_type='order',
                notification_title=f'New Order Received: {order.order_number}',
                message=(
                    f'New order ({order.order_number}) details:\n'
                    f'Customer: {order.customer_name}\n'
                    f'Amount: ${order.total_amount}\n'
                    f'Delivery Date: {order.expected_delivery_date}\n'
                    f'Status: {order.status}\n'
                    f'Priority: {order.priority}\n'
                    f'Shipping Address: {order.shipping_address}'
                ),
                user_id=order.supplier.user.id,
                priority='high',
                related_object_id=str(order.id),
                related_object_type='order'
            )
            
            if notification:
                email_service = EmailService()
                email_sent = email_service.send_email(
                    recp_email=order.supplier.user.email,
                    recp_name=f"{order.supplier.user.first_name} {order.supplier.user.last_name}".strip(),
                    subject='New Order Notification',
                    title=notification.notification_title,
                    message=notification.message,
                )
                
                if email_sent:
                    logger.info(f"Supplier notification email sent to {order.supplier.user.email}")
                else:
                    logger.error(f"Failed to send supplier notification email to {order.supplier.user.email}")
                    
        logger.info(f"Order notifications sent for order {order_id}")
        return True
    except Exception as e:
        logger.error(f"Error sending order notifications: {str(e)}")
        return False
 
@shared_task
def send_order_status_notification(order_id, old_status):
    """Send notification when order status changes"""
    try:
        order = Order.objects.select_related('supplier')\
            .get(id=order_id)
        notification_service = NotificationService()
        
        # Define status-specific messages
        status_messages = {
            'confirmed': 'has been confirmed and is being processed',
            'processing': 'is now being processed',
            'shipped': 'has been shipped',
            'delivered': f'was delivered on {order.actual_delivery_date}',
            'cancelled': 'has been cancelled',
        }
        
        message = (
            f'Order {order.order_number} {status_messages.get(order.status, "status has changed")}.\n'
            f'Customer: {order.customer_name}\n'
            f'Amount: ${order.total_amount}'
        )

        # Notify customer via email
        notification = notification_service.create_notification(
            notification_type='order_status',
            notification_title=f'Order Status Update: {order.order_number}',
            message=message,
            user_id=order.supplier.user.id if order.supplier else None,
            priority='medium',
            related_object_id=str(order.id),
            related_object_type='order'
        )
        
        if notification:
            email_service = EmailService()
            email_sent = email_service.send_email(
                recp_email=order.customer_email,
                recp_name=order.customer_name,
                subject=f'Order Status Update: {order.order_number}',
                title=notification.notification_title,
                message=notification.message,
            )
            
            if email_sent:
                logger.info(f"Order status email sent to {order.customer_email}")
            else:
                logger.error(f"Failed to send order status email to {order.customer_email}")
    except Exception as e:
        logger.error(f"Error sending order status notification: {str(e)}")

@shared_task
def send_order_cancellation_notification(order_id: str):
    """Send notification when order is cancelled"""
    try:
        order = Order.objects.select_related('supplier').get(id=order_id)
        notification_service = NotificationService()
        
        # Notify inventory managers
        inventory_managers = get_user_model().objects.filter(
            role__name='inventory_manager'
        )
        
        message = (
            f'Order {order.order_number} has been cancelled.\n'
            f'Customer: {order.customer_name}\n'
            f'Amount: ${order.total_amount}\n'
            f'Cancellation Date: {timezone.now().strftime("%Y-%m-%d %H:%M")}'
        )

        for manager in inventory_managers:
            notification = notification_service.create_notification(
                notification_type='order_cancelled',
                notification_title=f'Order Cancelled: {order.order_number}',
                message=message,
                user_id=manager.id,
                priority='high',
                related_object_id=str(order.id),
                related_object_type='order'
            )
            
            if notification:
                email_service = EmailService()
                email_sent = email_service.send_email(
                    recp_email=manager.email,
                    recp_name=f"{manager.first_name} {manager.last_name}".strip(),
                    subject='Order Cancellation Notification',
                    title=notification.notification_title,
                    message=notification.message,
                )
                
                if email_sent:
                    logger.info(f"Cancellation notification email sent to {manager.email}")
                else:
                    logger.error(f"Failed to send cancellation notification email to {manager.email}")
    except Exception as e:
        logger.error(f"Error sending order cancellation notification: {str(e)}")

@shared_task
def send_overdue_delivery_notification(order_id: str):
    """Send notification for overdue deliveries"""
    try:
        order = Order.objects.select_related('supplier').get(id=order_id)
        notification_service = NotificationService()
        
        message = (
            f'Order {order.order_number} is overdue for delivery.\n'
            f'Expected Delivery: {order.expected_delivery_date}\n'
            f'Customer: {order.customer_name}\n'
            f'Amount: ${order.total_amount}\n'
            f'Current Status: {order.status}'
        )

        # Notify managers and supplier
        recipients = list(get_user_model().objects.filter(
            role__name='inventory_manager'
        ))
        
        if order.supplier and hasattr(order.supplier, 'user'):
            recipients.append(order.supplier.user)

        for recipient in recipients:
            notification = notification_service.create_notification(
                notification_type='order_overdue',
                notification_title=f'Overdue Order Alert: {order.order_number}',
                message=message,
                user_id=recipient.id,
                priority='high',
                related_object_id=str(order.id),
                related_object_type='order'
            )
            
            if notification:
                email_service = EmailService()
                email_sent = email_service.send_email(
                    recp_email=recipient.email,
                    recp_name=f"{recipient.first_name} {recipient.last_name}".strip(),
                    subject='Overdue Order Notification',
                    title=notification.notification_title,
                    message=notification.message,
                )
                
                if email_sent:
                    logger.info(f"Overdue delivery notification email sent to {recipient.email}")
                else:
                    logger.error(f"Failed to send overdue delivery notification email to {recipient.email}")
    except Exception as e:
        logger.error(f"Error sending overdue delivery notification: {str(e)}")

@shared_task
def check_overdue_orders():
    """Check for overdue orders daily"""
    try:
        overdue_orders = Order.objects.filter(
            status__in=['confirmed', 'processing', 'shipped'],
            expected_delivery_date__lt=timezone.now().date(),
            actual_delivery_date__isnull=True
        )
        
        for order in overdue_orders:
            send_overdue_delivery_notification.delay(str(order.id))
            
        logger.info(f"Checked {overdue_orders.count()} overdue orders")
        
    except Exception as e:
        logger.error(f"Error checking overdue orders: {str(e)}")
                
@shared_task
def check_inventory_expiry():
    """Check inventory items for expiry and create notifications"""
    notification_service = NotificationService()
    expiry_threshold = timezone.now().date() + timedelta(days=30)
    
    # Get items expiring in next 30 days
    expiring_items = InventoryItem.objects.filter(
        Q(expiry_date__lte=expiry_threshold) & 
        Q(quantity__gt=0)
    ).select_related('supplier')

    logger.info(f"Found {expiring_items.count()} items expiring within 30 days")

    for item in expiring_items:
        days_until_expiry = (item.expiry_date - timezone.now().date()).days
        priority = 'high' if days_until_expiry <= 7 else 'medium'
        
        # Get users to notify based on roles
        inventory_managers = get_user_model().objects.filter(
            role__name='inventory_manager'
        )
        admins = get_user_model().objects.filter(
            role__name='admin'
        )
        
        for user in inventory_managers:
            notification = notification_service.create_notification(
                notification_type='expiry',
                title=f'Inventory Alert: Product Expiring Soon',
                message=(f'Product {item.name} (Batch: {item.batch_number}) '
                        f'will expire in {days_until_expiry} days. '
                        f'Current quantity: {item.quantity}. '
                        f'Please take necessary action.'),
                user_id=user.id,
                priority=priority,
                related_object_id=str(item.id),
                related_object_type='inventory_item'
            )
            send_notification_email.delay(notification.id)
            
        for user in admins:
            notification = notification_service.create_notification(
                notification_type='expiry',
                title=f'Admin Alert: Expiring Inventory',
                message=(f'Product {item.name} from supplier {item.supplier.name} '
                        f'will expire in {days_until_expiry} days. '
                        f'Quantity: {item.quantity}. '
                        f'Please review inventory management.'),
                user_id=user.id,
                priority=priority,
                related_object_id=str(item.id),
                related_object_type='inventory_item'
            )
            send_notification_email.delay(notification.id)
        
        logger.info(f"Created expiry notification for item {item.name}")
        
    return f"Processed {expiring_items.count()} expiring items"

@shared_task
def process_notification_queue():
    """Process pending notifications and send emails"""
    notifications = Notification.objects.filter(
        sent_email=False,
        created_at__gte=timezone.now() - timezone.timedelta(days=1)
    )
    print('Processing notifications:', notifications.count())
    
    for notification in notifications:
        try:
            send_notification_email.delay(notification.id)
        except Exception as e:
            logger.error(f"Failed to queue email for notification {notification.id}: {str(e)}")

@shared_task
def send_notification_email(notification_id):
    """Send email for a specific notification"""
    try:
        notification = Notification.objects.get(id=notification_id)
        full_name = f"{notification.user.first_name} \
            {notification.user.last_name}".strip()
        service = EmailService()
        email_sent = service.send_product_expiry_email(
            notification.user.email, 
            full_name,
            notification.priority,
            notification.notification_title,
            notification.message,
        )
        
        if email_sent:
            logger.info(f"Email sent for notification \
                {notification_id} to {notification.user.email}")
            notification.sent_email = True
            notification.save(update_fields=['sent_email', 'updated_at'])
        else:
            logger.error(f"Failed to send email for notification \
                {notification_id}")
        
        logger.info(f"Email sent for notification \
            {notification_id} to {notification.user.email}")
        notification.sent_email = True
        notification.save(update_fields=['sent_email', 'updated_at'])
    except Exception as e:
        logger.error(
            f"Error in send_notification_email for \
                {notification_id}: {str(e)}"
            )
