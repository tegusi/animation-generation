'''
Max-Planck-Gesellschaft zur Foerderung der Wissenschaften e.V. (MPG) is holder of all proprietary rights on this
computer program.

You can only use this computer program if you have closed a license agreement with MPG or you get the right to use
the computer program from someone who is authorized to grant you that right.

Any use of the computer program without a valid license is prohibited and liable to prosecution.

Copyright 2019 Max-Planck-Gesellschaft zur Foerderung der Wissenschaften e.V. (MPG). acting on behalf of its
Max Planck Institute for Intelligent Systems and the Max Planck Institute for Biological Cybernetics.
All rights reserved.

More information about FLAME is available at http://flame.is.tue.mpg.de.
For comments or questions, please email us at flame@tue.mpg.de
'''


import os
os.environ["PYOPENGL_PLATFORM"] = "osmesa"
import cv2
import six
import argparse
import numpy as np
import tensorflow as tf
from psbody.mesh import Mesh
from psbody.mesh.meshviewer import MeshViewer
from utils.rendering import render_mesh_helper

from tf_smpl.batch_smpl import SMPL

def sample_texture(model_fname, texture_fname, num_samples, out_path):
    '''
    Sample the FLAME model to demonstrate how to vary the model parameters.FLAME has parameters to
        - model identity-dependent shape variations (paramters: shape),
        - articulation of neck (paramters: pose[0:3]), jaw (paramters: pose[3:6]), and eyeballs (paramters: pose[6:12])
        - model facial expressions, i.e. all expression motion that does not involve opening the mouth (paramters: exp)
        - global translation (paramters: trans)
        - global rotation (paramters: rot)
    :param model_fname          saved FLAME model
    :param num_samples          number of samples
    :param out_path             output path to save the generated templates (no templates are saved if path is empty)
    '''

    tf_trans = tf.Variable(np.zeros((1,3)), name="trans", dtype=tf.float64, trainable=True)
    tf_rot = tf.Variable(np.zeros((1,3)), name="pose", dtype=tf.float64, trainable=True)
    tf_pose = tf.Variable(np.zeros((1,12)), name="pose", dtype=tf.float64, trainable=True)
    tf_shape = tf.Variable(np.zeros((1,300)), name="shape", dtype=tf.float64, trainable=True)
    tf_exp = tf.Variable(np.zeros((1,100)), name="expression", dtype=tf.float64, trainable=True)
    smpl = SMPL(model_fname)
    tf_model = tf.squeeze(smpl(tf_trans,
                               tf.concat((tf_shape, tf_exp), axis=-1),
                               tf.concat((tf_rot, tf_pose), axis=-1)))

    texture_model = np.load(texture_fname)
    tex_dim = texture_model['tex_dir'].shape[-1]
    tf_tex_params = tf.Variable(np.zeros((1,tex_dim)), name="pose", dtype=tf.float64, trainable=True)
    tf_tex_mean = tf.Variable(np.reshape(texture_model['mean'], (1,-1)), name='tex_mean', dtype=tf.float64, trainable=False)
    tf_tex_dir = tf.Variable(np.reshape(texture_model['tex_dir'], (-1, tex_dim)).T, name='tex_dir', dtype=tf.float64, trainable=False)
    
    tf_tex = tf.add(tf_tex_mean, tf.matmul(tf_tex_params, tf_tex_dir)),
    tf_tex = tf.reshape(tf_tex, (texture_model['tex_dir'].shape[0], texture_model['tex_dir'].shape[1], texture_model['tex_dir'].shape[2]))
    tf_tex = tf.cast(tf.clip_by_value(tf_tex, 0.0, 255.0), tf.int64)

    with tf.Session() as session:
        session.run(tf.global_variables_initializer())
        mv = MeshViewer()

        for i in range(num_samples):
            assign_tex = tf.assign(tf_tex_params, np.random.randn(tex_dim)[np.newaxis,:])
            session.run([assign_tex])

            v, tex = session.run([tf_model, tf_tex])
            out_mesh = Mesh(v, smpl.f)
            out_mesh.vt = texture_model['vt']
            out_mesh.ft = texture_model['ft']
            img = render_mesh_helper(out_mesh, None)
            cv2.imwrite(os.path.join(out_path, 'test.png'), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

            mv.set_dynamic_meshes([out_mesh], blocking=True)
            key = six.moves.input('Press (s) to save sample, any other key to continue ')
            if key == 's':
                out_mesh_fname = os.path.join(out_path, 'tex_sample_%02d.obj' % (i+1))
                out_tex_fname = out_mesh_fname.replace('obj', 'png')
                cv2.imwrite(out_tex_fname, tex)
                out_mesh.set_texture_image(out_tex_fname)
                out_mesh.write_obj(out_mesh_fname)

def main(args):
    if not os.path.exists(args.model_fname):
        print('FLAME model not found - %s' % args.model_fname)
        return
    if not os.path.exists(args.texture_fname):
        print('Texture model not found - %s' % args.texture_fname)
        return
    if not os.path.exists(args.out_path):
        os.makedirs(args.out_path)
    sample_texture(args.model_fname, args.texture_fname, int(args.num_samples), args.out_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sample FLAME shape space')
    parser.add_argument('--model_fname', default='./flame/generic_model.pkl', help='Path of the FLAME model')
    parser.add_argument('--texture_fname', default='./flame/FLAME_texture.npz', help='Path of the texture model')
    parser.add_argument('--num_samples', default='5', help='Number of samples')
    parser.add_argument('--out_path', default='./texture_samples', help='Output path')
    args = parser.parse_args()
    main(args)