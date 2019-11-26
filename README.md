# 自主プロ
## あめが降る！！
プロジェクターでスクリーンに飴や雨が降ってくる動画を映します。
飴を傘で弾き返して右下or左下の箱に入れられればポイント獲得！雨にあたってしまうとマイナスポイントです。
傘に何が当たったかによって光や音、振動が変化する予定。<br>

### ソフト編
#### 使うもの（予定）
* PC
* Kinect

* まずは動画づくり<br>
[参考サイト：失敗したけど画像貼り付け](https://www.qoosky.io/techs/b28ffe314d)<br>
[参考サイト：連番画像から動画作成](https://qiita.com/itoru257/items/228a91404fa77c780fd4)<br>
[参考サイト：アルファチャンネル画像を貼り付け](https://blanktar.jp/blog/2015/02/python-opencv-overlay.html)<br>

* python3 cv2 インストール<br>
```bash
$ python3 -m pip install opencv-python
```

**GIMPでアルファチャンネル画像作成**<br>
Candyだけを背景画像に貼るためには.png形式のアルファチャンネル画像を作成する必要がある。<br>
レイヤー ▶ 透明部分 ▶ アルファチャンネルの追加<br>
選択 ▶ 色域を選択　->　アルファチャンネルにしたい部分の色を選択<br>
Delete -> これでアルファチャンネル画像が作成できる。<br>
ファイル ▶ 名前をつけてエクスポート ▶ .pngで保存<br>

### ハード編
#### 使うもの（予定）
* Raspberry pi
* LEDテープ
* 振動子
* スピーカー

**Kinect**<br>
[参考になりそうなサイト](https://docs.opencv.org/master/d7/d6f/tutorial_kinect_openni.html)<br>
[python](https://gist.github.com/joinAero/1f76844278f141cea8338d1118423648)
[演習のサイト](http://www.cyber.t.u-tokyo.ac.jp/~narumi/class/mech_enshu/)<br>
