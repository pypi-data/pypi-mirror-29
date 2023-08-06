import operator

from fito import Operation
from fito.specs.base import SpecField, PrimitiveField, GetOperation


class SeriesOperation(Operation):
    def resample(self, rule='D', how='mean'):
        return ResampleOperation(operation=self, rule=rule, how=how)

    def __getitem__(self, operation):
        return ConditionedOperation(main_operation=self, cond_operation=operation)

    def __and__(self, operation):
        return AndOperation(operation1=self, operation2=operation)

    def __or__(self, operation):
        return OrOperation(operation1=self, operation2=operation)


class GetSeriesOperation(SeriesOperation, GetOperation):
    def _apply(self, data_store):
        return data_store.get(self.name)

    def __compare(self, op, scalar):
        return BinaryOperation(operation=self, op_name=op, val=scalar)

    def __eq__(self, scalar):
        # TODO: what happens when we insert this into a hashmap
        return self.__compare('=', scalar)

    def __le__(self, scalar):
        return self.__compare('<=', scalar)

    def __ge__(self, scalar):
        return self.__compare('>=', scalar)

    def __lt__(self, scalar):
        return self.__compare('<', scalar)

    def __gt__(self, scalar):
        return self.__compare('>', scalar)

    def __ne__(self, scalar):
        return self.__compare('!=', scalar)

    def __repr__(self):
        return 'GO(%s)' % try_encode(self.name)


def try_encode(s):
    return s.encode('utf8') if isinstance(s, unicode) else s


class ResampleOperation(SeriesOperation):
    operation = SpecField()
    how = PrimitiveField(base_type=basestring)
    rule = PrimitiveField(base_type=basestring)

    def _apply(self, data_store):
        series = data_store.execute(self.operation)
        if series.dtype == object:
            series = series.dropna().convert_objects()

        return getattr(series.resample(self.rule), self.how)

    def __repr__(self):
        return '(%s).resample(how=%s, rule=%s)' % (self.operation, try_encode(self.how), try_encode(self.rule))


class ConditionedOperation(SeriesOperation):
    main_operation = SpecField()
    cond_operation = SpecField()

    def _apply(self, data_store):
        return data_store.execute(self.main_operation)[data_store.execute(self.cond_operation)]

    def __repr__(self):
        return '(%s)[%s]' % (self.main_operation, self.cond_operation)


class AndOperation(SeriesOperation):
    operation1 = SpecField()
    operation2 = SpecField()

    def _apply(self, data_store):
        return data_store.execute(self.operation1) & data_store.execute(self.operation2)

    def __repr__(self):
        return '%s & %s' % (self.operation1, self.operation2)


class OrOperation(SeriesOperation):
    operation1 = SpecField()
    operation2 = SpecField()

    def _apply(self, data_store):
        return data_store.execute(self.operation1) | data_store.execute(self.operation2)

    def __repr__(self):
        return '%s | %s' % (self.operation1, self.operation2)


class IntervalOperation(SeriesOperation):
    operation = SpecField(0)
    lbound = PrimitiveField(1)
    ubound = PrimitiveField(2)

    def _apply(self, data_store):
        return (data_store.execute(self.operation) >= self.lbound) & (data_store.execute(self.operation) <= self.ubound)

    def __repr__(self):
        return '%s in [%s-%s]' % (self.operation, self.lbound, self.ubound)


class BinaryOperation(SeriesOperation):
    ops = {'=': operator.eq,
           '>=': operator.ge,
           '<=': operator.le,
           '>': operator.gt,
           '<': operator.lt,
           '!=': operator.ne}

    operation = SpecField()
    op_name = PrimitiveField()
    val = PrimitiveField()

    def _apply(self, data_store):
        import pandas as pd
        import numpy as np
        if np.isscalar(self.val) and pd.isnull(self.val) and self.op_name in ('=', '!='):
            res = pd.isnull(data_store.execute(self.operation))
            if self.op_name == '!=':
                res = ~res
            return res
        else:
            op = self.ops[self.op_name]
            return op(data_store.execute(self.operation), self.val)

    def __repr__(self):
        return '%s %s %s' % (self.operation, try_encode(self.op_name), try_encode(self.val))
