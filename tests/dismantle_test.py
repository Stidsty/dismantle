# Copyright 2021 Gary Stidston-Broadbent
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
# =============================================================================
from pathlib import Path
from dismantle.extension import Extensions
from dismantle.index import JsonFileIndexHandler
from dismantle.package import LocalPackageHandler


def test_full(datadir: Path) -> None:
    from tests.ColorExtension import ColorExtension
    from tests.GreetingExtension import GreetingExtension
    ext_types = [ColorExtension, GreetingExtension]
    index_src = datadir.join('index.json')
    index = JsonFileIndexHandler(index_src)
    packages = {}
    for pkg_meta in index:
        meta = index[pkg_meta]
        path = datadir.join(meta['path'])
        package = LocalPackageHandler(meta['name'], path)
        package._meta = {**package._meta, **meta}
        package.install()
        packages[package.name] = package
    extensions = Extensions(ext_types, packages, 'd_')
    assert extensions.types == ['color', 'greeting']
    assert list(extensions.category('color').keys()) == [
        '@scope-one/package-one.extension.green.GreenColorExtension',
        '@scope-one/package-two.extension.red.RedColorExtension',
        '@scope-one/package-three.extension.blue.BlueColorExtension',
    ]
    assert list(extensions.extensions.keys()) == ['color', 'greeting']
    assert list(extensions.imports.keys()) == [
        '@scope-one/package-one.extension.hello',
        '@scope-one/package-one.extension.green',
        '@scope-one/package-two.extension.afternoon',
        '@scope-one/package-two.extension.red',
        '@scope-one/package-three.extension.goodbye',
        '@scope-one/package-three.extension.blue'
    ]
