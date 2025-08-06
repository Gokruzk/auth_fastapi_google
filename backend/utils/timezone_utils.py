"""
Utilidades para manejo de zonas horarias UTC-5 (Ecuador)
"""

from datetime import datetime, timezone, timedelta


class TimezoneUtils:
    """Clase para manejar conversiones de zona horaria UTC-5"""

    # Definir zona horaria UTC-5 (Ecuador)
    ECUADOR_TZ = timezone(timedelta(hours=-5))

    @staticmethod
    def utc_to_ecuador(utc_datetime: datetime) -> datetime:
        """
        Convierte un datetime UTC a UTC-5 (Ecuador)

        Args:
            utc_datetime: datetime en UTC

        Returns:
            datetime en UTC-5
        """
        if utc_datetime.tzinfo is None:
            utc_datetime = utc_datetime.replace(tzinfo=timezone.utc)

        return utc_datetime.astimezone(TimezoneUtils.ECUADOR_TZ)

    @staticmethod
    def ecuador_to_utc(ecuador_datetime: datetime) -> datetime:
        """
        Convierte un datetime en UTC-5 a UTC

        Args:
            ecuador_datetime: datetime en UTC-5

        Returns:
            datetime en UTC
        """
        if ecuador_datetime.tzinfo is None:
            ecuador_datetime = ecuador_datetime.replace(
                tzinfo=TimezoneUtils.ECUADOR_TZ)

        return ecuador_datetime.astimezone(timezone.utc)

    @staticmethod
    def now_ecuador() -> datetime:
        """
        Obtiene la fecha y hora actual en UTC-5 (Ecuador)

        Returns:
            datetime actual en UTC-5
        """
        return datetime.now(TimezoneUtils.ECUADOR_TZ)

    @staticmethod
    def now_for_database() -> datetime:
        """
        Obtiene la fecha y hora actual en UTC-5 para guardar en la base de datos

        Este método debe ser usado cuando se vaya a guardar un timestamp en la base de datos
        para garantizar que todo se almacene en UTC-5

        Returns:
            datetime actual en UTC-5 (timezone-aware)
        """
        return datetime.now(TimezoneUtils.ECUADOR_TZ)

    @staticmethod
    def now_utc() -> datetime:
        """
        Obtiene la fecha y hora actual en UTC

        Returns:
            datetime actual en UTC
        """
        return datetime.now(timezone.utc)

    @staticmethod
    def to_date_ecuador(utc_datetime: datetime) -> datetime:
        """
        Convierte un datetime UTC a fecha en UTC-5 (solo fecha, sin hora)

        Args:
            utc_datetime: datetime en UTC

        Returns:
            date en UTC-5
        """
        ecuador_dt = TimezoneUtils.utc_to_ecuador(utc_datetime)
        return ecuador_dt.date()

    @staticmethod
    def to_time_ecuador(utc_datetime: datetime) -> datetime:
        """
        Convierte un datetime UTC a tiempo en UTC-5 (solo hora, sin fecha)

        Args:
            utc_datetime: datetime en UTC

        Returns:
            time en UTC-5
        """
        ecuador_dt = TimezoneUtils.utc_to_ecuador(utc_datetime)
        return ecuador_dt.time()

    @staticmethod
    def combine_date_time_ecuador(date_val, time_val) -> datetime:
        """
        Combina fecha y hora en UTC-5 y devuelve datetime con timezone

        Args:
            date_val: fecha
            time_val: hora

        Returns:
            datetime combinado en UTC-5
        """
        combined = datetime.combine(date_val, time_val)
        return combined.replace(tzinfo=TimezoneUtils.ECUADOR_TZ)

    @staticmethod
    def format_for_display(
        utc_datetime: datetime, format_str: str = "%Y-%m-%d %H:%M:%S"
    ) -> str:
        """
        Formatea un datetime UTC para mostrar en UTC-5

        Args:
            utc_datetime: datetime en UTC
            format_str: formato de salida

        Returns:
            string formateado en UTC-5
        """
        ecuador_dt = TimezoneUtils.utc_to_ecuador(utc_datetime)
        return ecuador_dt.strftime(format_str)

    @staticmethod
    def parse_from_input(
        datetime_str: str, format_str: str = "%Y-%m-%d %H:%M:%S"
    ) -> datetime:
        """
        Parsea un string de fecha/hora asumiendo que está en UTC-5

        Args:
            datetime_str: string de fecha/hora
            format_str: formato de entrada

        Returns:
            datetime en UTC-5
        """
        dt = datetime.strptime(datetime_str, format_str)
        return dt.replace(tzinfo=TimezoneUtils.ECUADOR_TZ)

    @staticmethod
    def get_start_of_day_ecuador(date_val=None) -> datetime:
        """
        Obtiene el inicio del día (00:00:00) en UTC-5

        Args:
            date_val: fecha específica (opcional, por defecto hoy)

        Returns:
            datetime del inicio del día en UTC-5
        """
        if date_val is None:
            date_val = TimezoneUtils.now_ecuador().date()

        return datetime.combine(date_val, datetime.min.time()).replace(
            tzinfo=TimezoneUtils.ECUADOR_TZ
        )

    @staticmethod
    def get_end_of_day_ecuador(date_val=None) -> datetime:
        """
        Obtiene el fin del día (23:59:59) en UTC-5

        Args:
            date_val: fecha específica (opcional, por defecto hoy)

        Returns:
            datetime del fin del día en UTC-5
        """
        if date_val is None:
            date_val = TimezoneUtils.now_ecuador().date()

        return datetime.combine(date_val, datetime.max.time()).replace(
            tzinfo=TimezoneUtils.ECUADOR_TZ
        )

    @staticmethod
    def ensure_utc_minus_5(dt: datetime) -> datetime:
        """
        Asegura que un datetime esté en UTC-5 (Ecuador)

        Args:
            dt: datetime a convertir

        Returns:
            datetime en UTC-5
        """
        if dt.tzinfo is None:
            # Si no tiene timezone, asumir que está en UTC-5
            return dt.replace(tzinfo=TimezoneUtils.ECUADOR_TZ)
        else:
            # Si tiene timezone, convertir a UTC-5
            return dt.astimezone(TimezoneUtils.ECUADOR_TZ)

    @staticmethod
    def convert_to_utc_minus_5_for_db(dt: datetime) -> datetime:
        """
        Convierte cualquier datetime a UTC-5 para almacenamiento en base de datos

        Este método garantiza que cualquier fecha/hora se almacene en UTC-5
        independientemente de su timezone original

        Args:
            dt: datetime a convertir

        Returns:
            datetime en UTC-5 listo para almacenar en BD
        """
        if dt.tzinfo is None:
            # Si no tiene timezone, asumir que está en UTC-5
            return dt.replace(tzinfo=TimezoneUtils.ECUADOR_TZ)
        else:
            # Si tiene timezone, convertir a UTC-5
            return dt.astimezone(TimezoneUtils.ECUADOR_TZ)

    @staticmethod
    def parse_date_to_utc_minus_5(date_string: str) -> datetime:
        """
        Parsea una fecha string y la convierte a UTC-5

        Args:
            date_string: fecha en formato ISO

        Returns:
            datetime en UTC-5
        """
        dt = datetime.fromisoformat(date_string)
        return TimezoneUtils.convert_to_utc_minus_5_for_db(dt)
