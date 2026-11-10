"""Validate the deployment and exercise the actual registered worker with a fixture."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine/src"))
from adcs.plugins.catalog import PluginCatalog
from adcs.retrieval.profiles import load_profiles

path = ROOT / "config/product-platform-plugins.json"
catalog = PluginCatalog(path)
assert set(catalog.plugins) == {"aspose.words.cpp"}
assert not catalog.compositions
manifest = catalog.extractor("aspose.words.cpp")
profiles = load_profiles(str(path))
assert set(profiles) == {("aspose.words", "cpp")}
source = manifest.sources["docs"]
relative = source.prefix + "/_index.md"
request = {
    "contract": manifest.contract, "plugin_id": manifest.plugin_id,
    "product_id": manifest.product_id, "language": manifest.language,
    "operation": "extract", "source_kind": "docs", "repo_id": source.repo_id,
    "product_family": "aspose", "source_path": source.path + "/" + relative,
    "relative_repo_path": relative, "source_prefix": source.prefix,
    "layout_detection": source.layout, "source_revision": "deployment-fixture",
    "canonical_base_url": source.canonical_base_url,
    "raw_markdown": (ROOT / "plugins/words-cpp/tests/fixtures/docs.md").read_text(encoding="utf-8"),
}
plugin_python = ROOT / "plugins/words-cpp/.venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
interpreter = str(plugin_python) if plugin_python.is_file() else sys.executable
result = subprocess.run(catalog.command(manifest.plugin_id, python=interpreter),
                        input=json.dumps(request), text=True, encoding="utf-8", capture_output=True, check=True)
payload = json.loads(result.stdout)
assert payload["plugin_id"] == manifest.plugin_id
assert payload["result"]["chunk_records"]
print("Words/C++ registration, retrieval profile and worker extraction verified")
