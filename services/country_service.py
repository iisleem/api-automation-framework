"""Example GraphQL service layer."""

from __future__ import annotations

from clients import GraphQLClient
from utils.config_reader import resolve_path


class CountryService:
    def __init__(self, client: GraphQLClient) -> None:
        self.client = client

    def country_by_code(self, code: str):
        query_path = resolve_path("data/graphql/country_query.graphql")
        return self.client.execute_file(query_path, variables={"code": code}, operation_name="CountryByCode")
