#!/usr/bin/env python3
"""Render the Homebrew cask for a published release.

  python3 scripts/update-cask.py --tag v0.1.1 --output path/to/Casks/agentdeck.rb

The SHA-256 is computed from the release ZIP as it is published (downloaded), and must match the
release's own .sha256 file.
"""
from pathlib import Path
import argparse
import hashlib
import os
import urllib.request

REPO = 'jdk1021/agentdeck'
TEMPLATE = '''cask "agentdeck" do
  version "{version}"
  sha256 "{sha256}"

  url "https://github.com/{repo}/releases/download/v#{{version}}/AgentDeck-#{{version}}-macos-arm64.zip"
  name "AgentDeck"
  desc "Usage limits, balances and accounts of AI coding agents in the menu bar"
  homepage "https://github.com/{repo}"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on arch: :arm64
  depends_on macos: :sonoma

  app "AgentDeck.app"
  binary "#{{appdir}}/AgentDeck.app/Contents/MacOS/agentdeck"

  uninstall quit: "org.agentdeck.AgentDeck"

  # No zap stanza: ~/Library/Application Support/AgentDeck holds the homes (and sign-ins) of
  # additional accounts. Remove it by hand only if you no longer need them.

  caveats <<~EOS
    AgentDeck is ad-hoc signed and not notarized. On first launch open
    System Settings > Privacy & Security and choose "Open Anyway".
  EOS
end
'''


def download(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'agentdeck-cask'})
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if token:
        request.add_header('Authorization', f'Bearer {token}')
    with urllib.request.urlopen(request, timeout=300) as response:
        return response.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    version = args.tag.removeprefix('v')
    base = f'https://github.com/{REPO}/releases/download/{args.tag}'
    archive = f'AgentDeck-{version}-macos-arm64.zip'
    digest = hashlib.sha256(download(f'{base}/{archive}')).hexdigest()
    published = download(f'{base}/AgentDeck-{version}-macos-arm64.sha256').decode()
    if f'{digest}  {archive}' not in published:
        raise SystemExit(f'{archive}: SHA-256 {digest} is not the one in the release .sha256 file')
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(TEMPLATE.format(version=version, sha256=digest, repo=REPO))
    print(f'{args.output}: agentdeck {version} {digest}')


if __name__ == '__main__':
    main()
