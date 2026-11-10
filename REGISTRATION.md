# Historical registration record

This record describes earlier GitLab work, not the current GitHub checkout.
See README.md for current publication prerequisites and engine compatibility.

# Words/C++ registration — uncommitted, C++ only

The engine branch `feat/words-cpp-serving` is based on original engine main
`79f6bd888cca188283c952396b7fab5c934ac09a`. The Java serving commit is not in this
branch's ancestry. No Java route, scope, ingress, tests, or profile-prefix changes
are included in the working diff. Existing generic Java mentions in the original
engine are unchanged.

All registration changes are uncommitted and unstaged for review. No changes were
pushed. Earlier local commit hashes and patches are historical and must not be
used as the current publication plan.

## Changed engine files

- src/adcs/mcp/product_scope.py: C++ scope and cpp/c++ aliases.
- src/adcs/api/mcp_gateway.py: dedicated C++ GET/POST route.
- infra/helm/adcs/values.yaml: C++ ingress path.
- tests/test_words_cpp_mcp.py: C++ scope, alias, isolation and retrieval tests.
- README.md and CHANGELOG.md: C++ endpoint documentation.

The plugin still uses dotted FQNs; engine retrieval-profile validation is unchanged.
Plugin source-layout, fixture and deployment registration changes are retained.

## Verification

Run C++ and .NET regression tests (Java branch tests are intentionally absent):

```powershell
$env:PYTHONPATH = Join-Path $PWD 'engine/src'
./.venv/Scripts/python.exe -m pytest engine/tests/test_words_cpp_mcp.py engine/tests/test_words_net_mcp.py -q
./.venv/Scripts/python.exe scripts/verify_registration.py
```

The previous live HTTP initialization check passed before removing Java changes;
current C++/.NET regression and registration checks are recorded in the task.
Review with `git -C engine diff`, `git -C plugins/words-cpp diff`, and `git diff`.
New untracked tests and fixtures must also be opened/reviewed separately.

When you choose to publish, commit and push the engine and plugin first, then
stage their new gitlinks in the deployment and commit/push that repository.
After review merges, re-pin to the actual merged commits. Do not run setup's
submodule update while changes are uncommitted. No commit or push is performed
by this document.
