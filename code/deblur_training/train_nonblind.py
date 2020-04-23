#!/usr/bin/env python3

import os

from utils import proc
from utils.dataset_proxy import Dataset, tvSwap
import utils.utils as ut
from utils.loss import get_loss
from utils import pix as net

import numpy as np
import tensorflow as tf

wts = 'wts/iclr'

#########################################################################
TLIST = [l.strip() for l in open('data/data_train.txt').readlines()]
# TLIST = TLIST + [l.strip() for l in open('data/Helen_train.txt').readlines()]
VLIST = [l.strip() for l in open('data/data_train.txt').readlines()]
# VLIST = VLIST + [l.strip() for l in open('data/Helen_dev.txt').readlines()]

KTLIST = 'data/kernels_train.txt'
KVLIST = 'data/kernels_train.txt'

BSZ = 64
IMSZ = 128

LR = 1e-3
drop = (29e4, 30e4, 30e4)

def get_lr(niter):
    if niter < drop[0]:
        return LR
    elif niter >= drop[0] and niter < drop[1]:
        return LR / np.sqrt(10.)
    else:
        return LR / 10.0
    return LR

VALFREQ = 30e4
SAVEFREQ = 1e3
MAXITER = drop[-1]

if not os.path.exists(wts):
    os.makedirs(wts)
#########################################################################

# Check for saved weights & optimizer states
msave = ut.ckpter(wts + '/iter_*.model.npz')
ssave = ut.ckpter(wts + '/iter_*.state.npz')
ut.logopen(wts+'/train.log')
niter = msave.iter

#########################################################################

# Setup Graphs
is_training = tf.placeholder_with_default(False, shape=[])
model = net.Net(is_training)

# Images loading setup
tset = Dataset(TLIST, KTLIST, BSZ, niter, rand_kernel=False)
vset = Dataset(VLIST, KVLIST, BSZ, 0, isval=True)
batch, swpT, swpV = tvSwap(tset, vset)
imgs, left_kernels, right_kernels, left_ck, right_ck, seeds = batch

# Generate blurry images
left_blurs = proc.gen_blur(imgs, left_kernels, nstd=2, seeds=seeds[:,:2])
right_blurs = proc.gen_blur(imgs, right_kernels, nstd=2, seeds=seeds[:,2:])

# Deblur, same model for left and right images
left_deblurs = left_blurs + model.generate(left_blurs)
right_deblurs = right_blurs + model.generate(right_blurs)

# Paired Loss
_, lvals, lnms = get_loss(left_blurs, right_blurs, left_deblurs, right_deblurs, left_kernels, right_kernels, nstd=0)
loss = 0.5 * (tf.reduce_mean(tf.abs(imgs-left_deblurs)) + tf.reduce_mean(tf.abs(imgs-right_deblurs)))

# Stop gradients
#left_deblurs = tf.stop_gradient(left_deblurs)
#right_deblurs = tf.stop_gradient(right_deblurs)

## Reblur, with random kernels
#left_reblurs = proc.gen_blur(left_deblurs, left_ck, nstd=2, seeds=None)
#right_reblurs = proc.gen_blur(right_deblurs, right_ck, nstd=2, seeds=None)
#
## Deblur, again
#left_cycle = left_reblurs + model.generate(left_reblurs)
#right_cycle = right_reblurs + model.generate(right_reblurs)
#
#
## Cycle loss
#cycle_loss = tf.reduce_mean(tf.abs(left_cycle-left_deblurs)) \
#    + tf.reduce_mean(tf.abs(right_cycle-right_deblurs))
#cycle_gt_mse = tf.reduce_mean(tf.squared_difference(imgs, left_cycle)) \
#    + tf.reduce_mean(tf.squared_difference(imgs, right_cycle))
#cycle_gt_psnr = tf.reduce_mean(-10. * tf.log(0.5*cycle_gt_mse) / tf.log(10.0))
#cycle_mse = tf.reduce_mean(tf.squared_difference(left_deblurs, left_cycle)) \
#    + tf.reduce_mean(tf.squared_difference(right_deblurs, right_cycle))
#cycle_psnr = tf.reduce_mean(-10. * tf.log(0.5*cycle_mse) / tf.log(10.0))

#loss = loss + cycle_loss
#lvals = lvals+[cycle_loss, cycle_gt_psnr, cycle_psnr]
#lnms = lnms+['cycle_loss', 'cycle_gt_psnr', 'cycle_psnr']

