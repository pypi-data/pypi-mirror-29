# HUD.ai Python Client

[![Build Status][ci-badge]][ci-url]
[![PyPI][pypi-badge]][pypi-url]
[![PyPI][python-versions-badge]][pypi-url]
[![License][license-badge]]()

The HUD.ai Python Client provides an easy to use wrapper to interact with the
HUD.ai API in python applications.

You must first acquire a HUD.ai secret key before you can use this module.

## Installation

`pip install hudai`

## Usage

```python
from hudai import Client as HudAiClient

hud_ai = HudAiClient(
    client_id='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
    client_secret='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
)

hud_ai.companies.list()

hud_ai.articles.fetch('17787d76-4198-4775-a49a-b3581c37a482')
```

### Parameters

| Parameter | Usage | Example |
|-----------|-------|---------|
| `client_id`*    | Registered Client ID | `'46ef9d9b-89a9-4fd2-84cf-af6de31f2618'` |
| `client_secret` | Registered Client Secret | `'59170c3e-e2c9-4244-92d8-c3595d4af325'` |
| `base_url`      | Specify an alternate server to request resources from | `'https://stage.api.hud.ai/v1'` |
| `auth_url`      | Specify an alternate server to request auth tokens from | `'https://stage.accounts.hud.ai'` |
| `redirect_uri`  | Path to redirect auth requests to (required for `#get_authorize_uri`) | `'https://app.example.com/oauth/callbacks/hud-ai'` |

### Client Auth Flow

In order to access HUD.ai data on a user's behalf, they must authorize you to do
so. This requires 3 steps.

First, send them to the authorization URL

```python
from flask import Flask, redirect, url_for
from hudai import Client as HudAiClient

app = Flask(__name__)

hud_ai = HudAiClient(
    client_id='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
    client_secret='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
    redirect_uri='https://app.example.com/oauth/callbacks/hud-ai'
)

@app.route('/oauth/authorize/hud-ai')
def hud_ai_authorization():
    return redirect(hud_ai.get_authorize_uri(), code=302)
```

Now the user will be presented with a dialog screen where they can accept or
deny your request. The auth server will redirect back to your app in either
case.

Finally, parse the response and get the code and attach it to the client. The
code will be exchanged before the next request is made.

```python
@app.route('/oauth/callbacks/hud-ai')
def hud_ai_callback():
    code = request.args.get('code')
    hud_ai.set_auth_code(code)
```

### `client.get_authorize_uri()`

**NOTE:** This method requires `redirect_uri`

Returns a URL to direct users to to authorize your application to act on their
behalf. You will need to handle the redirect that includes the `code`

### `client.set_auth_code(code)`

Store the code for future exchange for an auth token

### `client.refresh_tokens()`

Attempts to ensure that the client has valid auth tokens.

* Refreshes known expired tokens
* Exchanges auth `code`s for access tokens
* Exchanges client ID/secret for app access tokens

## Resources

### Notes

* `*` and bolded `Type` indicates required param
* Params indicated with `?` are optional keyword params
* `Date` types are automatically converted to/from standard `DateTime` objects
* All `list` resources are paginated to 50/request, with `page` being 0-indexed (e.g. `page=3` will get you the fourth page)

| Entity | Method Base |
|--------|-------------|
| Article | [client.articles](docs/Article.md) |
| ArticleHighlights | [client.article_highlights](docs/ArticleHighlights.d') |
| ArticleKeyTerm | [client.article_key_terms](docs/ArticleKeyTerm.md) |
| ArticleTag | [client.article_tags](docs/ArticleTag.md) |
| Company | [client.companies](docs/Company.md) |
| CompanyEvent | [client.company_events](docs/CompanyEvent.md) |
| CompanyIndustry | [client.company_industries](docs/CompanyIndustry.md) |
| CompanyKeyTerm | [client.company_key_terms](docs/CompanyKeyTerm.md) |
| Domain | [client.domains](docs/Domain.md) |
| Industry | [client.industries](docs/Industry.md) |
| KeyTerm | [client.key_terms](docs/KeyTerm.md) |
| Person | [client.people](docs/Person.md) |
| PersonKeyTerm | [client.person_key_terms](docs/PersonKeyTerm.md) |
| PersonQuote | [client.person_quotes](docs/PersonQuote.md) |
| RelevantArticle | [client.relevant_articles](docs/RelevantArticle.md) |
| SystemEvent | [client.system_events](docs/SystemEvent.md) |
| SystemTask | [client.system_tasks](docs/SystemTask.md) |
| TextCorpus | [client.text_corpora](docs/TextCorpus.md) |
| User | [client.users](docs/User.md) |
| UserCompany | [client.user_companies](docs/UserCompany.md) |
| UserContact | [client.user_contacts](docs/UserContact.md) |
| UserDigestSubscription | [client.user_digest_subscriptions](docs/UserDigestSubscription.md) |
| UserKeyTerm | [client.user_key_terms](docs/UserKeyTerm.md) |

## Deployment

Deploys occur automatically via Travis-CI on tagged commits that build
successfully. Should you need to manually build the project, follow these steps:

```bash
# Install twine to prevent your password from being set in plaintext
pip install twine
# Build the package
python setup.py sdist
# Upload via twine
twine upload dist/hudai-NEW_VERSION_HERE.tar.gz
```

[ci-badge]: https://travis-ci.org/FoundryAI/hud-ai-python.svg?branch=master
[ci-url]: https://travis-ci.org/FoundryAI/hud-ai-python
[pypi-badge]: https://img.shields.io/pypi/v/hudai.svg
[pypi-url]: https://pypi.python.org/pypi/hudai
[python-versions-badge]: https://img.shields.io/pypi/pyversions/hudai.svg
[license-badge]: https://img.shields.io/pypi/l/hudai.svg
[tz-database-link]: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
