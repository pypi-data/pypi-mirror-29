# directory-signature-auth

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gemnasium-image]][gemnasium]

**Library implementing Hawk authentication scheme using a message authentication code (MAC) algorithm to provide partial HTTP request cryptographic verification.**

---

The client implements `RequestSigner` to generate a secret-salted hash of the request URL and body. The secret-salt is shared with the target server.

The target server implements `RequestSignatureChecker` to check the signature provided in the request header accurately describes the request's URL and request body.

If `RequestSignatureChecker` accepts the header as genuine then the request is accepted, otherwise the request is rejected.

## RequestSigner usage

### Python requests

On the client, a signature can be generated for a [requests](http://docs.python-requests.org/en/master/)'s `requests.Request`:

```
import requests

from sigauth.utils import RequestSigner

from django.conf import settings


request_signer = RequestSigner(settings.API_SIGNATURE_SECRET)


def send_request(method, url, body):
    request = requests.Request(method=method, url=url, body=body).prepare()
    sign_request(request)
    return requests.Session().send(request)


def sign_request(request):
    headers = request_signer.get_signature_headers(
        url=request.path_url,
        body=request.body,
        method=request.method,
        content_type=request.headers.get('Content-Type'),
    )
    request.headers.update(headers)
```


## RequestSignatureChecker usage

### Django Rest Framework

This library implements a wrapper around `RequestSignatureChecker` for Django Rest Framework: `SignatureCheckPermissionBase`. It must be sub-classed to set the secret:

```
from sigauth import permissions

from django.conf import settings


class SignatureCheckPermission(permissions.SignatureCheckPermissionBase):
    secret = settings.SIGNATURE_SECRET
```

On the target server, `SignatureCheckPermission` can then be set in the `DEFAULT_PERMISSION_CLASSES` setting, or on a specific DRF view's `permission_classes` attribute.

### Django View

On the target server, the signature checker can be implemented on views too:

```
from django.http import HttpResponseForbidden

from sigauth.utils import RequestSignatureChecker


api_checker = RequestSignatureChecker(settings.SIGNATURE_SECRET)


class SignatureCheckMixin:
    def dispatch(self, request, *args, **kwargs):
        if api_checker.test_signature(request) is False:
            return HttpResponseForbidden()
        return super().dispatch(request, path='', *args, **kwargs)
```

`SignatureCheckMixin` can then be used on a view to reject incoming requests that have been tampered with.

Note that in the above examples, the client's `settings.API_SIGNATURE_SECRET` must be the same value as api's `settings.SIGNATURE_SECRET`

## Installation

```shell
pip install -e git+https://git@github.com/uktrade/directory-signature-auth.git@v1.0.0#egg=directory-signature-auth
```

## Development

    $ git clone https://github.com/uktrade/directory-signature-auth
    $ cd directory-signature-auth
    $ make

## Publish to PyPI

The package should be published to PyPI on merge to master. If you need to do it locally then get the credentials from rattic and add the environment variables to your host machine:

| Setting                     |
| --------------------------- |
| DIRECTORY_PYPI_USERNAME     |
| DIRECTORY_PYPI_PASSWORD     |


Then run the following command:

    make publish

[code-climate-image]: https://codeclimate.com/github/uktrade/directory-signature-auth/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/directory-signature-auth

[circle-ci-image]: https://circleci.com/gh/uktrade/directory-signature-auth/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-signature-auth/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-signature-auth/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-signature-auth

[gemnasium-image]: https://gemnasium.com/badges/github.com/uktrade/directory-signature-auth.svg
[gemnasium]: https://gemnasium.com/github.com/uktrade/directory-signature-auth