# MSE
mse1 = tf.reduce_mean(tf.squared_difference(imgs, left_deblurs), axis=(1,2,3))
mse2 = tf.reduce_mean(tf.squared_difference(imgs, right_deblurs), axis=(1,2,3))
mse = tf.concat([mse1, mse2], axis=0)
#loss=loss+mse
psnr = tf.reduce_mean(-10. * tf.log(mse) / tf.log(10.0))
mse = tf.reduce_mean(mse)
lvals, lnms = lvals+[mse, psnr], lnms+['mse', 'psnr']

tnms = [l+'.t' for l in lnms]
vnms = [l+'.v' for l in lnms]
# Set up optimizer
lr = tf.placeholder(shape=[], dtype=tf.float32)
opt = tf.train.AdamOptimizer(lr)
tStep = opt.minimize(loss, var_list=list(model.weights.values()))
tStep = tf.group([tStep]+model.updateOps)

#########################################################################
# Start TF session (respecting OMP_NUM_THREADS)
nthr = os.getenv('OMP_NUM_THREADS')
if nthr is None:
    sess = tf.Session()
else:
    sess = tf.Session(config=tf.ConfigProto(
        intra_op_parallelism_threads=int(nthr)))
sess.run(tf.global_variables_initializer())

#########################################################################
# Load saved weights if any
if niter > 0:
    mfn = wts+"/iter_%06d.model.npz" % niter
    sfn = wts+"/iter_%06d.state.npz" % niter

    ut.mprint("Restoring model from " + mfn )
    ut.loadNet(mfn,model.weights,sess)
    ut.mprint("Restoring state from " + sfn )
    ut.loadAdam(sfn,opt,model.weights,sess)
    ut.mprint("Done!")

#########################################################################
# Main Training loop

stop=False
ut.mprint("Starting from Iteration %d" % niter)
sess.run(tset.fetchOp,feed_dict=tset.fdict())

while niter < MAXITER and not ut.stop:

    # ## Validate model every so often
    # if niter % VALFREQ == 0 and :
    #     ut.mprint("Validating model")
    #     val_iter = vset.ndata // BSZ
    #     vloss, vset.niter = [], 0
    #     sess.run(vset.fetchOp,feed_dict=vset.fdict())
    #     for its in range(val_iter):
    #         sess.run(swpV)
    #         outs = sess.run(
    #             lvals+[vset.fetchOp],
    #             feed_dict={**vset.fdict(), is_training: False}
    #         )
    #         vloss.append(np.array(outs[:-1]))
    #     vloss = np.mean(np.stack(vloss, axis=0), axis=0)
    #     ut.vprint(niter, vnms, vloss.tolist())

    ## Run training step and print losses
    sess.run(swpT)
    if niter % 100 == 0:
        outs = sess.run(
            lvals+[tStep, tset.fetchOp],
            feed_dict={**tset.fdict(), lr: get_lr(niter), is_training: True}
        )
        ut.vprint(niter, tnms, outs[:-2])
        ut.vprint(niter, ['lr'], [get_lr(niter)])
    else:
        outs = sess.run(
            [loss, psnr, tStep, tset.fetchOp],
            feed_dict={**tset.fdict(), lr: get_lr(niter), is_training: True}
        )
        ut.vprint(niter, ['loss.t', 'psnr.t'], outs[:2])
    
    niter=niter+1
                    
    ## Save model weights if needed
    if SAVEFREQ > 0 and niter % SAVEFREQ == 0:
        mfn = wts+"/iter_%06d.model.npz" % niter
        sfn = wts+"/iter_%06d.state.npz" % niter

        ut.mprint("Saving model to " + mfn )
        ut.saveNet(mfn,model.weights,sess)
        ut.mprint("Saving state to " + sfn )
        ut.saveAdam(sfn,opt,model.weights,sess)
        ut.mprint("Done!")
        msave.clean(every=SAVEFREQ,last=1)
        ssave.clean(every=SAVEFREQ,last=1)


# Save last
if msave.iter < niter:
    mfn = wts+"/iter_%06d.model.npz" % niter
    sfn = wts+"/iter_%06d.state.npz" % niter

    ut.mprint("Saving model to " + mfn )
    ut.saveNet(mfn,model.weights,sess)
    ut.mprint("Saving state to " + sfn )
    ut.saveAdam(sfn,opt,model.weights,sess)
    ut.mprint("Done!")
    msave.clean(every=SAVEFREQ,last=1)
    ssave.clean(every=SAVEFREQ,last=1)
