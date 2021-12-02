from __future__ import (unicode_literals, division, absolute_import, print_function)

from powerline.segments import Segment, with_docstring
from powerline.theme import requires_segment_info, requires_filesystem_watcher

import yaml
from pathlib import Path

@requires_filesystem_watcher
@requires_segment_info
class ContextSegment(Segment):
    divider_highlight_group = None

    def __call__(self, pl, segment_info, create_watcher):
        kube_config_path = Path.joinpath(Path.home(), ".kube", "config")
        with open(kube_config_path) as f:
            kube_config = yaml.load(f, Loader=yaml.SafeLoader)

        ctx_name = kube_config.get("current-context", "UNKNOWN")
        return [{
            'contents': ctx_name,
            'highlight_groups': ['kubernetes:context', 'kubernetes', 'information:regular'],
        }]


@requires_filesystem_watcher
@requires_segment_info
class NamespaceSegment(Segment):
    divider_highlight_group = None

    def __call__(self, pl, segment_info, create_watcher):
        kube_config_path = Path.joinpath(Path.home(), ".kube", "config")
        with open(kube_config_path) as f:
            kube_config = yaml.load(f, Loader=yaml.SafeLoader)

        ctx_name = kube_config.get("current-context", "UNKNOWN")
        ctx = next((c for c in kube_config.get("contexts", {}) if c.get("name") == ctx_name), {})
        ns = ctx.get("context", {}).get("namespace", "default")
        return [{
            'contents': ns,
            'highlight_groups': ['kubernetes:namespace', 'kubernetes', 'information:regular'],
        }]

context = with_docstring(ContextSegment(), '''Return a Kubernetes Context segment''')
namespace = with_docstring(NamespaceSegment(), '''Return a Kubernetes Namespace segment''')
