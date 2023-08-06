import abc


class QuotationFacade(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def real(self, symbols, prefix=False):
        pass

    @abc.abstractmethod
    def market_snapshot(self, prefix=False):
        pass

