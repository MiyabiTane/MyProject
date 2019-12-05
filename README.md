# 自主プロ
## 🍬あめが降る☔
プロジェクターでスクリーンに飴や雨が降ってくる動画を映します。
飴を傘で弾き返して右下or左下の箱に入れられればポイント獲得！雨にあたってしまうとマイナスポイントです。
傘に何が当たったかによって光や音、振動が変化する予定。<br>

### 〜ソフト編〜
#### 使うもの（予定）
* PC
* ~~Kinect~~
* Coral TPU

**まずは動画づくり**<br>
[参考サイト：失敗したけど画像貼り付け](https://www.qoosky.io/techs/b28ffe314d)<br>
[参考サイト：連番画像から動画作成](https://qiita.com/itoru257/items/228a91404fa77c780fd4)<br>
[参考サイト：アルファチャンネル画像を貼り付け](https://blanktar.jp/blog/2015/02/python-opencv-overlay.html)<br>

**python3 cv2 インストール**<br>
```bash
$ python3 -m pip install opencv-python
```

**GIMPでアルファチャンネル画像作成**<br>
Candyだけを背景画像に貼るためには.png形式のアルファチャンネル画像を作成する必要がある。<br>
レイヤー ▶ 透明部分 ▶ アルファチャンネルの追加<br>
選択 ▶ 色域を選択　->　アルファチャンネルにしたい部分の色を選択<br>
Delete -> これでアルファチャンネル画像が作成できる。<br>
ファイル ▶ 名前をつけてエクスポート ▶ .pngで保存<br>

### 傘とあめがあったたかどうかの判定<br>
* 方法その１<br>
Kinectで写真と同じ画像を認識して/object_pose使う。<br>
```bash
 source ~/semi_ws/devel/setup.bash
 roslaunch openni_launch openni.launch camera:=head_camera
 roslaunch recog_umbrella.launch
```
* 方法その２<br>
ROSのBoundingBoxArrayを使う。<br>
```bash
 roslaunch kinect.launch
```
パラメータ調節したいときは<br>
```bash
 rosrun rqt_reconfigure rqt_reconfigure
```
役に立つか不明だけど[ここ](https://www.color-sample.com/colors/397/)にHSL(HSI?)の色見本が載っている。<br>

* プロジェクターの画像の認識->プロジェクターからの映像とカメラの映像の画角を合わせて比で位置を計算する。<br>

\-----pythonでやるなら-----<br>
[参考になりそうなサイト](https://docs.opencv.org/master/d7/d6f/tutorial_kinect_openni.html)<br>
[python](https://gist.github.com/joinAero/1f76844278f141cea8338d1118423648)<br>
[演習のサイト](http://www.cyber.t.u-tokyo.ac.jp/~narumi/class/mech_enshu/)<br>

* 方法その３<br>
方法その１とその２は失敗したのでCoral TPUの情報をSubscribeする。<br>
```bash
 roscore
```
```bash
 source /opt/ros/melodic/setup.bash
 rosrun usb_cam usb_cam_node
```
```bash
 source /opt/ros/melodic/setup.bash
 source ~/coral_ws/devel/setup.bash
 roslaunch coral_usb edgetpu_object_detector.launch INPUT_IMAGE:=/usb_cam/image_raw
```
```bash
 source /opt/ros/melodic/setup.bash
 rosrun image_view image_view image:=/edgetpu_object_detector/output/image
```
パラメータをいじるなら<br>
```bash
 rosrun rqt_reconfigure rqt_reconfigure
```

### 〜ハード編〜
**使うもの（予定）**
* Raspberry pi
* LEDテープ
* 振動モーター
* スピーカー

### Raspberry piの基本<br>
ラズパイのセットアップやピンの位置など、ラズパイの詳細については[BDMのREADME.md](https://github.com/MiyabiTane/BDM)参照。<br>

ただし、今回はROSを使うためにUbuntu Mateをいれたいので、MicroSDのセットアップでは以下に従う。<br>
[公式ページ](https://www.raspberrypi.org/downloads/)でUbuntu MATEをダウンロードする。
PCのUbuntuでターミナルを開く。まず、SDカードを挿したときと挿さない時とで
`$ df -h`
を実行してその差分を見ることでSDカードのデバイス名を見る。/dev/mmcblk0p1 だったらデバイス名は /dev/mmcblk0<br>br
デバイスをアンマウントする。<>
ダウンロードしたファイルを解凍。今回は　ubuntu-mate-18.04.2-beta1-desktop-armhf+raspi-ext4.img.xz
をダウンロードしたので<br>
`$ xz -dv ubuntu-mate-18.04.2-beta1-desktop-armhf+raspi-ext4.img.xz `<br>
ファイルが解凍されて　ubuntu-mate-18.04.2-beta1-desktop-armhf+raspi-ext4.img ができるので<br>
`$  sudo dd bs=4M if=ubuntu-mate-18.04.2-beta1-desktop-armhf+raspi-ext4.img of=/dev/mmcblk0`<br>
最後に`$ sync`として、アンマウントしてからSDを抜く。<br>

ROSをいれるにはRaspberry pi上のターミナルで[このページ](http://wiki.ros.org/melodic/Installation/Ubuntu)
に書いてあることを忠実に打ち込む。<br>

### フルカラーシリアルLEDテープ<br>
[このページに載っているGitHubのコードをダウンロード！](http://jellyware.jp/kurage/raspi/led_stick.html)<br>
ロジック変換しないでもいけてしまった...。<br>
上記サイトの"回路結線図"以降を参照。
strandtest.pyの中身を応用すれば良さそう。<br>
<img width="200" src="./for_README/led_rainbow.jpg">


### 振動モーター
[ここ](https://www.petitmonte.com/robot/howto_vibrating_motor.html)に書いてあるとおりにやれば多分大丈夫。<br>

### スピーカー
Raspberry piのイヤホンジャックに刺せるタイプのものを購入。Raspberry piの音声出力をイヤホンジャックに設定しておく。<br>
<img width="200" src="./for_README/speaker.jpg">
