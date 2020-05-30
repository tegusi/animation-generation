# [VOCA: Voice Operated Character Animation](https://voca.is.tue.mpg.de)

This is an official [VOCA](https://voca.is.tue.mpg.de) repository.

<p align="center"> 
<img src="gif/speech_driven_animation.gif">
</p>

VOCA is a simple and generic speech-driven facial animation framework that works across a range of identities. This codebase demonstrates how to synthesize realistic character animations given an arbitrary speech signal and a static character mesh. For details please see the scientific publication

```
Capture, Learning, and Synthesis of 3D Speaking Styles.
D. Cudeiro*, T. Bolkart*, C. Laidlaw, A. Ranjan, M. J. Black
Computer Vision and Pattern Recognition (CVPR), 2019
```

A pre-print of the publication can be found [here](
https://ps.is.tuebingen.mpg.de/uploads_file/attachment/attachment/510/paper_final.pdf).

## Video

See the demo video for more details and results.

[![VOCA](https://img.youtube.com/vi/XceCxf_GyW4/0.jpg)](https://youtu.be/XceCxf_GyW4)

## 和原版区别

修改了库引用的bug,支持OSMesa进行Off-screen渲染.

## 安装

本项目在Ubuntu 16.04,Python 3.6.8和Tensorflow 1.14.0平台下运行.

(可选)建立虚拟环境,virtualenv或conda皆可,以virtualenv为例:

建立环境:
```
$ mkdir <your_home_dir>/.virtualenvs
$ python3 -m venv <your_home_dir>/.virtualenvs/voca
```

激活环境:
```
$ cd voca
$ source <your_home_dir>/voca/bin/activate
```

首先安装ffmepg

```
sudo apt install ffmpeg
```


安装依赖包:
```
pip install -r requirements.txt
```

### 安装Mesh库


安装Mesh支持库 [MPI-IS/mesh](https://github.com/MPI-IS/mesh), 必须从源码手动编译.

安装boost库, 可能需要修改BOOST_ROOT环境变量
```
sudo apt-get install libboost-dev
cd mesh
make all
```

### 安装Osmesa

为支持Off-screen渲染, pyrender环境下必须安装OSMesa或EGL. 详细信息请参考[pyrender](https://pyrender.readthedocs.io/en/latest/install/index.html#getting-pyrender-working-with-osmesa).可以尝试其中的预编译deb包,但不保证能正确运行,推荐从源码编译:

安装相关库
```
sudo apt-get install llvm-6.0 freeglut3 freeglut3-dev
```

下载Mesa源码包
```
wget ftp://ftp.freedesktop.org/pub/mesa/mesa-18.3.3.tar.gz
tar xvf mesa-18.3.3.tar.gz
cd mesa-18.3.3
```

编译
```
./configure --prefix=/usr/local                               \
            --enable-opengl --disable-gles1 --disable-gles2   \
            --disable-va --disable-xvmc --disable-vdpau       \
            --enable-shared-glapi                             \
            --disable-texture-float                           \
            --enable-gallium-llvm --enable-llvm-shared-libs   \
            --with-gallium-drivers=swrast,swr                 \
            --disable-dri --with-dri-drivers=                 \
            --disable-egl --with-egl-platforms= --disable-gbm \
            --disable-glx                                     \
            --disable-osmesa --enable-gallium-osmesa          \
            ac_cv_path_LLVM_CONFIG=llvm-config-6.0
make -j8
make install
```

最后安装pyopengl

```
git clone git@github.com:mmatl/pyopengl.git
pip install ./pyopengl
```

(更新)可能还需要更新系统软件包/gcc版本库
```
apt-get update
apt-get upgrade
apt-get install build-essential
```

## 运行Demo

### 生成mesh

利用FLAME模型进行人脸采样,输出mesh文件. 

输入模型路径: --flame_model_path, 可以选择male,female,generic_model

输出模板路径: --out_path

```
python sample_templates.py --flame_model_path './flame/generic_model.pkl' --num_samples 1 --out_path './template'
```

### 修饰VOCA输出(可选)

眨眼 (FLAME2019 only):
```
python edit_sequences.py --source_path './animation_output/meshes' --out_path './FLAME_eye_blink' --flame_model_path  './flame/generic_model.pkl' --mode blink --num_blinks 2 --blink_duration 15
```

更改姿态:
```
python edit_sequences.py --source_path './animation_output/meshes' --out_path './FLAME_variation_pose' --flame_model_path  './flame/generic_model.pkl' --mode pose --index 3 --max_variation 0.52
```

### 运行生成结果

输出路径: --out_path

输入模板路径: --template_fname

输入音频路径: --audio_fname

得到video.mp4即为最终结果

```
CUDA_VISIBLE_DEVICES=0,1,2,3 python3 run_voca.py --tf_model_fname './model/gstep_52280.model' --ds_fname './ds_graph/output_graph.pb' --audio_fname './audio/News.wav' --template_fname './template/FLAME_sample.ply' --condition_idx 3 --out_path './News'
```

### 

## Set-up

The code uses Python 3.6.8 and it was tested on Tensorflow 1.14.0.

Install pip and virtualenv
```
sudo apt-get install python3-pip python3-venv
```

Install ffmpeg
```
sudo apt install ffmpeg
```

Clone the git project:
```
$ git clone https://github.com/TimoBolkart/voca.git
```

Set up virtual environment:
```
$ mkdir <your_home_dir>/.virtualenvs
$ python3 -m venv <your_home_dir>/.virtualenvs/voca
```

Activate virtual environment:
```
$ cd voca
$ source <your_home_dir>/voca/bin/activate
```

Make sure your pip version is up-to-date:
```
pip install -U pip
```

The requirements (including tensorflow) can be installed using:
```
pip install -r requirements.txt
```

Install mesh processing libraries from [MPI-IS/mesh](https://github.com/MPI-IS/mesh) within the virtual environment.

## Data

#### Data to run the demo 

Download the trained VOCA model, audio sequences, and template meshes from [MPI-IS/VOCA](https://voca.is.tue.mpg.de).<br/>
Download FLAME model from [MPI-IS/FLAME](http://flame.is.tue.mpg.de/).<br/>
Download the trained DeepSpeech model (v0.1.0) from [Mozilla/DeepSpeech](https://github.com/mozilla/DeepSpeech/releases/tag/v0.1.0) (i.e. deepspeech-0.1.0-models.tar.gz).

#### Data used to train VOCA

VOCA is trained on VOCASET, a unique 4D face dataset with about 29 minutes of 4D scans captured at 60 fps and synchronized audio from 12 speakers that can be downloaded at [MPI-IS/VOCASET](https://voca.is.tue.mpg.de). 

Training subjects:
```
FaceTalk_170728_03272_TA, FaceTalk_170904_00128_TA, FaceTalk_170725_00137_TA, FaceTalk_170915_00223_TA, FaceTalk_170811_03274_TA, FaceTalk_170913_03279_TA, FaceTalk_170904_03276_TA, FaceTalk_170912_03278_TA
```
This is also the order of the subjects for the one-hot-encoding (i.e. FaceTalk_170728_03272_TA: 0, FaceTalk_170904_00128_TA: 1, ...)

Validation subjects:
```
FaceTalk_170811_03275_TA, FaceTalk_170908_03277_TA
```

Test subjects:
```
FaceTalk_170809_00138_TA, FaceTalk_170731_00024_TA 
```

## Demo

We provide demos to
1) synthesize a character animation given an speech signal (VOCA),
2) add eye blinks, alter identity dependent face shape and head pose of an animation sequence using FLAME, and
3) generate templates (e.g. by sampling the [FLAME](http://flame.is.tue.mpg.de/) identity shape space, or by reconstructing a template from an image using [RingNet](https://github.com/soubhiksanyal/RingNet) that can be animated with VOCA.)

##### VOCA output

This demo runs VOCA, which outputs the animation meshes given audio sequences, and renders the animation sequence to a video.
```
python run_voca.py --tf_model_fname './model/gstep_52280.model' --ds_fname './ds_graph/output_graph.pb' --audio_fname './audio/test_sentence.wav' --template_fname './template/FLAME_sample.ply' --condition_idx 3 --out_path './animation_output'
```

##### Edit VOCA output

VOCA outputs meshes in FLAME topology in "zero pose". This allows to edit the output sequences by varying the FLAME model parameters. These demos shows how to use FLAME to add eye blinks, edit the identity dependent face shape, or head pose of a VOCA animation sequence.

Add eye blinks (FLAME2019 only):
```
python edit_sequences.py --source_path './animation_output/meshes' --out_path './FLAME_eye_blink' --flame_model_path  './flame/generic_model.pkl' --mode blink --num_blinks 2 --blink_duration 15
```
Please not that this only demonstrates how to use FLAME to manipulate the eyelids to blink. The output motion does not resemble a true eye blink. This demo works with the FLAME2019 model only.

Edit identity-dependent shape:
```
python edit_sequences.py --source_path './animation_output/meshes' --out_path './FLAME_variation_shape' --flame_model_path  './flame/generic_model.pkl' --mode shape --index 0 --max_variation 3
```

Edit head pose:
```
python edit_sequences.py --source_path './animation_output/meshes' --out_path './FLAME_variation_pose' --flame_model_path  './flame/generic_model.pkl' --mode pose --index 3 --max_variation 0.52
```

##### Render sequence

This demo renders an animation sequence to a video.
```
python visualize_sequence.py --sequence_path './FLAME_eye_blink/meshes' --audio_fname './audio/test_sentence.wav' --out_path './FLAME_eye_blink'
python visualize_sequence.py --sequence_path './FLAME_variation_shape/meshes' --audio_fname './audio/test_sentence.wav' --out_path './FLAME_variation_shape'
python visualize_sequence.py --sequence_path './FLAME_variation_pose/meshes' --audio_fname './audio/test_sentence.wav' --out_path './FLAME_variation_pose'
```

##### Sample template

VOCA animates static templates in FLAME topology. Such templates can be obtained by fitting FLAME to scans, images, or by sampling the FLAME shape space. This demo randomly samples the FLAME identity shape space to generate new templates.
```
python sample_templates.py --flame_model_path './flame/generic_model.pkl' --num_samples 1 --out_path './template'
```

##### Reconstruct template from images

[RingNet](https://ringnet.is.tue.mpg.de/) is a framework to fully automatically reconstruct 3D meshes in FLAME topology from an image. After removing effects of pose and expression, the RingNet output mesh can be used as VOCA template. Please see the RingNet [demo](https://github.com/soubhiksanyal/RingNet) on how to reconstruct a 3D mesh from an image with neutralized pose and expression.

## Training

We provide code to train a VOCA model. Prior to training, run the VOCA output demo, as the training shares the requirements.
Additionally, download the VOCA training data from [MPI-IS/VOCA](https://voca.is.tue.mpg.de).<br/>

The training code requires a config file containing all model training parameters. To create a config file, run
```
python config_parser.py
```

To start training, run
```
python run_training.py
```

To visualize the training progress, run
```
tensorboard --logdir='./training/summaries/' --port 6006
```
This generates a [link](http://localhost:6006/) on the command line.  Open the link with a web browser to show the visualization.

## Known issues

If you get an error like
```
ModuleNotFoundError: No module named 'psbody'
```
please check if the [MPI-IS/mesh](https://github.com/MPI-IS/mesh) is successfully installed within the virtual environment.

## License

Free for non-commercial and scientific research purposes. By using this code, you acknowledge that you have read the license terms (https://voca.is.tue.mpg.de/license), understand them, and agree to be bound by them. If you do not agree with these terms and conditions, you must not use the code.


## Referencing VOCA

If you find this code useful for your research, or you use results generated by VOCA in your research, please cite following paper:

```
@article{VOCA2019,
    title = {Capture, Learning, and Synthesis of {3D} Speaking Styles},
    author = {Cudeiro, Daniel and Bolkart, Timo and Laidlaw, Cassidy and Ranjan, Anurag and Black, Michael},
    journal = {Computer Vision and Pattern Recognition (CVPR)},
    pages = {10101--10111},
    year = {2019}
    url = {http://voca.is.tue.mpg.de/}
}
```

## Acknowledgement

We thank Raffi Enficiaud and Ahmed Osman for pushing the release of psbody.mesh.








