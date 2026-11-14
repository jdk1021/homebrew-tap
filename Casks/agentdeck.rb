cask "agentdeck" do
  version "0.1.3"
  sha256 "291e26543448aae4c6e6bc0b244cd01fd7629a40e0c0920ae506f1c134467c12"

  url "https://github.com/jdk1021/agentdeck/releases/download/v#{version}/AgentDeck-#{version}-macos-arm64.zip"
  name "AgentDeck"
  desc "Usage limits, balances and accounts of AI coding agents in the menu bar"
  homepage "https://github.com/jdk1021/agentdeck"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on arch: :arm64
  depends_on macos: :sonoma

  app "AgentDeck.app"
  binary "#{appdir}/AgentDeck.app/Contents/MacOS/agentdeck"

  uninstall quit: "org.agentdeck.AgentDeck"

  # No zap stanza: ~/Library/Application Support/AgentDeck holds the homes (and sign-ins) of
  # additional accounts. Remove it by hand only if you no longer need them.

  caveats <<~EOS
    AgentDeck is ad-hoc signed and not notarized. On first launch open
    System Settings > Privacy & Security and choose "Open Anyway".
  EOS
end
