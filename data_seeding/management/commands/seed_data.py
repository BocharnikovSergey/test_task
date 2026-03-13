import csv

from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import Role
from permissions.models import BusinessElement, PermissionRoleRule


class Command(BaseCommand):
    """Команда для наполнения БД данными."""

    help = 'Наполняет базу данными.'

    def handle(self, *args, **options):
        self.load_simple_csv_to_model(
            model=Role, data_path=settings.DATA_DIR / 'roles.csv'
        )
        self.load_simple_csv_to_model(
            model=BusinessElement,
            data_path=settings.DATA_DIR / 'business_element.csv'
        )
        self.load_csv_permissions(
            data_path=settings.DATA_DIR / 'permissions.csv'
        )
        self.stdout.write(self.style.SUCCESS('Команда выполнена'))

    def load_simple_csv_to_model(self, model, data_path):
        try:
            with open(data_path, 'r', encoding='utf-8') as data_files:
                for data in csv.DictReader(data_files):
                    model.objects.get_or_create(**data)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Данные успешно загружены в {model.__name__}'
                )
            )
        except FileNotFoundError:
            self.stdout.write(
                self.style.WARNING(f'Файл не найден {data_path}')
            )
        except Exception as error:
            self.stdout.write(
                self.style.ERROR(f'Ошибка: {str(error)}')
            )

    def load_csv_permissions(self, data_path):
        try:
            with open(data_path, 'r', encoding='utf-8') as data_files:
                for data in csv.DictReader(data_files):
                    data['role'] = Role.objects.filter(
                        name=data['role']
                    ).first()
                    data['element'] = BusinessElement.objects.filter(
                        name=data['element']
                    ).first()
                    PermissionRoleRule.objects.get_or_create(**data)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Данные успешно загружены в {PermissionRoleRule.__name__}'
                )
            )
        except FileNotFoundError:
            self.stdout.write(
                self.style.WARNING(f'Файл не найден {data_path}')
            )
        except Exception as error:
            self.stdout.write(
                self.style.ERROR(f'Ошибка: {str(error)}')
            )
