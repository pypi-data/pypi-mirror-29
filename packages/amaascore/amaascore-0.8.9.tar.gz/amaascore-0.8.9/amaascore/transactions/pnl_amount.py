import json
from decimal import Decimal
from amaascore.core.amaas_model import AMaaSModel

class PnlAmount(AMaaSModel):


    def __init__(self, total_pnl=None, asset_pnl=None, fx_pnl=None,
                 realised_pnl=None, unrealised_pnl=None,
                 additional=None, error_message=None):
        self.total_pnl = total_pnl
        self.asset_pnl = asset_pnl
        self.fx_pnl = fx_pnl
        self.realised_pnl = realised_pnl
        self.unrealised_pnl = unrealised_pnl
        self.additional = additional
        self.error_message = error_message
    
    @property
    def asset_pnl(self):
        return self._asset_pnl

    @asset_pnl.setter
    def asset_pnl(self, val):
        if not isinstance(val, Decimal) and val is not None:
            self._asset_pnl = Decimal(val)
        else:
            self._asset_pnl = val

    @property
    def fx_pnl(self):
        return self._fx_pnl

    @fx_pnl.setter
    def fx_pnl(self, val):
        if not isinstance(val, Decimal) and val is not None:
            self._fx_pnl = Decimal(val)
        else:
            self._fx_pnl = val

    @property
    def total_pnl(self):
        return self._total_pnl

    @total_pnl.setter
    def total_pnl(self, val):
        if not isinstance(val, Decimal) and val is not None:
            self._total_pnl = Decimal(val)
        else:
            self._total_pnl = val

    @property
    def unrealised_pnl(self):
        return self._unrealised_pnl

    @unrealised_pnl.setter
    def unrealised_pnl(self, val):
        if not isinstance(val, Decimal) and val is not None:
            self._unrealised_pnl = Decimal(val)
        else:
            self._unrealised_pnl = val

    @property
    def realised_pnl(self):
        return self._realised_pnl

    @realised_pnl.setter
    def realised_pnl(self, val):
        if not isinstance(val, Decimal) and val is not None:
            self._realised_pnl = Decimal(val)
        else:
            self._realised_pnl = val

    @property
    def additional(self):
        if hasattr(self, '_additional'):
            return self._additional

    @additional.setter
    def additional(self, val):
        if val:
            if isinstance(val, str):
                self._additional = json.loads(val)
            elif isinstance(val, dict):
                self._additional = val
            else:
                raise TypeError('Unsupported data type for additional.')