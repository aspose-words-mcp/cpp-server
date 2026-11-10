# Aspose.Words for C++ MCP Server

Deploy the Aspose context engine with the Aspose.Words for C++ extraction plugin registered, then connect an MCP-compatible AI client to documentation and API tools.

This repository supplies a pinned engine/plugin composition, its catalog, and setup, launch, and ingestion helpers. It does not bundle indexed documentation, provision infrastructure, or supply a hosted endpoint.

## Project family

| Repository | Responsibility |
| --- | --- |
| [context-engine](https://github.com/aspose-core-mcp/context-engine) | Shared ingestion, indexing, retrieval, and MCP infrastructure |
| [cpp-plugin](https://github.com/aspose-words-mcp/cpp-plugin) | Words C++ documentation/API extraction and retrieval configuration |
| [cpp-server](https://github.com/aspose-words-mcp/cpp-server) | Deployment helpers combining pinned engine and plugin versions |

## Get the server

```sh
git clone https://github.com/aspose-words-mcp/cpp-server.git
cd cpp-server
```

Setup initializes only the immediate engine and plugin submodules. Do not clone recursively: the engine retains historical corpus submodules that this deployment does not need.

## Setup and verification

Requires Git and Python 3.12 or newer. From the repository root:

```powershell
.\scripts\setup.ps1
```

Linux:

```sh
sh scripts/setup.sh
```

Setup installs the engine into `.venv`, creates a separate plugin interpreter, and verifies registration, retrieval-profile loading, and fixture extraction. It does not download corpora or publish content. Preserve uncommitted submodule edits before running setup. See [registration details](REGISTRATION.md) for component revisions and additional tests.

## Run the server

Configure runtime stores, credentials, and embeddings as described in [the engine README](engine/README.md). Then:

```powershell
.\scripts\run-engine.ps1 -m uvicorn adcs.api.main:app --host 127.0.0.1 --port 8080
```

Linux:

```sh
sh scripts/run-engine.sh -m uvicorn adcs.api.main:app --host 127.0.0.1 --port 8080
```

For queued ingestion, run the worker in another terminal:

```sh
sh scripts/run-engine.sh -m celery -A adcs.worker.celery_app:celery_app worker --loglevel=info
```

On Windows use `scripts/run-engine.ps1` with the same arguments. Always use the wrapper: it selects this deployment's product and retrieval catalogs and runs from `engine/`.

## Populate content and connect

Clone the sources into the engine workspace, from the server root (only if destinations do not exist):

```powershell
$env:GIT_LFS_SKIP_SMUDGE = '1'
New-Item -ItemType Directory -Force engine/sources | Out-Null
git clone --depth 1 --filter=blob:none --sparse --branch master https://github.com/aspose-words-mcp/docs.git engine/sources/documentation-current
if ($LASTEXITCODE -ne 0) { throw 'Documentation clone failed.' }
git -C engine/sources/documentation-current sparse-checkout set en/cpp
if ($LASTEXITCODE -ne 0) { throw 'Documentation checkout failed.' }
git clone --depth 1 --filter=blob:none --sparse --branch main https://github.com/aspose-words-mcp/reference.git engine/sources/api-reference
if ($LASTEXITCODE -ne 0) { throw 'API clone failed.' }
git -C engine/sources/api-reference sparse-checkout set english/cpp
if ($LASTEXITCODE -ne 0) { throw 'API checkout failed.' }
$env:PYTHONPATH = Join-Path $PWD 'plugins/words-cpp/src'
& .\plugins\words-cpp\.venv\Scripts\python.exe -m adcs_words_cpp.gist_examples --source-root engine/sources/documentation-current/en/cpp --cache plugins/words-cpp/sources/gist-examples.json --resolve-history
if ($LASTEXITCODE -ne 0) { throw 'Gist preparation failed.' }
.\scripts\ingest.ps1 --source-kind both --timeout 300
# Continue only after validation succeeds:
.\scripts\ingest.ps1 --source-kind both --publish --timeout 300
```

On Linux, use the same Git commands with `export GIT_LFS_SKIP_SMUDGE=1`, prepare Gists with `PYTHONPATH=plugins/words-cpp/src plugins/words-cpp/.venv/bin/python -m adcs_words_cpp.gist_examples` and the same arguments, then use `sh scripts/ingest.sh`. See the [plugin README](plugins/words-cpp/README.md) for extraction details. Do not change sources or run overlapping ingestion operations during publication.

Configure a client with the local endpoint:

```text
http://127.0.0.1:8080/words/cpp/mcp/v1/streamable-http
```

For a hosted deployment, substitute your reachable HTTPS host. Localhost refers to the client's own machine; remote clients need a reachable deployment or tunnel. Initialization reports `aspose-words-cpp-mcp`; successful initialization does not prove ingestion or retrieval quality.

## Scope

Only `aspose.words.cpp` is registered; the catalog has no compositions. The Words C++ route fixes the product and language. The shared engine also defines generic, TeX, Total, and .NET routes; this repository does not remove them. Registration does not populate indexes or grant access to source repositories.

## Files

| Path | Purpose |
| --- | --- |
| `engine/` | Pinned context-engine submodule |
| `plugins/words-cpp/` | Pinned Words C++ plugin submodule |
| `config/product-platform-plugins.json` | Deployment registration catalog |
| `scripts/setup.*` | Initialize components and verify registration |
| `scripts/run-engine.*` | Launch engine commands with deployment catalogs |
| `scripts/ingest.*` | Words ingestion with explicit workspace and interpreter |
| `scripts/verify_registration.py` | Fixture-based integration check |
| `REGISTRATION.md` | Component revisions, checks and publication order |

Submodules pin exact commits. Updating an upstream branch does not update this deployment automatically. Publish component commits first, then update the parent references and rerun verification.

## Validation and licenses

GitHub Actions checks shell syntax, catalog JSON and component URL placeholders, runs setup and registration, runs plugin regressions, and checks that the Words C++ route is present. It does not deploy services or publish content. Local test results and their limitations are documented in [REGISTRATION.md](REGISTRATION.md).

Engine and plugin licenses and notices are supplied by their respective pinned repositories. Preserve them when distributing those components. A root deployment license has not yet been added; do not assume the component licenses automatically license this repository's own files.
