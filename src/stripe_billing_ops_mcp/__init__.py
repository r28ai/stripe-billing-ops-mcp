# SPDX-FileCopyrightText: 2026 R28 AI, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Stripe Billing Ops: the `finance` family of Charter, served over MCP."""

from __future__ import annotations

import sys
from typing import List, Optional


def main(argv: Optional[List[str]] = None) -> int:
    """`PKG` serves; `PKG login [app]`, `status` and `logout` connect apps."""
    from charter_packs_mcp import main as run

    args = sys.argv[1:] if argv is None else argv
    return run(
        ["finance", *args, "--name", "billing", "--command", "stripe-billing-ops-mcp"]
    )
