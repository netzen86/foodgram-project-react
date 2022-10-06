import schemathesis

schema = schemathesis.from_uri("http://localhost/api/docs/openapi-schema.yml")


@schema.parametrize()
def test_api(case):
    case.call_and_validate(headers={"Authorization": "Token bc209de938a05543d9180a6e4734483a8a8b79f8"})
