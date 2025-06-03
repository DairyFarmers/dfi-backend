from typing import Optional, Dict
from django.db import transaction
from exceptions.exceptions import RepositoryException
from utils import setup_logger

logger = setup_logger(__name__)

class UserSettingsRepository:
    def __init__(self, model):
        self.model = model
        
    def create(self, data: Dict) -> Optional[Dict]:
        """Create new user settings with defaults"""
        try:
            with transaction.atomic():
                settings = self.model.objects.create(**data)
                settings.initialize_defaults()
                return settings
        except Exception as e:
            logger.error(
                f"Repository error creating user settings: {str(e)}"
            )
            raise RepositoryException(str(e))

    def get_by_user_id(self, user_id) -> Optional[Dict]:
        """Get settings by user ID with related data"""
        try:
            settings = self.model.objects.select_related(
                'user',
                'user__contact'
            ).prefetch_related(
                'user__locations',
                'user__role'
            ).get(
                user_id=user_id,
                is_active=True
            )
            return settings
        except self.model.DoesNotExist:
            return None
        except Exception as e:
            logger.error(
                f"Repository error getting user settings: {str(e)}"
            )
            raise RepositoryException(str(e))

    def update(self, settings_id, data: Dict) -> Optional[Dict]:
        """Update user settings with validation"""
        try:
            with transaction.atomic():
                settings = self.model.objects.get(
                    id=settings_id, 
                    is_active=True
                )
                
                if 'privacy_settings' in data:
                    settings.privacy_settings.update(
                        data['privacy_settings']
                    )
                
                settings.save()
                return settings
        except self.model.DoesNotExist:
            return None
        except Exception as e:
            logger.error(
                f"Repository error updating user settings: {str(e)}"
            )
            raise RepositoryException(str(e))

    def update_specific_preference(
        self, 
        user_id, 
        preference_type, 
        preference_data: Dict
    ) -> Optional[Dict]:
        """Update a specific preference type"""
        try:
            with transaction.atomic():
                settings = self.get_by_user_id(user_id)
                
                if not settings:
                    return None

                valid_preferences = [
                    'privacy_settings'
                ]

                if preference_type not in valid_preferences:
                    raise RepositoryException(
                        f"Invalid preference type: {preference_type}"
                    )

                current_preferences = getattr(settings, preference_type)
                current_preferences.update(preference_data)
                setattr(settings, preference_type, current_preferences)
                settings.save()
                return settings
        except Exception as e:
            logger.error(
                f"Repository error updating {preference_type}: {str(e)}"
            )
            raise RepositoryException(str(e))

    def bulk_update_preferences(
        self, 
        user_id, 
        preferences: Dict
    ) -> Optional[Dict]:
        """Bulk update multiple preference types"""
        try:
            with transaction.atomic():
                settings = self.get_by_user_id(user_id)
                
                if not settings:
                    return None

                for pref_type, pref_data in preferences.items():
                    self.update_specific_preference(
                        user_id,
                        pref_type,
                        pref_data
                    )

                return settings
        except Exception as e:
            logger.error(
                f"Repository error bulk updating preferences: {str(e)}"
            )
            raise RepositoryException(str(e))