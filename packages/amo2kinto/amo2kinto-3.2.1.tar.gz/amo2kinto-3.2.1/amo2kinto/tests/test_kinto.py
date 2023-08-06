import mock
from kinto_http.exceptions import KintoException
from amo2kinto.kinto import get_kinto_records


def test_get_kinto_records_try_to_create_the_bucket():
    kinto_client = mock.MagicMock()
    kinto_client.create_collection.return_value.status_code = 201
    get_kinto_records(kinto_client, mock.sentinel.bucket,
                      mock.sentinel.collection, mock.sentinel.permissions)

    kinto_client.create_bucket.assert_called_with(id=mock.sentinel.bucket,
                                                  if_not_exists=True)


def test_get_kinto_records_try_to_create_the_bucket_and_keep_going_on_403():
    kinto_client = mock.MagicMock()
    Http403 = mock.MagicMock()
    Http403.response.status_code = 403
    kinto_client.create_bucket.side_effect = KintoException(exception=Http403)
    get_kinto_records(kinto_client, mock.sentinel.bucket,
                      mock.sentinel.collection, mock.sentinel.permissions)

    kinto_client.create_bucket.assert_called_with(id=mock.sentinel.bucket,
                                                  if_not_exists=True)
    kinto_client.create_collection.assert_called_with(
        id=mock.sentinel.collection, bucket=mock.sentinel.bucket,
        permissions=mock.sentinel.permissions, if_not_exists=True)


def test_get_kinto_records_try_to_create_the_collection_with_permissions():
    kinto_client = mock.MagicMock()
    kinto_client.create_collection.return_value.status_code = 201
    get_kinto_records(kinto_client, mock.sentinel.bucket,
                      mock.sentinel.collection, mock.sentinel.permissions)

    kinto_client.create_collection.assert_called_with(
        id=mock.sentinel.collection, bucket=mock.sentinel.bucket,
        permissions=mock.sentinel.permissions, if_not_exists=True)


def test_get_kinto_records_try_to_create_the_collection_and_keep_going_on_403():
    kinto_client = mock.MagicMock()
    Http403 = mock.MagicMock()
    Http403.response.status_code = 403
    kinto_client.create_collection.side_effect = KintoException(exception=Http403)
    get_kinto_records(kinto_client, mock.sentinel.bucket,
                      mock.sentinel.collection, mock.sentinel.permissions)

    kinto_client.get_collection.assert_called_with(id=mock.sentinel.collection,
                                                   bucket=mock.sentinel.bucket)


def test_get_kinto_records_gets_a_list_of_records():
    kinto_client = mock.MagicMock()
    kinto_client.create_collection.return_value.status_code = 201
    get_kinto_records(kinto_client, mock.sentinel.bucket,
                      mock.sentinel.collection, mock.sentinel.permissions)

    kinto_client.get_records.assert_called_with(
        bucket=mock.sentinel.bucket, collection=mock.sentinel.collection)


def test_get_kinto_records_try_to_create_the_collection_with_schema():
    kinto_client = mock.MagicMock()
    kinto_client.create_collection.return_value.status_code = 201
    kinto_client.create_collection.return_value.json.return_value = {
        "data": {
            "schema": {},
            "uiSchema": {},
            "displayFields": {}
        }
    }
    get_kinto_records(kinto_client,
                      mock.sentinel.bucket,
                      mock.sentinel.collection,
                      mock.sentinel.permissions,
                      config={"schema": {'foo': 'bar'}})

    kinto_client.patch_collection.assert_called_with(
        bucket=mock.sentinel.bucket,
        id=mock.sentinel.collection,
        data={"schema": {"foo": "bar"}})


def test_get_kinto_records_try_to_update_the_collection_schema():
    kinto_client = mock.MagicMock()
    kinto_client.create_collection.return_value = {
        "details": {
            "existing": {
                "schema": {},
                "uiSchema": {},
                "displayFields": {}
            }
        }
    }
    get_kinto_records(kinto_client,
                      mock.sentinel.bucket,
                      mock.sentinel.collection,
                      mock.sentinel.permissions,
                      config={"schema": {'foo': 'bar'}})

    kinto_client.patch_collection.assert_called_with(
        bucket=mock.sentinel.bucket,
        id=mock.sentinel.collection,
        data={"schema": {"foo": "bar"}})


def test_get_kinto_records_doesnt_update_the_collection_schema_if_identical():
    kinto_client = mock.MagicMock()
    kinto_client.create_collection.return_value = {
        "details": {
            "existing": {
                "schema": {"foo": "bar"},
                "uiSchema": {"ui": "bar"},
                "displayFields": ["display", "bar"],
            }
        }
    }
    get_kinto_records(kinto_client,
                      mock.sentinel.bucket,
                      mock.sentinel.collection,
                      mock.sentinel.permissions,
                      config={
                          "schema": {"foo": "bar"},
                          "uiSchema": {"ui": "bar"},
                          "displayFields": ["display", "bar"],
                      })

    assert not kinto_client.patch_collection.called


def test_get_kinto_records_does_update_if_it_has_created_it():
    kinto_client = mock.MagicMock()
    kinto_client.create_collection.return_value = {
        "data": {
            "schema": {}
        }
    }
    get_kinto_records(kinto_client,
                      mock.sentinel.bucket,
                      mock.sentinel.collection,
                      mock.sentinel.permissions,
                      config={"schema": {'foo': 'bar'}})

    assert kinto_client.patch_collection.called
