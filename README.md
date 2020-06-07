# Animation Generation with Speech Signal

A course project of Deep Generative Model, Spring 2020.

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
