import datetime

from market_simulator.models  import DailySymbolData
from strategies.utils         import get_num_trading_sessions
from strategies.base_strategy import BaseStrategy


class BearishHaramiChartStrategy(BaseStrategy):

    def is_bearish_harami(self, symbol_data):
        # Check last body
        last_dsd = symbol_data.get_dsd_x_days_back(1)
        if not last_dsd.is_bullish_body():
            self.confidence_metrics['last_body'] = 0
            return False
        else:
            self.confidence_metrics['last_body'] = 1

        # Check if current body is bullish
        if not symbol_data.is_bearish_body():
            self.confidence_metrics['current_body_trend'] = 0
            return False
        else:
            self.confidence_metrics['current_body_trend'] = 1

        if (last_dsd.close_price > symbol_data.start_price) and (last_dsd.start_price < symbol_data.close_price):
            self.confidence_metrics['harami'] = 1
        else:
            return False

        self.extra_info['stoploss'] = max(last_dsd.high_price, symbol_data.high_price)

        return True

    def run(self,
            symbol,
            market_data_source,
            date_start=datetime.date.today() - datetime.timedelta(days=1),
            date_end=datetime.date.today()):
        symbol_data = DailySymbolData.objects.filter(symbol=symbol,
                                                     data_souce=market_data_source,
                                                     date=date_end)
        if symbol_data.exists():
            symbol_data = DailySymbolData.objects.get(symbol=symbol,
                                                      data_souce=market_data_source,
                                                      date=date_end)
            is_bearish_harami = self.is_bearish_harami(symbol_data)
            day_difference = get_num_trading_sessions(date_start, date_end, symbol, market_data_source)
            if day_difference > 0:
                is_previously_upward = symbol_data.is_previously_upward_trend(
                    num_days=day_difference,
                    percent_upward=60
                )
            else:
                is_previously_upward = True
            if is_bearish_harami and is_previously_upward and self.is_symbol_data_tradeable(symbol_data):
                return (True, self.confidence_metrics, self.extra_info)
            else:
                return (False, self.confidence_metrics, self.extra_info)
        else:
            return (False, self.confidence_metrics, self.extra_info)
