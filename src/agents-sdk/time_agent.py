import sys
import datetime
from pydantic import BaseModel
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

load_dotenv()


class TimeInterval(BaseModel):
    start_time: int
    end_time: int


@function_tool
def date_conversion(
    year: int, month: int, day: int, hour: int, minute: int, second: int
) -> int:
    """Function that converts dates to timestamps in miliseconds"""
    return (
        int(
            datetime.datetime(year, month, day, hour, minute, second)
            .replace(tzinfo=datetime.timezone.utc)
            .timestamp()
        )
        * 1000
    )


@function_tool
def current_time() -> int:
    """Function that gets current time in timestamp miliseconds"""
    return int(datetime.datetime.now(datetime.timezone.utc).timestamp()) * 1000


@function_tool
def time_delta(
    timestamp: int, days: int, hours: int, minutes: int, seconds: int
) -> int:
    """Function that returns a timestamp substracting an interval of days, hours, minutes, seconds"""
    interval = (
        datetime.timedelta(
            days=days, hours=hours, minutes=minutes, seconds=seconds
        ).total_seconds()
        * 1000
    )
    result = int(timestamp - interval)
    return result


agent = Agent(
    name="Time Agent",
    instructions="You perform time related tasks. You return time intervals. You always return responses in timestamps.",
    output_type=TimeInterval,
    tools=[date_conversion, current_time, time_delta],
)

result = Runner.run_sync(agent, str(sys.argv[1]))
print(result.raw_responses)
