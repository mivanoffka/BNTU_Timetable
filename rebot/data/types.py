import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, String, Column, ForeignKey, DateTime, Time, Boolean, MetaData, text

base = declarative_base()


class WeekNumber(base):
    __tablename__ = 'week_numbers'
    id = Column(Integer(), primary_key=True)
    info = Column(String(16), nullable=False)


class Weekday(base):
    __tablename__ = 'weekdays'
    id = Column(Integer(), primary_key=True)
    name = Column(String(16), nullable=False)


class Revision(base):
    __tablename__ = 'revisions'
    id = Column(Integer(), primary_key=True)
    datetime = Column(DateTime(), nullable=False)
    name = Column(String(16), nullable=True)


class Subgroups(base):
    __tablename__ = 'subgroups'
    id = Column(Integer(), primary_key=True)
    info = Column(String(16), nullable=False)


class DailyDistributionTime(base):
    __tablename__ = 'daily_distribution_times'
    id = Column(Integer(), primary_key=True)
    time = Column(Time(), unique=True, nullable=False)


class LessonTime(base):
    __tablename__ = 'lesson_times'
    id = Column(Integer(), primary_key=True)
    time = Column(Time(), unique=True, nullable=False)


class Group(base):
    __tablename__ = 'groups'
    id = Column(Integer(), primary_key=True)
    group = Column(String(32), unique=True, nullable=False)
    present_in_schedule = Column(Boolean())


class User(base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)

    telegram_id = Column(String(32), unique=True)
    telegram_name = Column(String(32), nullable=True)

    group_id = Column(Integer(), ForeignKey('groups.id'))
    ui_message_id = Column(String(32), nullable=True)
    daily_distribution_time_id = Column(Integer(), ForeignKey('daily_distribution_times.id'))


class Lesson(base):
    __tablename__ = 'lessons'
    id = Column(Integer(), primary_key=True)

    group_id = Column(Integer(), ForeignKey("groups.id"), nullable=False)
    weekday_id = Column(Integer(), ForeignKey("weekdays.id"), nullable=False)
    time_id = Column(Integer(), ForeignKey("lesson_times.id"), nullable=False)

    week_number_id = Column(Integer(), ForeignKey("week_numbers.id"), nullable=False)
    subgroup_id = Column(Integer(), ForeignKey("subgroups.id"), nullable=False)

    info = Column(String(512), nullable=False)

    revision_id = Column(Integer(), ForeignKey("revisions.id"), nullable=False)





