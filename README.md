# Animal Clash Atlas

子供向けの教育型カードバトルゲームです。  
実在する動物だけが登場し、`Streamlit` 上で `グー / チョキ / パー` のカードバトルとして遊べます。

## Features

- 敵カードを上、自分カードを下に置いたカードバトル風UI
- HPバー、あいこカウント、中央バトルログ
- 3回あいこでアイコ技が発動
- 弱点属性ヒット時は `弱点！1.5倍！` を表示
- 動物ごとのカード編集
- 動物画像を差し替え可能

## Local Setup

```bash
uv sync
uv run streamlit run app.py
```

## Animal Images

次のフォルダに画像を置くと、絵文字の代わりにカード画像として表示されます。

`assets/animals/`

ファイル名は動物名と一致させてください。

- `assets/animals/ライオン.png`
- `assets/animals/ワニ.png`
- `assets/animals/ハヤブサ.png`

対応拡張子:

- `.png`
- `.jpg`
- `.jpeg`
- `.webp`

## Deploy To Streamlit Community Cloud

このリポジトリは `app.py` をエントリーポイントとして、そのまま `Streamlit Community Cloud` に載せる想定です。

### 1. GitHub に push

```bash
git init
git add .
git commit -m "Initial Streamlit MVP"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

### 2. Streamlit Community Cloud でデプロイ

1. [Streamlit Community Cloud](https://share.streamlit.io/) にログイン
2. `New app` を選択
3. GitHub リポジトリを選択
4. Branch: `main`
5. Main file path: `app.py`
6. `Deploy` を押す

### 3. 公開URL

デプロイ完了後、自動で共有URLが発行されます。

## Dependency Notes

このプロジェクトは `uv` で管理しています。

- `uv.lock`
- `pyproject.toml`

`Streamlit Community Cloud` は依存ファイルとして `uv.lock` を認識するため、この構成のまま公開できます。

## Project Structure

```txt
app.py
core.py
pyproject.toml
uv.lock
assets/
  animals/
```
