from uuid import UUID

import asyncio

from evo.aio import AioTransport
from evo.common import APIConnector, Environment, IAuthorizer, HTTPHeaderDict
from evo.common.utils import Cache
from evo.discovery import DiscoveryAPIClient
from evo.objects.client import ObjectAPIClient
from evo.workspaces import WorkspaceAPIClient


class HackAuthorizer(IAuthorizer):
    async def get_default_headers(self) -> HTTPHeaderDict:
        # Snoop on BentleyUserIdProvider and put the real token here
        token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IlFBSU1TLkJFTlRMRVkyNCIsInBpLmF0bSI6ImE4bWUifQ.eyJzY29wZSI6WyJvcGVuaWQiLCJlbWFpbCIsInByb2ZpbGUiLCJvcmdhbml6YXRpb24iLCJvZmZsaW5lX2FjY2VzcyIsImNlbnRyYWwuYXV0aHoiLCJjZW50cmFsLmluc3RhbmNlOnJlYWQiLCJlbnRpdGxlbWVudC5hdXRoeiIsImV2by5ibG9ja3N5bmMiLCJldm8uZGlzY292ZXJ5IiwiZXZvLmZpbGUiLCJldm8ub2JqZWN0IiwiZXZvLndvcmtzcGFjZSJdLCJjbGllbnRfaWQiOiJsZWFwZnJvZy13b3JrcyIsImF1ZCI6WyJodHRwczovL3FhLWltcy5iZW50bGV5LmNvbS9hcy90b2tlbi5vYXV0aDIiLCJodHRwczovL3FhLWltc29pZGMuYmVudGxleS5jb20vYXMvdG9rZW4ub2F1dGgyIiwiaHR0cHM6Ly9xYTItaW1zLmJlbnRsZXkuY29tL2FzL3Rva2VuLm9hdXRoMiIsImh0dHBzOi8vcWEyLWltc29pZGMuYmVudGxleS5jb20vYXMvdG9rZW4ub2F1dGgyIiwiaHR0cHM6Ly9xYS1pbXNvaWRjLmJlbnRsZXkuY29tL3Jlc291cmNlcyIsImh0dHBzOi8vcWEyLWltcy5iZW50bGV5LmNvbS9yZXNvdXJjZXMiLCJzZWVxdWVudC1jZW50cmFsLXNjb3BlcyIsImxlYXBmcm9nLXdvcmtzLXNjb3BlcyIsInNlZXF1ZW50LWV2by1zY29wZXMiLCJzcS1ldm8tc2NvcGVzIl0sInN1YiI6IjRjM2EyMWU1LTZhOTYtNDlkNy04Yjg3LTNlYTBlNWNhNmU4ZCIsInJvbGUiOiJCRU5UTEVZX0VNUExPWUVFIiwiYmVudGxleUxhc3RUb2tlblJlZnJlc2giOiIyMDI1LTA4LTExVDAzOjEyOjI3WiIsIm9yZyI6IjcyYWRhZDMwLWMwN2MtNDY1ZC1hMWZlLTJmMmRmYWM5NTBhNCIsInN1YmplY3QiOiI0YzNhMjFlNS02YTk2LTQ5ZDctOGI4Ny0zZWEwZTVjYTZlOGQiLCJhbXIiOlsiQmVudGxleUlkIiwiZmVkIl0sImlzcyI6Imh0dHBzOi8vcWEtaW1zLmJlbnRsZXkuY29tIiwiZW50aXRsZW1lbnQiOlsiU0VMRUNUXzIwMDYiXSwicHJlZmVycmVkX3VzZXJuYW1lIjoiRGFuaWVsLktpbm5leUBiZW50bGV5LmNvbSIsImdpdmVuX25hbWUiOiJEYW5pZWwiLCJzaWQiOiJJSDg2c0E2S3ZuTEhJUFVacEFjb3h1Nk5aUHMuVVVGSlRWTXRRbVZ1ZEd4bGVTMVRSdy5tUmo2IiwibmJmIjoxNzU0ODYzNTY2LCJ1bHRpbWF0ZV9zaXRlIjoiMTAwMTM4OTExNyIsInVzYWdlX2NvdW50cnlfaXNvIjoiTFQiLCJhdXRoX3RpbWUiOjE3NTQ4NjM4NjYsIm5hbWUiOiJEYW5pZWwuS2lubmV5QGJlbnRsZXkuY29tIiwib3JnX25hbWUiOiJCZW50bGV5IFN5c3RlbXMgSW5jIiwiZmFtaWx5X25hbWUiOiJLaW5uZXkiLCJlbWFpbCI6IkRhbmllbC5LaW5uZXlAYmVudGxleS5jb20iLCJleHAiOjE3NTQ4ODU1NDh9.Vs5n_wA94ylT2bAKvAX-8jhqaDBsRroUgInluyAJy6SPq8yy4LbJWyXyvUI8bbDz78AWqSgTENuhbIKhlIzd6gC_46A2ZErwGvuDwgLN5x1htb0T9Q3yJ29pun7dxGoOCgSU9v2dVHsiDQJSaKJ4uEkKeK4b07cVTMiwCXRK4s6c8YSEtJQS_Jsgi4lKwNMUCuXwopuhceCondDZJWgHl-EIh_npjP5kjn1i4bfNlDWhRnCXFVcnIlmQcgUOQ63Nyc9MKFtkSwjslpp46FEYprmHMW0Qk8KmcGjMJfM6nI8v_EFOYD8ZxI2D5PphDuOsJ6Rs70fu6hm3U3YY-7dTtA'

        return HTTPHeaderDict({"Authorization": f"Bearer {token}"})

    async def refresh_token(self) -> bool:
        raise NotImplementedError("If token expires, snoop to find another one")


def make_api_connector(base_url: str):
    return APIConnector(
        base_url=base_url,
        transport=AioTransport(user_agent="whatever"),
        authorizer=HackAuthorizer(),
    )


def discover_orgs():
    base_url = r"https://uat-api.test.seequent.systems"  # Snoop on ApiConnector
    discovery_client = DiscoveryAPIClient(make_api_connector(base_url))
    return asyncio.run((discovery_client.list_organizations(service_codes=("evo", "blockmodel"))))


def discover_workspaces_for_hub(org_id, hub_url):
    client = WorkspaceAPIClient(make_api_connector(hub_url), org_id)
    return asyncio.run(client.list_workspaces())


# Hardcode the environment. Or, use the discover functions.
environment = Environment(
    hub_url="https://350mt.api.integration.seequent.com",
    org_id=UUID("829e6621-0ab6-4d7d-96bb-2bb5b407a5fe"),
    workspace_id=UUID("6678600c-168e-4920-a6f8-8926ae0a3c59"),
)


def get_evo_api(cache_path: str):
    api_connector = make_api_connector(environment.hub_url)
    api_client = ObjectAPIClient(environment=environment, connector=api_connector)
    cache = Cache(root=cache_path, mkdir=True)
    data_client = api_client.get_data_client(cache)
    return api_client, data_client


async def get_evo_polyline(api_client):
    objects = await api_client.list_all_objects()
    obj_meta = [o for o in objects if o.name == "10_pts_features.json"][0]
    # obj_meta = [o for o in objects if o.name == "10_pts_features - additions at beginning - well known text.json"][0]
    # obj_meta = [o for o in objects if o.name == "Waipara_contacts.json"][0]
    return obj_meta
