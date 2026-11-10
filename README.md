# Aspose.Words C++ MCP

Deployment wrapper registering only
`aspose.words.cpp`. No compositions are registered. The selected engine revision must support the Words C++ route (see publication status below).

## GitHub checkout and publication status

```powershell
git clone https://github.com/aspose-words-mcp/cpp-server.git
Set-Location cpp-server
git submodule update --init
```

The engine is https://github.com/aspose-core-mcp/context-engine and the plugin is
https://github.com/aspose-words-mcp/cpp-plugin. Do not use recursive submodule
initialization: the engine's historical corpus submodules are not needed.

**Publication prerequisite:** the checked-out GitHub engine revision
`93f76496050c54da99addaf3453e8067c47436e7` does not define the Words C++ route.
Publish/merge the reviewed C++ serving changes to the shared engine, then pin
this server to that available GitHub commit before advertising the endpoint.
The plugin source-URL corrections are also local until published in cpp-plugin;
commit/push them there and update this server's plugin reference afterwards.
Do not publish a parent reference to a commit unavailable from its GitHub remote.

The plugin manifest uses documentation from `aspose-words-mcp/docs` (master,
`en/cpp`) and API references from `aspose-words-mcp/reference` (main,
`english/cpp`). Public citation URLs continue to use Aspose's documentation sites.

## Components

- `engine/`: pinned submodule from `aspose-context-engine-core`.
- `plugins/words-cpp/`: pinned submodule from `aspose-plugin-words-cpp`.
- `config/product-platform-plugins.json`: deployment-specific plugin catalog.

Submodules pin exact commits. Updating an upstream branch does not update this
deployment automatically. Do not recursively initialize historical engine submodules.

## Windows setup

Requires Git, Python 3.12+, access to both component repositories and internet for
dependencies. In PowerShell from this repository root:

```powershell
./scripts/setup.ps1
```

Use `./scripts/setup.ps1 -Python 'C:/path/to/python.exe'` if the Python launcher
is unavailable. Setup initializes immediate submodules and separate Python
environments and verifies worker registration. It does not download corpora or ingest.

## Linux setup

```sh
./scripts/setup.sh
```

## Run the engine

Configure runtime services and credentials as described in `engine/README.md`.
The helpers set both engine catalog environment variables and run from `engine/`.

```powershell
./scripts/run-engine.ps1 -m uvicorn adcs.api.main:app --host 127.0.0.1 --port 8080
# In another terminal, if using queued ingestion:
./scripts/run-engine.ps1 -m celery -A adcs.worker.celery_app:celery_app worker --loglevel=info
```

Linux equivalents use `scripts/run-engine.sh` and `scripts/ingest.sh`.
Use `/words/cpp/mcp/v1/streamable-http`. Its server-selected scope is
`product_id=aspose.words`, `language=cpp`; initialization returns
`aspose-words-cpp-mcp`. The generic endpoint also remains available.
The inherited .NET-specific endpoint is not the C++ endpoint. Other inherited
routes remain defined; this wrapper does not implement route filtering.

## Sources, cache and ingestion

The ingestion workspace is `engine/`. Use the URLs/branches/prefixes in the pinned
plugin's `plugin.json`; resolve source paths against `engine/`. The separate
sibling plugin checkout is not used automatically by this deployment.

For the registered C++ manifest, sources are `engine/sources/documentation-current` (prefix
`en/cpp`) and `engine/sources/api-reference` (prefix `english/cpp`). Follow the plugin
README's Git commands with those destination paths. Do not download sources into
the engine's tracked historical source submodules.

Prepare Gists from the deployment root after cloning documentation:

```powershell
$env:PYTHONPATH = Join-Path $PWD 'plugins/words-cpp/src'
& ./plugins/words-cpp/.venv/Scripts/python.exe -m adcs_words_cpp.gist_examples --source-root engine/sources/documentation-current/en/cpp --cache plugins/words-cpp/sources/gist-examples.json --resolve-history
if ($LASTEXITCODE -ne 0) { throw 'Gist preparation failed.' }
```

Validate first; this can write local operation metadata but does not publish:

```powershell
./scripts/ingest.ps1 --source-kind both --timeout 300
```

With stores/embeddings configured, publish explicitly:

```powershell
./scripts/ingest.ps1 --source-kind docs --publish --timeout 300
./scripts/ingest.ps1 --source-kind apiref --publish --timeout 300
```

Keep source checkouts clean and retain revisions. Do not run overlapping ingestion.
Runtime data and secrets are not repository content. This wrapper does not provision
Docker or databases. CI validates registration and runs standalone plugin tests;
GitHub Actions validates registration and standalone plugin tests using top-level submodules only.


## Dedicated C++ endpoint verification

After pinning a GitHub engine commit with Words C++ serving support, the run
helpers select this repository's plugin catalog.

After setup, start the API with configured local runtime settings:

```powershell
./scripts/run-engine.ps1 -m uvicorn adcs.api.main:app --host 127.0.0.1 --port 8080
```

In another terminal:

```powershell
$body = @{ jsonrpc = '2.0'; id = 1; method = 'initialize' } | ConvertTo-Json
$response = Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8080/words/cpp/mcp/v1/streamable-http' -ContentType 'application/json' -Body $body
$response.result.serverInfo
if ($response.result.serverInfo.name -ne 'aspose-words-cpp-mcp') { throw 'Unexpected MCP identity.' }
```

Initialization confirms serving registration, not corpus ingestion or search quality.
Re-pin the engine submodule to the reviewed GitHub commit after the C++ serving
branch is merged. If merging rewrites either submodule commit, re-pin that pointer
before publishing this parent deployment commit. See `REGISTRATION.md` for the
local verification record, full patches, and manual publication order.
