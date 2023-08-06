import pytz
from copy import copy
from datetime import datetime, date
from decimal import Decimal
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from amaascore.core.amaas_model import AMaaSModel
from amaascore.transactions.pnl_amount import PnlAmount


class Pnl(AMaaSModel):

    def __init__(self, asset_manager_id, pnl_type,
                 book_id, business_date, pnl_timestamp,
                 currency, quantity=None, asset_id=None,
                 transaction_id=None, transaction_date=None,
                 DTD=None, MTD=None, YTD=None,
                 *args, **kwargs):
        self.asset_manager_id = asset_manager_id
        self.pnl_type = pnl_type
        self.book_id = book_id
        self.business_date = business_date
        self.pnl_timestamp = pnl_timestamp
        self.currency = currency
        self.quantity = quantity
        self.asset_id = asset_id
        self.transaction_id = transaction_id
        self.transaction_date = transaction_date
        self.DTD = copy(DTD)
        self.MTD = copy(MTD)
        self.YTD = copy(YTD)

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, Decimal) and value is not None:
            self._quantity = Decimal(value)
        else:
            self._quantity = value

    @property
    def asset_manager_id(self):
        if hasattr(self, '_asset_manager_id'):
            return self._asset_manager_id

    @asset_manager_id.setter
    def asset_manager_id(self, value):
        self._asset_manager_id = int(value)

    @property
    def DTD(self):
        return self._DTD

    @DTD.setter
    def DTD(self, value):
        if value is None:
            self._DTD = None
        elif isinstance(value, dict):
            self._DTD = PnlAmount(**value)
        elif isinstance(value, PnlAmount):
            self._DTD = value
        else:
            raise TypeError('Invalid type for DTD')

    @property
    def MTD(self):
        return self._MTD

    @MTD.setter
    def MTD(self, value):
        if value is None:
            self._MTD = None
        elif isinstance(value, dict):
            self._MTD = PnlAmount(**value)
        elif isinstance(value, PnlAmount):
            self._MTD = value
        else:
            raise TypeError('Invalid type for MTD')

    @property
    def YTD(self):
        return self._YTD

    @YTD.setter
    def YTD(self, value):
        if value is None:
            self._YTD = None
        elif isinstance(value, dict):
            self._YTD = PnlAmount(**value)
        elif isinstance(value, PnlAmount):
            self._YTD = value
        else:
            raise TypeError('Invalid type for YTD')

    @property
    def pnl_type(self):
        return self._pnl_type

    @pnl_type.setter
    def pnl_type(self, value):
        if value not in ['Position', 'Transaction']:
            raise ValueError('Invalid value for "Pnl Type"')
        self._pnl_type = value

    @property
    def business_date(self):
        if hasattr(self, '_business_date'):
            return self._business_date

    @business_date.setter
    def business_date(self, value):
        if value is None:
            raise ValueError('Missing required attribute "Business Date".')

        if isinstance(value, str):
            self._business_date = parse(value).date()
        elif isinstance(value, datetime):
            self._business_date = value.date()
        elif isinstance(value, date):
            self._business_date = value
        else:
            raise TypeError('Invalid type for attribute "Business Date".')

    @property
    def pnl_timestamp(self):
        return self._pnl_timestamp

    @pnl_timestamp.setter
    def pnl_timestamp(self, value):
        if value is None:
            raise ValueError('Missing required attribute "Pnl Timestamp".')

        parsed_value = None
        if isinstance(value, str):
            parsed_value = parse(value)
        elif isinstance(value, datetime):
            parsed_value = value
        elif isinstance(value, date):
            parsed_value = datetime.combine(value, datetime.min.time())
        else:
            raise TypeError('Invalid type for attribute "Pnl Timestamp".')

        if parsed_value is None:
            raise ValueError('Unable to parse {} into a "Pnl Timestamp".'.format(str(value)))
        else:
            self._pnl_timestamp = parsed_value.replace(tzinfo=pytz.UTC) \
                                  if not parsed_value.tzinfo else parsed_value

    @property
    def transaction_date(self):
        if hasattr(self, '_transaction_date'):
            return self._transaction_date

    @transaction_date.setter
    def transaction_date(self, value):
        if value is None:
            self._transaction_date = None
        elif isinstance(value, str):
            self._transaction_date = parse(value).date()
        elif isinstance(value, datetime):
            self._transaction_date = value.date()
        elif isinstance(value, date):
            self._transaction_date = value
        else:
            raise TypeError('Invalid type for attribute "Transaction Date".')