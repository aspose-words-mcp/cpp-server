# Aspose.Words C++ MCP registration

This deployment registers only `aspose.words.cpp` through
`config/product-platform-plugins.json`; its compositions list is empty.
The shared engine also supports TeX and Total C++ routes, but this deployment
does not register those plugins or a Total composition.

## GitHub components

| Component | Repository | Selected commit |
| --- | --- | --- |
| Engine | https://github.com/aspose-core-mcp/context-engine | `e917d8cc1dbff142ba67cc6b45e75c271c8daa16` |
| Words C++ plugin | https://github.com/aspose-words-mcp/cpp-plugin | `3cce9f892f9250ee0877f9839cf21bdc945e80ab` |

The engine commit adds Words, TeX, and Total C++ serving support on top of
`93f76496050c54da99addaf3453e8067c47436e7`. The plugin uses
`aspose-words-mcp/docs` (`master`, `en/cpp`) and
`aspose-words-mcp/reference` (`main`, `english/cpp`).
Git records exact submodule commits; changing an upstream branch does not
update this deployment automatically. Use `git ls-files --stage engine
plugins/words-cpp` to inspect the selected references.

## Fresh checkout

From a clean clone, initialize only the top-level submodules:

```powershell
git submodule sync -- engine plugins/words-cpp
git submodule update --init engine plugins/words-cpp
git submodule status
.\scripts\setup.ps1
```

Linux setup: `sh scripts/setup.sh`. Do not add `--recursive`: historical engine
corpus submodules are not required. Preserve local component edits before
running setup or updating submodules.

## Registration and endpoint

The run helpers set `ADCS_PRODUCT_PLUGIN_CATALOG` and
`ADCS_RETRIEVAL_PLUGIN_CATALOG` to this deployment's catalog. The Words endpoint
is `/words/cpp/mcp/v1/streamable-http`; it enforces `aspose.words` and `cpp`, and
initialization returns server name `aspose-words-cpp-mcp`. With the README's
port setting, its URL is `http://127.0.0.1:8080/words/cpp/mcp/v1/streamable-http`.

Registration checks exercise the actual isolated worker with a fixture:

```powershell
.\.venv\Scripts\python.exe scripts/verify_registration.py
$env:PYTHONPATH = Join-Path $PWD 'plugins/words-cpp/src'
.\plugins\words-cpp\.venv\Scripts\python.exe -m unittest discover -s plugins/words-cpp/tests -v
```

For engine endpoint regressions, install pytest in the engine environment and
run from the engine directory:

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
Push-Location engine
try {
    $env:PYTHONPATH = Join-Path $PWD 'src'
    ..\.venv\Scripts\python.exe -m pytest tests/test_words_cpp_mcp.py tests/test_tex_cpp_mcp.py tests/test_total_cpp_mcp.py tests/test_words_net_mcp.py tests/test_tex_net_mcp.py tests/test_total_net_mcp.py -q
} finally {
    Pop-Location
}
```

## Verification evidence and CI

Local checks during the GitHub migration passed:

- Registration, retrieval-profile loading, and worker extraction.
- 12 Words C++ plugin tests.
- 304 C++ and .NET endpoint regression tests for the engine changes.

These checks do not establish full-corpus ingestion, persistent-store retrieval,
or a successful hosted GitHub Actions run.

`.github/workflows/tests.yml` checks shell syntax, catalog JSON and configured
component URLs, initializes top-level submodules, runs setup and registration,
runs plugin tests, and checks that the Words C++ route exists. It does not run
the full engine regression suite or publish content.

## Publishing component updates

1. Commit and push intended engine/plugin changes to their own repositories.
2. Select those published commits in the local submodule checkouts.
3. Stage `engine` and `plugins/words-cpp` in this parent repository, along with
   any changed workflow or documentation files.
4. Review, commit, and push the parent repository, then verify GitHub Actions.

A parent push does not upload uncommitted component files. All referenced
commits must be available from the repositories declared in `.gitmodules`.
