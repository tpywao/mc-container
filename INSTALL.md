## Requirements

- AWS
  - EC2
  - CloudWatch
  - IPAM?
- CloudFlare
  - Workers

### EC2

- Debian 系 OS を想定

### user `mc` を作る

- ログインしないので `nologin` を設定
- `-M` でホームディレクトリも作らない

```sh
useradd -s /sbin/nologin -M mc
```

### 必要なパッケージをインストール

- curl: MCBE サーバの DL
- git, gh: ワールドデータのバックアップ

```sh
apt install curl unzip vim gh
```

### Minecraft Bedrock Server を展開

- MCBE_SERVER_ZIP_PATH: https://www.minecraft.net/ja-jp/download/server/bedrock から取得する
- VERSION

```sh
curl -Lo ${VERSION}.zip ${MCBE_SERVER_ZIP_PATH}
unzip -d /opt/bedrock/${VERSION} ${VERSION}.zip
# アップデートを考えて main へシンボリックリンクを貼っておく
ln -s /opt/bedrock/${VERSION} /opt/bedrock/main
```

### (if need)ワールドデータと設定ファイルを取得

- REPO: worlds, server.properties, allowlist.json が含まれたリポジトリ
- BRANCH

```sh
gh auth login
gh repo clone /srv/${REPO} -- --depth 1 --branch ${BRANCH}
ln -s /opt/bedrock/main/server.properties /srv/${REPO}/server.properties
ln -s /opt/bedrock/main/allowlist.json /srv/${REPO}/allowlist.json
ln -s /opt/bedrock/main/worlds /srv/${REPO}/worlds
```

### service を導入

`/etc/systemd/system/` 配下に `mc@.service` と `mc@.socket` を配置

```sh
systemctl daemon-reload
systemctl enable mc@.socket
systemctl enable mc@.service
```
