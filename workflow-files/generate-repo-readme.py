# Copyright 2020 IT Projects Labs
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import os.path
import sys
import itertools
import glob

import yaml
from plumbum import FG
from plumbum.cmd import cat

BRANCHES = ["14.0", "13.0", "12.0", "11.0", "10.0", "9.0", "8.0"]
NBSP=" "
REPOS={
    "pos-addons": {
        "prefix": NBSP*4,
        "extra_branches": ["7.0"]
    },
    "mail-addons": {
        "prefix": NBSP*3,
    },
    "misc-addons": {
        "prefix": NBSP*3,
        "extra_branches": ["7.0"]
    },
    "sync-addons": {
        "prefix": NBSP*3,
    },
    "access-addons": {
        "prefix": NBSP*1,
    },
    "website-addons":{
    },
}

def main(branch, repo_description):
    config = get_config()
    # TODO: find new modules and mark them with :tada: emoji in README
    store_modules = [{m: {store: True}} for m in config.get("addons", [])]
    repo_modules = get_repo_modules()
    modules = dict(sorted((store_modules + repo_modules).items(), key=lambda item: item[0]))    
    
    lines = [
        "[![help@itpp.dev](https://itpp.dev/images/infinity-readme.png)](mailto:help@itpp.dev)",
        "# [%s] %s" % (branch, config.get("title", repo_description)),
        "",
    ]
    for m, data in modules.items():
        lines.append("* [{module}](https://apps.odoo.com/apps/modules/{branch}/{module}/)".format(module=m, branch=branch))
    lines += [
        "",
        "Other Addons",
        "",
    ]
    for r, data in REPOS.items():
        base_url = "https://github.com/itpp-labs/" + r
        code = "* [itpp-labs/%s]: " % r
        code += data.get("prefix", "")
        bb = []
        for b in (BRANCHES + data.get("extra_branches", [])):
            bb.append("[[{branch}]]({base_url}/tree/{branch}#readme)".format(branch=b, base_url=base_url))
        code += " ".join(bb)
        lines.append(code)

    with open("README.md", "w") as readme:
        readme.write("\n".join(lines) + "\n")
    
    
def get_repo_modules():
    modules = []
    for path in itertools.chain(glob.glob("*/__manifest__.py"), glob.glob("*/__openerp__.py")):
        manifest = parse_manifest(path)
        module = path.split("/")[0]
        if manifest.get("installable", True):
            modules.append({module: {}})
    return modules
    modules_data = parse_manifests(manifests)


def get_config():
    try:
        with open(".DINAR/config.yaml") as config_file:
            config = yaml.safe_load(config_file)
    except Exception as e:
        print("Error on parsing .DINAR/config.yaml: %s" % e)
        return {}
    return config.get("repo_readme", {})


def parse_manifest(path):
    try:
        manifest_data = ast.literal_eval(cat(manifest_path))
    except Exception:
        manifest_data = {"error": "cannot parse"}
    return manifest_data


def cmd(command, ignore_errors=False):
    print(command)
    try:
        print(command())
    except Exception:
        if not ignore_errors:
            raise


if __name__ == "__main__":
    print(sys.argv)
    branch = sys.argv[1]
    repo_description = sys.argv[1]
    main(branch, repo_description)
