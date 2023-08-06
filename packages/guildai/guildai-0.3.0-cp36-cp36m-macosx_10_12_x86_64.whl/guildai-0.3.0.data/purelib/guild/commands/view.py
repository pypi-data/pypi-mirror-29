# Copyright 2017-2018 TensorHub, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division

import click

from guild import click_util
from . import runs_list

@click.command(name="view")
@runs_list.runs_list_options
@click.option(
    "--host",
    help="Name of host interface to listen on.")
@click.option(
    "--port",
    help="Port to listen on.",
    type=click.IntRange(0, 65535))
@click.option(
    "-n", "--no-open",
    help="Don't open the TensorBoard URL in a brower.",
    is_flag=True)
@click.option("--dev", is_flag=True, hidden=True)

@click_util.use_args
@click_util.render_doc

def view(args):
    """Visualize runs.
    """
    from . import view_impl
    view_impl.main(args)
