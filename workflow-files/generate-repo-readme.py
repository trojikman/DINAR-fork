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

import yaml
from plumbum import FG
from plumbum.cmd import cp, git, mkdir


def cmd(command, ignore_errors=False):
    print(command)
    try:
        print(command())
    except Exception:
        if not ignore_errors:
            raise


if __name__ == "__main__":
    repo_path = sys.argv[1]

    main(repo_path)
