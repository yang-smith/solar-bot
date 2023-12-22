import json
import requests
from dotenv import load_dotenv

load_dotenv()
url = 'https://sola-graphql.hasura.app/v1/graphql'

headers = {
}

data = {
  "query": """
  {
    events(where: {group_id: {_eq: 1925}, start_time: {_gte: "2023-12-22T00:00:00"}, end_time: {_lte: "2023-12-23T23:00:00"}})
    {
      id
      badge_id
      category
      content
      cover_url
      created_at
      display
      end_time
      event_site_id
      event_type
      formatted_address
      geo_lat
      geo_lng
      group_id
      host_info
      location
      location_viewport
      max_participant
      meeting_url
      min_participant
      owner_id
      owner {
        about
        id
        image_url
        nickname
        username
      }
      start_time
      status
      tags
      timezone
      title
      require_approval
    }
  }
  """,
  "variables": None
}

def extract_event_details(json_data):
    # Parse the JSON data
    data = json.loads(json_data)

    event_details_str = (
        "群公告\n"
        "👾今日瓦猫活动推荐！\n"
        "活动报名与签到请在Social Layer平台https://app.sola.day/event/\n\n"
    )

    # Loop through each event in the data and format details
    for count, event in enumerate(data['data']['events'], 1):
        title = event.get('title', 'No Title Provided')
        content = event.get('content', 'No Content Available').strip() or '[No Content Available]'
        start_time = event.get('start_time', 'No Start Time Provided')
        end_time = event.get('end_time', 'No End Time Provided')
        organizer = event.get('owner', {}).get('username', 'No Organizer Provided')
        event_link = event.get('meeting_url', 'No Link Provided')
        timezone = event.get('timezone', 'UTC')
        location = event.get('location', 'No Location Provided')

        # Event details formatting
        event_details_str += (
            f"{count}️⃣ . {title}\n"
            f"-{content}\n"
            f"⏰时间：{start_time} to {end_time} {timezone}\n"
            f"🏠场地：{location}  Event Link: {event_link}\n\n"
            # f"📍 Hosted By: {organizer}\n\n"
        )

    # Footer with additional links and information
    event_details_str += (
        "WAMO官网：https://wamotopia.love/\n"
        "「👀查看、发起、报名活动，捐赠、了解、支持WAMO」\n"
        "「⚠️请所有伙伴在首页点击“我想加入共创”领取 “WAMO PASS”」\n"
        "WAMO广场住宿：https://slender-tarn-59b.notion.site/734f27e840674ca897dc183582960527\n"
        "「📖预订WAMO广场，出门即参会」\n"
        " WAMO广场地址：Dreamer Club Resort\n"
        "「🗺️打开谷歌地图搜索」"
    )

    return event_details_str

import asyncio
from datetime import datetime, timedelta
async def events():
    today = datetime.now()
    start_of_today = datetime(today.year, today.month, today.day)
    end_of_today = start_of_today + timedelta(days=1) - timedelta(seconds=1)
    
    start_time = start_of_today.strftime("%Y-%m-%dT%H:%M:%S")
    end_time = end_of_today.strftime("%Y-%m-%dT%H:%M:%S")
    data = {
      "query": f"""
      {{
        events(where: {{group_id: {{_eq: 1925}}, start_time: {{_gte: "{start_time}"}}, end_time: {{_lte: "{end_time}"}}}})
        {{
          id
          badge_id
          category
          content
          cover_url
          created_at
          display
          end_time
          event_site_id
          event_type
          formatted_address
          geo_lat
          geo_lng
          group_id
          host_info
          location
          location_viewport
          max_participant
          meeting_url
          min_participant
          owner_id
          owner {{
            about
            id
            image_url
            nickname
            username
          }}
          start_time
          status
          tags
          timezone
          title
          require_approval
        }}
      }}
      """,
      "variables": None
    }
    response = requests.post(url, json=data)
    # print(response.text)
    events_datails = extract_event_details(response.text)
    print(events_datails)
    # result = await ai.ai_event(events_datails)
    # print(result)
    return events_datails

# asyncio.run(events())
