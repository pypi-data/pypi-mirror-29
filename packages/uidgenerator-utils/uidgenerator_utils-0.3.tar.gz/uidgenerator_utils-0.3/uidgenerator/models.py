# -*- coding: utf-8 -*-
import time
from django.core import exceptions

from django.db import models
from django.db.models import BigIntegerField

from test_server.apps.uidgenerator import settings

class UIDField(models.Field):
    empty_strings_allowed = False

    def __init__(self, *args, **kwargs):
        self.startTimeStamp = kwargs.pop("start_timestamp", settings.STARTTIMESTAMP)
        self.regionIdBits = kwargs.pop("regionIdBits", settings.REGIONIDBITS)
        self.workerIdBits = kwargs.pop("workerIdBits", settings.WORKERIDBITS)
        self.sequenceBits = kwargs.pop("sequenceBits", settings.SEQUENCEBITS)

        self.regionId = kwargs.pop("regionId", settings.REGIONID)
        self.workerId = kwargs.pop("workerId", settings.WORKERID)

        maxRegionId = -1 ^ (-1 << self.regionIdBits)
        maxWorkerId = -1 ^ (-1 << self.workerIdBits)
        self.maxSequenceId = -1 ^ (-1 << self.sequenceBits)

        if self.regionId > maxRegionId or self.regionId < 0:
            raise OverflowError

        if self.workerId > maxWorkerId or self.workerId < 0:
            raise OverflowError

        self.lastTimeStamp = -1
        self.sequenceId = 0
        super().__init__(*args, **kwargs)


    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['primary_key'] = True
        return name, path, args, kwargs

    def get_internal_type(self):
        return "UIDField"

    def to_python(self, value):
        if value is None:
            return value
        try:
            return int(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def db_type(self, connection):
        return 'BIGINT'

    def get_prep_value(self, value):
        if value is None:
            workerIdShift = self.sequenceBits
            regionIdShift = self.workerIdBits + self.sequenceBits
            timesStampShift = self.workerIdBits + self.sequenceBits + self.regionIdBits

            curTime = self.currentTime()
            if (self.lastTimeStamp == curTime):
                self.sequence = (self.sequence + 1) & self.maxSequenceId
                if (self.sequence == 0):
                    curTime = self.tailNextMillis(self.lastTimeStamp)
            else:
                self.sequence = 0

            self.lastTimeStamp = curTime
            uid = int(((curTime - self.startTimeStamp) << timesStampShift) | (self.regionId << regionIdShift) | (self.workerId << workerIdShift) | self.sequence)
            print('uid======%s'%uid)
            return uid
        else:
            return value

    def currentTime(self):
        return int(time.time()*1000)

    def tailNextMillis(self, timeStamp):
        curTime = self.currentTime()
        while (curTime <= timeStamp):
            curTime = self.currentTime()
        return curTime

    def rel_db_type(self, connection):
        return BigIntegerField().db_type(connection=connection)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return value

    def validate(self, value, model_instance):
        pass

    def formfield(self, **kwargs):
        return None


