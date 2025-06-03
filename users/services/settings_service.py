from typing import Optional, Dict
from exceptions.exceptions import ServiceException
from django.db import transaction
from utils import setup_logger

logger = setup_logger(__name__)

class UserSettingsService:
    def __init__(self, settings_repository):
        self.settings_repository = settings_repository

    def get_default_privacy_settings(self) -> Dict:
        """Return default privacy settings"""
        return {
            "share_contact_info": False,
            "share_location": False,
            "share_inventory": False,
            "share_analytics": False,
            "allow_marketing": False
        }
        
    def create_default_settings(self, user_id: str):
        """Create default settings for new user"""
        try:
            return self.settings_repository.create({
                "user_id": user_id,
                "privacy_settings": self.get_default_privacy_settings(),
                "is_active": True
            })
        except Exception as e:
            logger.error(f"Error creating default settings: {str(e)}")
            raise ServiceException(str(e))

    @transaction.atomic
    def get_user_settings(self, user_id) -> Optional[Dict]:
        """Get or create user settings with all related data"""
        try:
            settings = self.settings_repository.get_by_user_id(user_id)
            
            if not settings:
                logger.info(f"Creating default settings for user {user_id}")
                settings = self.create_default_settings(user_id)
                
            contact_info = getattr(settings.user, 'contact', None)
            locations = list(settings.user.locations.filter(
                is_active=True
            )) if hasattr(settings.user, 'locations') else []

            return {
                'privacy_settings': settings.privacy_settings or \
                    self.get_default_privacy_settings(),
                'user': {
                    'id': str(settings.user.id),
                    'first_name': settings.user.first_name,
                    'last_name': settings.user.last_name,
                    'email': settings.user.email,
                    'contact': {
                        'phone_primary': contact_info.phone_primary \
                            if contact_info else None,
                        'phone_secondary': contact_info.phone_secondary \
                            if contact_info else None,
                    } if contact_info else {
                        'phone_primary': None,
                        'phone_secondary': None,
                    },
                    'locations': [{
                        'id': str(loc.id),
                        'type': loc.location_type,
                        'is_primary': loc.is_primary,
                        'address': f"{loc.address_line1}, {loc.city}, {loc.state}"
                    } for loc in locations] if locations else [],
                    'created_at': settings.user.date_joined,
                    'last_login': settings.user.last_login
                },
                'role': {
                    'name': settings.user.role.name,
                    'description': settings.user.role.description,
                    'priority': settings.user.role.priority,
                    'permissions': settings.user.role.get_all_permissions()
                } if settings.user.role else None
            }
        except Exception as e:
            logger.error(f"Service error getting user settings: {str(e)}")
            raise ServiceException(str(e))

    def update_settings(self, user_id: str, data: Dict) -> Optional[Dict]:
        """Update user settings with validation"""
        try:
            settings = self.settings_repository.get_by_user_id(user_id)
            
            if not settings:
                return None

            # Validate preference types
            valid_preferences = {
                'privacy_settings'
            }

            invalid_prefs = set(data.keys()) - valid_preferences
            if invalid_prefs:
                raise ServiceException(f"Invalid preference types: {invalid_prefs}")

            updated_settings = self.settings_repository.update(
                settings.id,
                data
            )
            return self.get_user_settings(user_id)
        except Exception as e:
            logger.error(f"Service error updating user settings: {str(e)}")
            raise ServiceException(str(e))

    def update_specific_preference(
        self,
        user_id: str,
        preference_type: str,
        preference_data: Dict
    ) -> Optional[Dict]:
        """Update a specific preference type"""
        try:
            return self.settings_repository.update_specific_preference(
                user_id,
                preference_type,
                preference_data
            )
        except Exception as e:
            logger.error(f"Service error updating {preference_type}: {str(e)}")
            raise ServiceException(str(e))